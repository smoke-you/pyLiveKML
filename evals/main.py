"""Main module for the evals server."""

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Mapping, Any, AsyncGenerator, cast
from uuid import UUID

import uvicorn

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import (
    FileResponse,
    PlainTextResponse,
    RedirectResponse,
)
from fastapi.routing import Mount
from starlette.routing import BaseRoute
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from lxml import etree  # type: ignore

from apps.KMLApp import find_apps, KMLControlRequest, KMLControlResponse
from pyLiveKML import (
    Folder,
    KML_DOCTYPE,
    KML_HEADERS,
    Link,
    NetworkLink,
    NetworkLinkControl,
    RefreshModeEnum,
    kml_root_tag,
)

# the host address needs to be set to your local IP address, not (generally) a public one
# note that if you are running all the components (GEP, webserver, browser) from a single
# machine, 127.0.0.1 is probably the optimal choice
# note also that if you set the host address to 0.0.0.0 then the GEP interface will likely
# fail because GEP will try to access e.g. 0.0.0.0/update.kml, which may not be reachable
HOST_ADDR = "192.168.56.102"
HOST_PORT = 8111

uv_args: Mapping[str, Any] = {
    "app": "main:app",
    "host": HOST_ADDR,
    "port": HOST_PORT,
    "reload": False,
    "workers": 1,
    "log_level": "info",
    "use_colors": True,
    # set the following values to valid file paths to key and certificate files to enable HTTPS
    # 'ssl_keyfile': './certs/example.key',
    # 'ssl_certfile': './certs/example.crt',
}

# constants to set various configuration parameters
APP_PROTO = "https" if uv_args.get("ssl_keyfile", None) else "http"
APP_URI = f"{APP_PROTO}://{HOST_ADDR}:{HOST_PORT}/"
ELEMENTS_FILE = "elements.kml"
UPDATE_FILE = "update.kml"
LOADER_FILE = "loader.kml"
ELEMENTS_HREF = f"{APP_URI}{ELEMENTS_FILE}"
UPDATE_HREF = f"{APP_URI}{UPDATE_FILE}"
LOADER_HREF = f"{APP_URI}{LOADER_FILE}"
REFRESH_INTERVAL = 0.5
MIN_UPDATE_SZ: int = 1
MAX_UPDATE_SZ: int = 200


# The KML loader object; this can be a Document instead if you prefer
gep_loader = Folder(
    name="pyLiveKML Demo",
    is_open=True,
    features=[
        NetworkLink(
            name="Elements",
            is_open=True,
            link=Link(href=ELEMENTS_HREF),
        ),
        NetworkLink(
            name="Update",
            link=Link(
                href=UPDATE_HREF,
                refresh_mode=RefreshModeEnum.ON_INTERVAL,
                refresh_interval=REFRESH_INTERVAL,
            ),
        ),
    ],
)

# The master synchronization controller, a NetworkLinkControl object
gep_sync = NetworkLinkControl(
    target_href=ELEMENTS_HREF,
    # link_name="pyLiveKML synchronizer",
    # link_description="Synchronizes the webserver UI state with Google Earth Pro.",
)
# assign a constant UUID to the container, so that it can be refreshed in GEP
# without having to reload the pyLiveKML link after restarting the server
gep_sync.container._id = UUID("8c2cda8e-7d56-4a29-99e7-e05e6dbaf193")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """FastAPI lifespan context manager."""
    # pre-yield: server startup
    global applist
    # set the gep_sync NetworkLinkControl for all of the apps, and fire it up
    for x in applist:
        x.sync = gep_sync
        x.load_data()
    yield
    # post-yield: server shutdown


local_dir = Path(__file__).parent
routes: list[BaseRoute | Mount] = [
    Mount(
        "/static", StaticFiles(directory=local_dir.joinpath("static")), name="static"
    ),
]
applist = find_apps(local_dir.joinpath("apps"))
routes.extend(map(lambda x: Mount(path=x.path, app=x.app, name=x.name), applist))
app = FastAPI(routes=routes, lifespan=lifespan)
templates = Jinja2Templates(directory=local_dir.joinpath("templates"))


@app.get("/favicon.ico")
async def _() -> FileResponse:
    return FileResponse(local_dir.joinpath("static/img/earth.png"))


@app.get("/")
async def _() -> RedirectResponse:
    return RedirectResponse("index.html")


@app.get("/{filename}")
async def _(filename: str, request: Request) -> Any:
    root = kml_root_tag()
    if filename == "index.html":
        for c in gep_sync.container:
            c.activate(False, True)
        context = {
            "request": request,
            "applist": applist,
            "updateSz": {
                "value": gep_sync.update_limit,
                "min": MIN_UPDATE_SZ,
                "max": MAX_UPDATE_SZ,
            },
        }
        return templates.TemplateResponse("index.html.j2", context)
    elif filename == ELEMENTS_FILE:
        elems = etree.SubElement(
            root, gep_sync.container._kml_tag, attrib={"id": str(gep_sync.container.id)}
        )
        gep_sync.container.build_kml(elems, False)
    elif filename == UPDATE_FILE:
        root.append(gep_sync.construct_sync())
    elif filename == LOADER_FILE:
        root.append(gep_loader.construct_kml())
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    return PlainTextResponse(
        content=etree.tostring(
            root, doctype=KML_DOCTYPE, encoding="utf-8", pretty_print=True
        ),
        headers=KML_HEADERS,
    )


@app.post("/clear")
async def _() -> None:
    for c in gep_sync.container:
        c.activate(False, True)


@app.post("/control", response_model=KMLControlResponse)
async def _(ctrl: KMLControlRequest) -> KMLControlResponse:
    try:
        updatesz = int(ctrl.req.get("updateSz", 0))
        if updatesz:
            if updatesz < 1 or updatesz > 200:
                raise Exception("updateSz is out of range")
            gep_sync.update_limit = updatesz
            return KMLControlResponse(rsp={"updateSz": gep_sync.update_limit})
    except ValueError:
        raise HTTPException(404, "updateSz is not an integer")
    except Exception as ex:
        raise HTTPException(404, ex.args)
    return KMLControlResponse(rsp={})


if __name__ == "__main__":
    uvicorn.run(**uv_args)
