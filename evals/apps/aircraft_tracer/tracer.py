import json

from datetime import datetime
from pathlib import Path

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from .AircraftPosition import AircraftPosition
from evals.apps.KMLApp import KMLApp, KMLSelect
from src.pyLiveKML.KML.KMLObjects.Folder import Folder


def load_adsb_exchange_data(filename: Path) -> Folder:
    with open(filename) as f:
        sample_data = json.loads(f.read())
    try:
        kmldata = Folder(sample_data['r'])
        transponder = sample_data['icao']
        flight = sample_data['r']
        base_ts = sample_data['timestamp']
        trace = sample_data['trace']
        for t in trace:
            try:
                p = AircraftPosition(
                    transponder,
                    flight,
                    datetime.fromtimestamp(base_ts + t[0]),
                    t[2],
                    t[1],
                    t[3] * 0.3048 if isinstance(t[3], (float, int)) else None,
                    t[4] * 1.852 if isinstance(t[4], (float, int)) else 0,
                    t[5] if isinstance(t[5], (float, int)) else 0,
                )
                kmldata.append(p)
            except BaseException as x:
                print(x)
        return kmldata
    except BaseException as x:
        print(x)


tracer_app = FastAPI()
locdir = Path(__file__).parent
with open(locdir.joinpath('description.txt'), 'r') as f:
    description = f.read()
templates = Jinja2Templates(directory=locdir.joinpath('templates'))
tracer_data = [
    load_adsb_exchange_data(file)
    for file in locdir.parent.joinpath('aircraft_data').glob('*.json')
]
for a in tracer_data:
    a.select(False, True)
tracer = KMLApp('Tracer', description, '/tracer', tracer_app, tracer_data)


@tracer_app.get('/')
async def _(request: Request):
    return templates.TemplateResponse(
        'tracer.html.j2',
        {'request': request, 'aircraftlist': tracer_data},
    )


@tracer_app.post('/select')
async def _(select: KMLSelect | list[KMLSelect]):
    if isinstance(select, KMLSelect):
        select_list = [select]
    else:
        select_list = select
    for s in select_list:
        for f in tracer.sync.container:
            if s.id == f.id:
                f.select(s.checked, True)
                break
