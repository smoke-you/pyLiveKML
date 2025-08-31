"""Overlay module."""

from abc import ABC
from typing import Iterable, cast

from lxml import etree  # type: ignore

from pyLiveKML.KML.Object import (
    _BaseObject,
    _FieldDef,
    ColorParse,
    NoDump,
)
from pyLiveKML.KML.GeoColor import GeoColor
from pyLiveKML.KMLObjects.AbstractView import AbstractView
from pyLiveKML.KMLObjects.Feature import Feature
from pyLiveKML.KML.Object import _ChildDef
from pyLiveKML.KMLObjects.Region import Region
from pyLiveKML.KMLObjects.StyleSelector import StyleSelector
from pyLiveKML.KMLObjects.TimePrimitive import TimePrimitive


class _Overlay_Icon(_BaseObject):
    """A minimalist Icon class, used only within `Overlay`."""

    _kml_tag = "Icon"
    _kml_fields = _BaseObject._kml_fields + (_FieldDef("href"),)

    def __init__(self, href: str):
        """_Overlay_Icon instance constructor."""
        super().__init__()
        self.href = href


class Overlay(Feature, ABC):
    """A KML 'Overlay', per https://developers.google.com/kml/documentation/kmlreference#overlay."""

    _kml_tag = ""
    _kml_fields: tuple[_FieldDef, ...] = Feature._kml_fields + (
        _FieldDef("icon", dumper=NoDump),
        _FieldDef("color", parser=ColorParse),
        _FieldDef("draw_order", "drawOrder"),
    )
    _direct_children = Feature._direct_children + (_ChildDef("icon"),)

    def __init__(
        self,
        icon: str,
        draw_order: int | None = None,
        color: GeoColor | int | None = None,
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
        Feature.__init__(
            self,
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
        self.icon = _Overlay_Icon(icon)
        self.draw_order = draw_order
        self.color = cast(GeoColor | None, color)
