import json

from datetime import datetime
from pathlib import Path

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from .AircraftData import AircraftData
from .AircraftTrail import AircraftTrail
from evals.apps.KMLApp import KMLApp, KMLControlRequest, KMLControlResponse, KMLSelect


def load_adsb_exchange_data(filename: str, trailsz: int = 20) -> AircraftTrail:
    data = list[AircraftData]()
    with open(filename) as f:
        sample_data = json.loads(f.read())
    try:
        transponder = sample_data['icao']
        flight = sample_data['r']
        base_ts = sample_data['timestamp']
        trace = sample_data['trace']
        for t in trace:
            try:
                data.append(
                    AircraftData(
                        transponder,
                        flight,
                        datetime.fromtimestamp(base_ts + t[0]),
                        t[2],
                        t[1],
                        t[3] * 0.3048 if isinstance(t[3], (float, int)) else None,
                        t[4] * 1.852 if isinstance(t[4], (float, int)) else 0,
                        t[5] if isinstance(t[5], (float, int)) else 0,
                    )
                )
            except BaseException as x:
                print(x)
    except BaseException as x:
        print(x)
    return AircraftTrail(data, trailsz)


DEFAULT_TRAIL_SZ: int = 20
MIN_TRAIL_SZ: int = 1
MAX_TRAIL_SZ: int = 100
trail_sz = DEFAULT_TRAIL_SZ
trail_app = FastAPI()
locdir = Path(__file__).parent
with open(locdir.joinpath('description.txt'), 'r') as f:
    description = f.read()
templates = Jinja2Templates(directory=locdir.joinpath('templates'))
trail_data: list[AircraftTrail] = [
    load_adsb_exchange_data(file, trail_sz)
    for file in locdir.parent.joinpath('aircraft_data').glob('*.json')
]
for a in trail_data:
    a.select(False, True)
trail = KMLApp('Trail', description, '/trail', trail_app, trail_data)


@trail_app.get('/')
async def _(request: Request):
    return templates.TemplateResponse(
        'trail.html.j2',
        {
            'request': request,
            'aircraftlist': trail_data,
            'trailSz': {
                'value': trail_sz,
                'min': MIN_TRAIL_SZ,
                'max': MAX_TRAIL_SZ,
            },
        },
    )


@trail_app.post('/select')
async def _(select: KMLSelect | list[KMLSelect]):
    if isinstance(select, KMLSelect):
        select_list = [select]
    else:
        select_list = select
    for s in select_list:
        for f in trail.sync.container:
            if s.id == f.id:
                f.select(s.checked, True)
                break


@trail_app.post('/control', response_model=KMLControlResponse)
async def _(ctrl: KMLControlRequest):
    global trail_sz
    try:
        trailsz = int(ctrl.req.get('trailSz', 0))
        if trailsz:
            if trailsz < MIN_TRAIL_SZ or trailsz > MAX_TRAIL_SZ:
                raise Exception('trailSz is out of range')
            trail_sz = trailsz
            for a in trail_data:
                a.trail_sz = trailsz
            return KMLControlResponse(rsp={'trailSz': trail_sz})
    except ValueError:
        raise HTTPException(404, 'trailSz is not an integer')
    except Exception as ex:
        raise HTTPException(404, ex.args)
    return KMLControlResponse(rsp={})
