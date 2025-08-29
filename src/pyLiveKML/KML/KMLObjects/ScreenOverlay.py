"""ScreenOverlay module."""

from abc import ABC
from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML.KML._BaseObject import _FieldDef
from pyLiveKML.KML.GeoColor import GeoColor
from pyLiveKML.KML.KMLObjects.AbstractView import AbstractView
from pyLiveKML.KML.KMLObjects.Overlay import Overlay
from pyLiveKML.KML.KMLObjects.Region import Region
from pyLiveKML.KML.KMLObjects.StyleSelector import StyleSelector
from pyLiveKML.KML.KMLObjects.TimePrimitive import TimePrimitive
from pyLiveKML.KML.Vec2 import OverlayXY, RotationXY, ScreenXY, Size


class ScreenOverlay(Overlay):
    """A KML 'ScreenOverlay', per https://developers.google.com/kml/documentation/kmlreference#screenoverlay."""

    _kml_tag = "ScreenOverlay"
    _kml_fields = Overlay._kml_fields + (_FieldDef("rotation"),)
    _direct_children = Overlay._direct_children + (
        "overlay_xy",
        "screen_xy",
        "rotation_xy",
        "size",
    )

    def __init__(
        self,
        # ScreenOverlay parameters
        overlay_xy: OverlayXY,
        screen_xy: ScreenXY,
        rotation_xy: RotationXY,
        size: Size,
        # Overlay parameters
        icon: str,
        draw_order: int | None = None,
        color: GeoColor | int | None = None,
        # ScreenOverlay parameters
        rotation: float = 0,
        # Feature parameters
        name: str | None = None,
        visibility: bool | None = None,
        is_open: bool | None = None,
        author_name: str | None = None,
        author_link: str | None = None,
        address: str | None = None,
        phone_number: str | None = None,
        snippet: str | None = None,
        snippet_max_lines: int | None = None,
        description: str | None = None,
        abstract_view: AbstractView | None = None,
        time_primitive: TimePrimitive | None = None,
        style_url: str | None = None,
        styles: Iterable[StyleSelector] | None = None,
        region: Region | None = None,
    ):
        """IconStyle instance constructor."""
        Overlay.__init__(
            self,
            icon=icon,
            draw_order=draw_order,
            color=color,
            name=name,
            visibility=visibility,
            is_open=is_open,
            author_name=author_name,
            author_link=author_link,
            address=address,
            phone_number=phone_number,
            snippet=snippet,
            snippet_max_lines=snippet_max_lines,
            description=description,
            abstract_view=abstract_view,
            time_primitive=time_primitive,
            style_url=style_url,
            styles=styles,
            region=region,
        )
        ABC.__init__(self)
        self.overlay_xy = overlay_xy
        self.screen_xy = screen_xy
        self.rotation_xy = rotation_xy
        self.size = size
        self.rotation = rotation
