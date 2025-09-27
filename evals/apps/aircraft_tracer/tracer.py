# pyLiveKML: A python library that streams geospatial data using the KML protocol.
# Copyright (C) 2022 smoke-you

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""tracer module."""

import json
from datetime import datetime
from pathlib import Path
from typing import cast

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from lxml import etree  # type: ignore

from pyLiveKML import (
    KML_DOCTYPE,
    KML_HEADERS,
    AltitudeModeEnum,
    Camera,
    Document,
    Folder,
    GeoCoordinates,
    Point,
    TimeSpan,
    kml_root_tag,
)
from pyLiveKML.objects.Feature import Feature

from ..KMLApp import KMLApp, KMLSelect
from .AircraftPosition import AircraftPosition


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
            except BaseException as ex:
                print(ex)
        kmldata.time_primitive = TimeSpan(
            cast(AircraftPosition, kmldata[0]).timestamp,
            cast(AircraftPosition, kmldata[-1]).timestamp,
        )
        min_lon = min(
            map(
                lambda x: cast(
                    Point, cast(AircraftPosition, x).geometry
                ).coordinates.lon,
                kmldata.features,
            )
        )
        max_lon = max(
            map(
                lambda x: cast(
                    Point, cast(AircraftPosition, x).geometry
                ).coordinates.lon,
                kmldata.features,
            )
        )
        min_lat = min(
            map(
                lambda x: cast(
                    Point, cast(AircraftPosition, x).geometry
                ).coordinates.lat,
                kmldata.features,
            )
        )
        max_lat = max(
            map(
                lambda x: cast(
                    Point, cast(AircraftPosition, x).geometry
                ).coordinates.lat,
                kmldata.features,
            )
        )
        kmldata.abstract_view = Camera(
            GeoCoordinates((min_lon + max_lon) / 2, (min_lat + max_lat) / 2, 2500000),
            altitude_mode=AltitudeModeEnum.ABSOLUTE,
        )
    except BaseException as ex:
        print(ex)
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
    a.activate(False, True)
tracer = KMLApp(
    "Tracer", description, "/tracer", tracer_app, cast(list[Feature], tracer_data)
)


@tracer_app.get("/")
async def _(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "tracer.html.j2",
        {"request": request, "aircraftlist": tracer_data},
    )


@tracer_app.get("/loadable-tracer.kml")
async def _(request: Request) -> PlainTextResponse:
    root = kml_root_tag()
    doc = Document(
        "tracer",
        features=[x for x in tracer_data if x.active],
    )
    root.append(doc.construct_kml())
    return PlainTextResponse(
        content=etree.tostring(
            root, doctype=KML_DOCTYPE, encoding="utf-8", pretty_print=True
        ),
        headers=KML_HEADERS,
    )


@tracer_app.post("/select")
async def _(select: KMLSelect | list[KMLSelect]) -> None:
    if isinstance(select, KMLSelect):
        select_list = [select]
    else:
        select_list = select
    for s in select_list:
        target = next(filter(lambda x: x.id == str(s.id), tracer.data), None)
        if target is None:
            continue
        if target in tracer.sync and not s.checked:
            tracer.sync.remove(target)
            target.force_idle()
        elif target not in tracer.sync and s.checked:
            tracer.sync.append(target)
            target.activate(True, True)
