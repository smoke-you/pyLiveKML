"""simple KML app module."""

from pathlib import Path
from typing import Callable, Mapping, cast

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse, Response
from fastapi.templating import Jinja2Templates
from lxml import etree  # type: ignore

from pyLiveKML import kml_root_tag, KML_DOCTYPE, KML_HEADERS, Document

from ..KMLApp import KMLApp
from . import most_examples_builder
from . import track_example_builder
from . import multitrack_example_builder
from . import tour_example_builder


simple_app = FastAPI()
locdir = Path(__file__).parent
with open(locdir.joinpath("description.txt"), "r") as f:
    description = f.read()
templates = Jinja2Templates(directory=locdir.joinpath("templates"))
simple = KMLApp("Simple", description, "/simple", simple_app)


@simple_app.get("/")
async def _(request: Request) -> Response:
    return templates.TemplateResponse(
        "simple.html.j2",
        {"request": request},
    )


@simple_app.get("/{filename}")
async def _(filename: str, request: Request) -> Response:
    pathmap: dict[str, Callable[[str], Document]] = {
        "most_examples.kml": most_examples_builder.build_doc,
        "track_example.kml": track_example_builder.build_doc,
        "multitrack_example.kml": multitrack_example_builder.build_doc,
        "tour_example.kml": tour_example_builder.build_doc,
    }
    builder = pathmap.get(filename, None)
    if builder is None:
        raise HTTPException(status_code=404, detail="File not found")
    root = kml_root_tag()
    root.append(builder(str(request.base_url)).construct_kml())
    return PlainTextResponse(
        etree.tostring(root, doctype=KML_DOCTYPE, encoding="utf-8", pretty_print=True),
        200,
        KML_HEADERS,
    )
