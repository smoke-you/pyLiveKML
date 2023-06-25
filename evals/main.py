import uvicorn

from pathlib import Path

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import FileResponse, PlainTextResponse, RedirectResponse
from fastapi.routing import Mount
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.routing import Route
from lxml import etree

from evals.apps.KMLApp import find_apps, KMLControlRequest, KMLControlResponse
from src.pyLiveKML.KML.KML import RefreshMode, kml_tag, kml_header
from src.pyLiveKML.KML.KMLObjects.Folder import Folder
from src.pyLiveKML.KML.KMLObjects.NetworkLink import NetworkLink
from src.pyLiveKML.KML.NetworkLinkControl import NetworkLinkControl

# the host address needs to be set to your local IP address, not (generally) a public one
# note that if you are running all the components (GEP, webserver, browser) from a single 
# machine, 127.0.0.1 is probably the optimal choice
# note also that if you set the host address to 0.0.0.0 then the GEP interface will likely 
# fail because GEP will try to access e.g. 0.0.0.0/update.kml, which is not reachable
HOST_ADDR = '192.168.56.102'
HOST_PORT = 8111

uv_args = {
    'app': 'main:app',
    'host': HOST_ADDR,
    'port': HOST_PORT,
    'reload': False,
    'workers': 1,
    'log_level': 'info',
    'use_colors': True,
    # set the following values to valid file paths to key and certificate files to enable HTTPS
    # 'ssl_keyfile': './certs/example.key',
    # 'ssl_certfile': './certs/example.crt',
}

# constants to set various configuration parameters
APP_PROTO = 'https' if uv_args.get('ssl_keyfile', None) else 'http'
APP_URI = f'{APP_PROTO}://{HOST_ADDR}:{HOST_PORT}/'
ELEMENTS_FILE = 'elements.kml'
UPDATE_FILE = 'update.kml'
LOADER_FILE = 'loader.kml'
ELEMENTS_HREF = f'{APP_URI}{ELEMENTS_FILE}'
UPDATE_HREF = f'{APP_URI}{UPDATE_FILE}'
LOADER_HREF = f'{APP_URI}{LOADER_FILE}'
REFRESH_INTERVAL = 0.5
MIN_UPDATE_SZ: int = 1
MAX_UPDATE_SZ: int = 200


# The KML loader object; this can be a Document instead if you prefer
gep_loader = Folder(
    name='pyLiveKML Demo',
    is_open=True,
    features=[
        NetworkLink(name='Elements', href=ELEMENTS_HREF, is_open=True),
        NetworkLink(
            name='Update',
            href=UPDATE_HREF,
            refresh_mode=RefreshMode.ON_INTERVAL,
            refresh_interval=REFRESH_INTERVAL,
        ),
    ],
)

# The master synchronization controller, a NetworkLinkControl object
gep_sync = NetworkLinkControl(target_href=ELEMENTS_HREF)


local_dir = Path(__file__).parent
routes = [
    Mount(
        '/static', StaticFiles(directory=local_dir.joinpath('static')), name='static'
    ),
]
applist = find_apps(local_dir.joinpath('apps'))
routes.extend(map(lambda x: Mount(path=x.path, app=x.app, name=x.name), applist))
app = FastAPI(routes=routes)
templates = Jinja2Templates(directory=local_dir.joinpath('templates'))


@app.on_event('startup')
async def _():
    for x in applist:
        x.sync = gep_sync
        x.load_data()


@app.get('/favicon.ico')
async def _():
    return FileResponse(local_dir.joinpath('static/img/favicon.jpg'))


@app.get('/')
async def _():
    return RedirectResponse('index.html')


@app.get('/{filename}')
async def _(filename: str, request: Request):
    kml = kml_tag()
    if filename == 'index.html':
        for c in gep_sync.container:
            c.select(False, True)
        context = {
            'request': request,
            'applist': applist,
            'updateSz': {
                'value': gep_sync.container.update_limit,
                'min': MIN_UPDATE_SZ,
                'max': MAX_UPDATE_SZ,
            },
        }
        return templates.TemplateResponse('index.html.j2', context)
    elif filename == ELEMENTS_FILE:
        kml.append(gep_sync.container.construct_kml())
    elif filename == UPDATE_FILE:
        kml.append(gep_sync.update_kml())
    elif filename == LOADER_FILE:
        kml.append(gep_loader.construct_kml(with_features=True))
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    return PlainTextResponse(
        content=etree.tostring(kml, doctype=kml_header, encoding='utf-8'),
        headers={'Content-Type': 'application/vnd.google-earth.kml+xml'},
    )


@app.post('/clear')
async def _():
    for c in gep_sync.container:
        c.select(False, True)


@app.post('/control', response_model=KMLControlResponse)
async def _(ctrl: KMLControlRequest):
    try:
        updatesz = int(ctrl.req.get('updateSz', 0))
        if updatesz:
            if updatesz < 1 or updatesz > 200:
                raise Exception('updateSz is out of range')
            gep_sync.container.update_limit = updatesz
            return KMLControlResponse(rsp={'updateSz': gep_sync.update_limit})
    except ValueError:
        raise HTTPException(404, 'updateSz is not an integer')
    except Exception as ex:
        raise HTTPException(404, ex.args)
    return KMLControlResponse(rsp={})


if __name__ == '__main__':
    uvicorn.run(**uv_args)
