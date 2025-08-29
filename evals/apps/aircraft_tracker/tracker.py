"""tracker module."""

import json

from datetime import datetime
from pathlib import Path
from typing import cast

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .AircraftData import AircraftData
from .AircraftLocation import AircraftLocation
from ..KMLApp import KMLApp, KMLSelect
from pyLiveKML import NetworkLinkControl
from pyLiveKML.KML.KMLObjects.Feature import Feature


def load_adsb_exchange_data(filename: Path) -> AircraftLocation:
    """Load an ADSB exchange dataset and transform it into a useful form."""
    with open(filename) as f:
        sample_data = json.loads(f.read())
    transponder = sample_data["icao"]
    flight = sample_data["r"]
    base_ts = sample_data["timestamp"]
    trace = sample_data["trace"]
    positions = list[AircraftData]()
    try:
        for t in trace:
            try:
                p = AircraftData(
                    datetime.fromtimestamp(base_ts + t[0]),
                    t[2],
                    t[1],
                    t[3] * 0.3048 if isinstance(t[3], (float, int)) else None,
                    t[4] * 1.852 if isinstance(t[4], (float, int)) else 0,
                    t[5] if isinstance(t[5], (float, int)) else 0,
                )
                positions.append(p)
            except BaseException as x:
                print(x)
    except BaseException as x:
        print(x)
    return AircraftLocation(transponder, flight, positions)


tracker_app = FastAPI()
locdir = Path(__file__).parent
with open(locdir.joinpath("description.txt"), "r") as f:
    description = f.read()
templates = Jinja2Templates(directory=locdir.joinpath("templates"))
tracker_data = [
    load_adsb_exchange_data(file)
    for file in locdir.parent.joinpath("aircraft_data").glob("*.json")
]
for a in tracker_data:
    a.select(False, True)
tracker = KMLApp(
    "Tracker", description, "/tracker", tracker_app, cast(list[Feature], tracker_data)
)


@tracker_app.get("/")
async def _(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "tracker.html.j2",
        {"request": request, "aircraftlist": tracker_data},
    )


@tracker_app.post("/select")
async def _(select: KMLSelect | list[KMLSelect]) -> None:
    if isinstance(select, KMLSelect):
        select_list = [select]
    else:
        select_list = select
    for s in select_list:
        for f in cast(NetworkLinkControl, tracker.sync).container:
            if s.id == f.id:
                f.select(s.checked, True)
                break
