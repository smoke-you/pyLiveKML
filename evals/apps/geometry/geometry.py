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

"""geometry KML app module."""

from pathlib import Path
from typing import cast

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from lxml import etree  # type: ignore
from pydantic import BaseModel, UUID4
from pyLiveKML import (
    AltitudeModeEnum,
    BalloonStyle,
    DisplayModeEnum,
    Document,
    GeoCoordinates,
    NetworkLinkControl,
    Style,
    kml_root_tag,
    KML_DOCTYPE,
    KML_HEADERS,
)
from pyLiveKML.objects.Feature import Feature
from scipy.spatial.transform import Rotation

from .GeoEllipse import GeoEllipse
from .GeoRing import GeoRing
from .GeoShape import GeoShape
from ..KMLApp import KMLApp, KMLControlRequest, KMLControlResponse, KMLSelect


origin = GeoCoordinates(lon=-85.844, lat=40.019, alt=1000)
# the GeoShapes that will be manipulated
gpr = GeoRing(
    name="ring",
    origin=GeoCoordinates(lon=origin.lon, lat=origin.lat, alt=origin.alt),
    outer_radius=1000,
    inner_radius=800,
    num_vertices=128,
    border_width=1,
    border_color=0xFF0000FF,
    fill_color=0x4000FF00,
    altitude_mode=AltitudeModeEnum.CLAMP_TO_GROUND,
)
gpr.description = "This is a polygon with an internal cutout.\nYou can change the border and fill colours via the web UI."
# gpr.region = Region(
#     north=origin.lat + 0.05,
#     south=origin.lat - 0.05,
#     east=origin.lon + 0.05,
#     west=origin.lon - 0.05,
# )
cast(Style, gpr._styles[0]).balloon_style = BalloonStyle(0xFF400000, 0xFF0000FF)
gpe = GeoEllipse(
    name="ellipse",
    origin=GeoCoordinates(lon=origin.lon, lat=origin.lat, alt=origin.alt),
    x_radius=1000,
    y_radius=800,
    num_vertices=32,
    border_width=1,
    border_color=0xFF0000FF,
    fill_color=0x4000FF00,
    altitude_mode=AltitudeModeEnum.ABSOLUTE,
)
gpe.snippet = "This is a simple polygon.\nIt has no internal cutouts.\nYou can change the border and fill colours via the web UI."
gpe.snippet_max_lines = 3
# gpe.region = Region(
#     north=origin.lat + 0.01,
#     south=origin.lat - 0.01,
#     east=origin.lon + 0.01,
#     west=origin.lon - 0.01,
# )

geo_app = FastAPI()
locdir = Path(__file__).parent
with open(locdir.joinpath("description.txt"), "r") as f:
    description = f.read()
templates = Jinja2Templates(directory=locdir.joinpath("templates"))
geodata: list[GeoShape] = [gpr, gpe]
for g in geodata:
    g.activate(False, True)
geometry = KMLApp(
    "Geometry", description, "/geometry", geo_app, cast(list[Feature], geodata)
)


@geo_app.get("/")
async def _(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "geometry.html.j2",
        {
            "request": request,
            "geolist": geodata,
        },
    )


@geo_app.get("/loadable-geometry.kml")
async def _(request: Request) -> PlainTextResponse:
    root = kml_root_tag()
    doc = Document(
        "geometry",
        features=[x for x in geodata if x.active],
    )
    root.append(doc.construct_kml())
    return PlainTextResponse(
        content=etree.tostring(
            root, doctype=KML_DOCTYPE, encoding="utf-8", pretty_print=True
        ),
        headers=KML_HEADERS,
    )


@geo_app.post("/select")
async def _(select: KMLSelect | list[KMLSelect]) -> None:
    if isinstance(select, KMLSelect):
        select_list = [select]
    else:
        select_list = select
    for s in select_list:
        target = next(filter(lambda x: x.id == str(s.id), geometry.data), None)
        if target is None:
            continue
        if target in geometry.sync and not s.checked:
            geometry.sync.remove(target)
            target.force_idle()
        elif target not in geometry.sync and s.checked:
            geometry.sync.append(target)
            target.activate(True, True)


class OriginControlRequest(BaseModel):
    """Origin control request."""

    id: UUID4
    lat: float
    lon: float
    alt: float


class RGBControlRequest(BaseModel):
    """RGB control request."""

    id: UUID4
    rgb: str
    alpha: int


class RotationControlRequest(BaseModel):
    """Rotation control request."""

    id: UUID4
    value: float


@geo_app.post("/control", response_model=KMLControlResponse)
async def _(ctrl: KMLControlRequest) -> KMLControlResponse:
    try:
        origin = ctrl.req.get("origin", None)
        if origin:
            origin = OriginControlRequest(**origin)
            for g in geodata:
                if g.id == str(origin.id):
                    g.origin = GeoCoordinates(origin.lon, origin.lat, origin.alt)
                    break
        fill = ctrl.req.get("fill", None)
        if fill:
            fill = RGBControlRequest(**fill)
            for g in geodata:
                if g.id == str(fill.id):
                    g.fill_rgb = fill.rgb[1:]
                    g.fill_alpha = fill.alpha
                    g._styles[0].field_changed()
                    break
        border = ctrl.req.get("border", None)
        if border:
            border = RGBControlRequest(**border)
            for g in geodata:
                if g.id == str(border.id):
                    g.border_rgb = border.rgb[1:]
                    g.border_alpha = border.alpha
                    g._styles[0].field_changed()
                    break
        rotate = ctrl.req.get("rotate", None)
        if rotate:
            rotate = RotationControlRequest(**rotate)
            for g in geodata:
                if g.id == str(rotate.id):
                    g.rotate_shape(Rotation.from_euler("z", rotate.value, degrees=True))
                    break
    except ValueError:
        raise HTTPException(404, "origin is not formatted correctly")
    except Exception as ex:
        raise HTTPException(404, ex.args)
    return KMLControlResponse(rsp={})
