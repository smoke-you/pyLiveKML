"""simple KML app module."""

from pathlib import Path
from typing import cast

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from lxml import etree   # type: ignore

from pyLiveKML import kml_root_tag, KML_DOCTYPE, KML_HEADERS
from pyLiveKML.KMLObjects.Feature import Feature

from ..KMLApp import KMLApp
from .build import build_data

simple_app = FastAPI()
locdir = Path(__file__).parent
with open(locdir.joinpath("description.txt"), "r") as f:
    description = f.read()
templates = Jinja2Templates(directory=locdir.joinpath("templates"))
simple = KMLApp("Simple", description, "/simple", simple_app)


@simple_app.get("/")
async def _(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "simple.html.j2",
        {
            "request": request
        },
    )


@simple_app.get("/simple_data.kml")
async def _(request: Request) -> PlainTextResponse:
    root = kml_root_tag()
    root.append(build_data.construct_kml(True))
    return PlainTextResponse(
        content=etree.tostring(
            root, doctype=KML_DOCTYPE, encoding="utf-8", pretty_print=True
        ),
        headers=KML_HEADERS,
    )
