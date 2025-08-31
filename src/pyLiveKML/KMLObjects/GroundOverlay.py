"""GroundOverlay module."""

from abc import ABC
from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML.KML._BaseObject import (
    _BaseObject,
    _FieldDef,
    Angle180,
    Angle90,
)
from pyLiveKML.KML.GeoColor import GeoColor
from pyLiveKML.KMLObjects.AbstractView import AbstractView
from pyLiveKML.KMLObjects.Object import _ChildDef
from pyLiveKML.KMLObjects.Overlay import Overlay
from pyLiveKML.KMLObjects.Region import Region
from pyLiveKML.KMLObjects.StyleSelector import StyleSelector
from pyLiveKML.KMLObjects.TimePrimitive import TimePrimitive


class _GroundOverlay_LatLonBox(_BaseObject):
    """LatLonBox class, specific to the <GroundOverlay> KML tag."""

    _kml_tag = "LatLonBox"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("north", parser=Angle90),
        _FieldDef("south", parser=Angle90),
        _FieldDef("east", parser=Angle180),
        _FieldDef("west", parser=Angle180),
        _FieldDef("rotation", parser=Angle180),
    )

    def __init__(
        self,
        north: float,
        south: float,
        east: float,
        west: float,
        rotation: float = 0,
    ) -> None:
        """_GroundOverlay_LatLonBox instance constructor."""
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.rotation = rotation


class _GroundOverlay_LatLonQuad(_BaseObject):
    """LatLonQuad class, specific to the <GroundOverlay> KML tag."""

    _kml_tag = "gx:LatLonQuad"

    def __init__(
        self,
        quad: tuple[
            tuple[float, float],
            tuple[float, float],
            tuple[float, float],
            tuple[float, float],
        ],
    ) -> None:
        """_GroundOverlay_LatLonQuad instance constructor."""
        self.quad = quad

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        etree.SubElement(root, "coordinates").text = " ".join(
            (",".join(map(str, x)) for x in self.quad)
        )


class GroundOverlay(Overlay):
    """A KML 'GroundOverlay', per https://developers.google.com/kml/documentation/kmlreference#screenoverlay."""

    _kml_tag = "GroundOverlay"
    _kml_fields = Overlay._kml_fields + (
        _FieldDef("altitude"),
        _FieldDef("altitude_mode", "gx:altitudeMode"),
    )
    _direct_children = Overlay._direct_children + (
        _ChildDef("box"),
        _ChildDef("quad"),
    )

    def __init__(
        self,
        # Overlay parameters
        icon: str,
        # GroundOverlay parameters
        quad: tuple[
            tuple[float, float],
            tuple[float, float],
            tuple[float, float],
            tuple[float, float],
        ],
        north: float,
        south: float,
        east: float,
        west: float,
        rotation: float = 0,
        # Overlay parameters
        draw_order: int | None = None,
        color: GeoColor | int | None = None,
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
        self.quad = _GroundOverlay_LatLonQuad(quad)
        self.box = _GroundOverlay_LatLonBox(north, south, east, west, rotation)
