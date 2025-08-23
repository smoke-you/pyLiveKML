"""geometry module."""

from pathlib import Path
from typing import cast

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, UUID4
from pyLiveKML import NetworkLinkControl, GeoCoordinates, Feature, AltitudeMode, Region
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
    altitude_mode=AltitudeMode.CLAMP_TO_GROUND,
)
gpr.snippet = "This is a polygon with an internal cutout.\nYou can change the border and fill colours via the web UI."
gpr.region = Region(
    north=origin.lat + 0.05,
    south=origin.lat - 0.05,
    east=origin.lon + 0.05,
    west=origin.lon - 0.05,
)
gpe = GeoEllipse(
    name="ellipse",
    origin=GeoCoordinates(lon=origin.lon, lat=origin.lat, alt=origin.alt),
    x_radius=1000,
    y_radius=800,
    num_vertices=32,
    border_width=1,
    border_color=0xFF0000FF,
    fill_color=0x4000FF00,
    altitude_mode=AltitudeMode.ABSOLUTE,
)
gpe.snippet = "This is a simple polygon.\nIt has no internal cutouts.\nYou can change the border and fill colours via the web UI."
gpe.snippet_max_lines = 3
gpe.region = Region(
    north=origin.lat + 0.01,
    south=origin.lat - 0.01,
    east=origin.lon + 0.01,
    west=origin.lon - 0.01,
)

geo_app = FastAPI()
locdir = Path(__file__).parent
with open(locdir.joinpath("description.txt"), "r") as f:
    description = f.read()
templates = Jinja2Templates(directory=locdir.joinpath("templates"))
geodata: list[GeoShape] = [gpr, gpe]
for g in geodata:
    g.select(False, True)
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


@geo_app.post("/select")
async def _(select: KMLSelect | list[KMLSelect]) -> None:
    if isinstance(select, KMLSelect):
        select_list = [select]
    else:
        select_list = select
    for s in select_list:
        for f in cast(NetworkLinkControl, geometry.sync).container:
            if s.id == f.id:
                f.select(s.checked, True)
                break


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
                if g.id == origin.id:
                    g.origin = GeoCoordinates(origin.lon, origin.lat, origin.alt)
                    break
        fill = ctrl.req.get("fill", None)
        if fill:
            fill = RGBControlRequest(**fill)
            for g in geodata:
                if g.id == fill.id:
                    g.fill_rgb = fill.rgb[1:]
                    g.fill_alpha = fill.alpha
                    break
        border = ctrl.req.get("border", None)
        if border:
            border = RGBControlRequest(**border)
            for g in geodata:
                if g.id == border.id:
                    g.border_rgb = border.rgb[1:]
                    g.border_alpha = border.alpha
                    break
        rotate = ctrl.req.get("rotate", None)
        if rotate:
            rotate = RotationControlRequest(**rotate)
            for g in geodata:
                if g.id == rotate.id:
                    g.rotate_shape(Rotation.from_euler("z", rotate.value, degrees=True))
                    break
    except ValueError:
        raise HTTPException(404, "origin is not formatted correctly")
    except Exception as ex:
        raise HTTPException(404, ex.args)
    return KMLControlResponse(rsp={})
