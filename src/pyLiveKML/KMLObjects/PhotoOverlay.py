"""PhotoOverlay module."""

from abc import ABC
from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML.KML import GridOriginEnum
from pyLiveKML.KML.Object import (
    _BaseObject,
    _FieldDef,
    Angle180,
    Angle90,
)
from pyLiveKML.KML.GeoColor import GeoColor
from pyLiveKML.KMLObjects.AbstractView import AbstractView
from pyLiveKML.KML.Object import _ChildDef
from pyLiveKML.KMLObjects.Overlay import Overlay
from pyLiveKML.KMLObjects.Point import Point
from pyLiveKML.KMLObjects.Region import Region
from pyLiveKML.KMLObjects.StyleSelector import StyleSelector
from pyLiveKML.KMLObjects.TimePrimitive import TimePrimitive


class _PhotoOverlay_ViewVolume(_BaseObject):
    """A minimalist child class, used only within `PhotoOverlay`."""

    _kml_tag = "ViewVolume"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("left_fov", "leftFov", Angle180),
        _FieldDef("right_fov", "rightFov", Angle180),
        _FieldDef("bottom_fov", "bottomFov", Angle90),
        _FieldDef("top_fov", "topFov", Angle90),
        _FieldDef("near"),
    )

    def __init__(
        self,
        left_fov: float = 0,
        right_fov: float = 0,
        bottom_fov: float = 0,
        top_fov: float = 0,
        near: float = 0,
    ) -> None:
        """_PhotoOverlay_ViewVolume instance constructor."""
        super().__init__()
        self.left_fov = left_fov
        self.right_fov = right_fov
        self.bottom_fov = bottom_fov
        self.top_fov = top_fov
        self.near = near


class _PhotoOverlay_ImagePyramid(_BaseObject):
    """A minimalist child class, used only within `PhotoOverlay`."""

    _kml_tag = "ImagePyramid"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("tile_size", "tileSize"),
        _FieldDef("max_width", "maxWidth"),
        _FieldDef("max_height", "maxHeight"),
        _FieldDef("grid_origin", "gridOrigin"),
    )

    def __init__(
        self,
        tile_size: int = 256,
        max_width: int = 0,
        max_height: int = 0,
        grid_origin: GridOriginEnum = GridOriginEnum.LOWER_LEFT,
    ) -> None:
        """_PhotoOverlay_ImagePyramid instance constructor."""
        self.tile_size = tile_size
        self.max_width = max_width
        self.max_height = max_height
        self.grid_origin = grid_origin


class PhotoOverlay(Overlay):
    """A KML 'PhotoOverlay', per https://developers.google.com/kml/documentation/kmlreference#photooverlay."""

    _kml_tag = "PhotoOverlay"
    _kml_fields = Overlay._kml_fields + (
        _FieldDef("rotation"),
        _FieldDef("shape"),
    )
    _kml_children = Overlay._kml_children + (
        _ChildDef("point"),
        _ChildDef("view_volume"),
        _ChildDef("image_pyramid"),
    )

    def __init__(
        self,
        point: Point,
        # Overlay parameters
        icon: str,
        draw_order: int | None = None,
        color: GeoColor | int | None = None,
        # ViewVolume parameters
        left_fov: float = 0,
        right_fov: float = 0,
        bottom_fov: float = 0,
        top_fov: float = 0,
        near: float = 0,
        # ImagePyramid parameters
        tile_size: int = 256,
        max_width: int = 0,
        max_height: int = 0,
        grid_origin: GridOriginEnum = GridOriginEnum.LOWER_LEFT,
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
        self.point = point
        self.view_volume = _PhotoOverlay_ViewVolume(
            left_fov, right_fov, bottom_fov, top_fov, near
        )
        self.image_pyramid = _PhotoOverlay_ImagePyramid(
            tile_size, max_width, max_height, grid_origin
        )
