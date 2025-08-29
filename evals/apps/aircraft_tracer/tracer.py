"""tracer module."""

import json

from datetime import datetime
from pathlib import Path
from typing import cast

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from pyLiveKML import Folder, NetworkLinkControl, TimeSpan
from pyLiveKML.KMLObjects.Feature import Feature

from .AircraftPosition import AircraftPosition
from ..KMLApp import KMLApp, KMLSelect


def load_adsb_exchange_data(filename: Path) -> Folder:
    """Load an ADSB exchange dataset and transform it into a useful form."""
    with open(filename) as f:
        sample_data = json.loads(f.read())
    kmldata = Folder(sample_data["r"])
    try:
        transponder = sample_data["icao"]
        flight = sample_data["r"]
        base_ts = sample_data["timestamp"]
        trace = sample_data["trace"]
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
        kmldata.time_primitive = TimeSpan(
            cast(AircraftPosition, kmldata[0]).timestamp,
            cast(AircraftPosition, kmldata[-1]).timestamp,
        )
    except BaseException as x:
        print(x)
    return kmldata


tracer_app = FastAPI()
locdir = Path(__file__).parent
with open(locdir.joinpath("description.txt"), "r") as f:
    description = f.read()
templates = Jinja2Templates(directory=locdir.joinpath("templates"))
tracer_data = [
    load_adsb_exchange_data(file)
    for file in locdir.parent.joinpath("aircraft_data").glob("*.json")
]
for a in tracer_data:
    a.select(False, True)
tracer = KMLApp(
    "Tracer", description, "/tracer", tracer_app, cast(list[Feature], tracer_data)
)


@tracer_app.get("/")
async def _(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "tracer.html.j2",
        {"request": request, "aircraftlist": tracer_data},
    )


@tracer_app.post("/select")
async def _(select: KMLSelect | list[KMLSelect]) -> None:
    if isinstance(select, KMLSelect):
        select_list = [select]
    else:
        select_list = select
    for s in select_list:
        for f in cast(NetworkLinkControl, tracer.sync).container:
            if s.id == f.id:
                f.select(s.checked, True)
                break
