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

"""PhotoOverlay module."""

from abc import ABC
from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML.objects.AbstractView import AbstractView
from pyLiveKML.objects.ExtendedData import ExtendedData
from pyLiveKML.objects.Icon import Icon
from pyLiveKML.objects.Object import (
    _BaseObject,
    _ChildDef,
    _FieldDef,
    _Angle180,
    _Angle90,
)
from pyLiveKML.objects.Overlay import Overlay
from pyLiveKML.objects.Point import Point
from pyLiveKML.objects.Region import Region
from pyLiveKML.objects.StyleSelector import StyleSelector
from pyLiveKML.objects.TimePrimitive import TimePrimitive
from pyLiveKML.types import GeoColor, GridOriginEnum, OverlayShapeEnum


class ViewVolume(_BaseObject):
    """A KML `<ViewVolume>` tag constructor.

    Defines how much of the current scene is visible. Specifying the field of view is
    analogous to specifying the lens opening in a physical camera. A small field of view,
    like a telephoto lens, focuses on a small part of the scene. A large field of view,
    like a wide-angle lens, focuses on a large part of the scene.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-photooverlay

    Parameters
    ----------
    left_fov: float, default = 0
        Angle, in degrees, between the camera's viewing direction and the left side of
        the view volume.
    right_fov: float, default = 0
        Angle, in degrees, between the camera's viewing direction and the right side of
        the view volume.
    bottom_fov: float, default = 0
        Angle, in degrees, between the camera's viewing direction and the bottom side of
        the view volume.
    top_fov: float, default = 0
        Angle, in degrees, between the camera's viewing direction and the top side of the
        view volume.
    near: float, default = 0
        Measurement in meters along the viewing direction from the camera viewpoint to
        the PhotoOverlay shape.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "ViewVolume"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("left_fov", "leftFov", _Angle180),
        _FieldDef("right_fov", "rightFov", _Angle180),
        _FieldDef("bottom_fov", "bottomFov", _Angle90),
        _FieldDef("top_fov", "topFov", _Angle90),
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


class ImagePyramid(_BaseObject):
    """A KML `<ImagePyramid>` tag constructor.

    A hierarchical set of images, each of which is an increasingly lower resolution
    version of the original image.

    Each image in the pyramid is subdivided into tiles, so that only the portions in view
    need to be loaded. Google Earth calculates the current viewpoint and loads the tiles
    that are appropriate to the user's distance from the image. As the viewpoint moves
    closer to the `PhotoOverlay`, Google Earth loads higher resolution tiles. Since all
    the pixels in the original image can't be viewed on the screen at once, this
    preprocessing allows Google Earth to achieve maximum performance because it loads
    only the portions of the image that are in view, and only the pixel details that can
    be discerned by the user at the current viewpoint.

    Notes
    -----
    * When you specify an `ImagePyramid` for a `PhotoOverlay`, you must also modify the
    `icon` attribute to include specifications for which tiles to load.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-photooverlay

    Parameters
    ----------
    tile_size : int, default = 256
        Size of the tiles, in pixels. Tiles must be square, and `tile_size` must be a
        power of 2. A tile size of 256 (the default) or 512 is recommended. The original
        image is divided into tiles of this size, at varying resolutions.
    max_width : int, default = 0
        Width in pixels of the original image.
    max_height : int, default = 0
        Height in pixels of the original image.
    grid_origin : GridOriginEnum, default = GridOriginEnum.LOWER_LEFT
        Specifies where to begin numbering the tiles in each layer of the pyramid. A
        value of `LOWER_LEFT` specifies that row 1, column 1 of each layer is in the
        bottom left corner of the grid.

    Attributes
    ----------
    Same as parameters.

    """

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
        super().__init__()
        self.tile_size = tile_size
        self.max_width = max_width
        self.max_height = max_height
        self.grid_origin = grid_origin


class PhotoOverlay(Overlay):
    """A KML `<PhotoOverlay>` tag constructor.

    `PhotoOverlay` allows you to geographically locate a photograph on the Earth and to
    specify viewing parameters for this `PhotoOverlay`. The `PhotoOverlay` can be a
    simple 2D rectangle, a partial or full cylinder, or a sphere (for spherical
    panoramas). The overlay is placed at the specified location and oriented toward the
    viewpoint.

    Because `PhotoOverlay` is derived from `Feature`, it can contain a concrete instance
    of `AbstractView` - either `Camera` or `LookAt`. The `Camera` (or `LookAt`) specifies
    a viewpoint and a viewing direction (also referred to as a view vector). The
    `PhotoOverlay` is positioned in relation to the viewpoint. Specifically, the plane of
    a 2D rectangular image is orthogonal (at right angles to) the view vector. The normal
    of this plane - that is, its front, which is the part with the photo - is oriented
    toward the viewpoint.

    The URL for the `PhotoOverlay` image is specified in the `icon` attribute, which is
    inherited from `Overlay`. The `icon` must specify the image file to use for the
    `PhotoOverlay`. In the case of a very large image, `icon` is a special URL that indexes
    into a pyramid of images of varying resolutions (see `ImagePyramid`).

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#photooverlay
    * https://developers.google.com/kml/documentation/photos

    Parameters
    ----------
    point : Point
        The `Point` acts as a `Point` inside a `Placemark` element. It draws an icon to
        mark the position of the `PhotoOverlay`. The icon drawn is specified by the
        `style_url` or `StyleSelector` fields, just as it is for `Placemark`.
    shape : OverlayShapeEnum | None, default = None
        The `PhotoOverlay` is projected onto the `shape`.
    rotation : float | None, default = None
        Adjusts how the photo is placed inside the field of view. This is useful if your
        photo has been rotated and deviates slightly from a desired horizontal view.
    view_volume : ViewVolume | None, default = None
        Defines how much of the current scene is visible.
    image_pyramid : ImagePyramid | None, default = None
        For very large images, you'll need to construct an image pyramid, which is a
        hierarchical set of images, each of which is an increasingly lower resolution
        version of the original image.
    icon : str | Icon | None, default = None
        Defines the location of the image to be used as the `Overlay`. This location can
        be either on a local file system or on a web server. If this attribute is `None`,
        a rectangle is drawn using the color and size defined by the ground or screen
        overlay. If a simple `str` is supplied, then it will be used as the `href` of an
        `Icon`.
    color : GeoColor | int | None, default = None
        The image or rectangle color and transparency.
    draw_order : int | None, default = None
        Defines the stacking order for the images in overlapping `Overlay`s. `Overlay`s
        with higher `draw_order` values are drawn on top of `Overlay`s with lower
        `draw_order` values.
    name : str|None, default = None
        User-defined text displayed in the 3D viewer as the label for the object.
    visibility : bool | None, default = None
        Specifies whether the `Feature` is drawn in the 3D viewer when it is initially
        loaded. In order for a `Feature` to be visible, the `<visibility>` tag of all
        its ancestors must also be set `True`.
    is_open : bool | None, default = None
        Specifies whether a `Document` or `Folder` appears closed or open when first
        loaded into the "Places" panel. `False` or `None` is collapsed (the default),
        `True` is expanded. This element applies only to `Document`, `Folder`, and
        `NetworkLink`.
    author_name : str | None, default = None
        The name of the author of the `Feature`.
    author_link : str | None, default = None
        URL of the web page containing the KML file.
    address : str | None, default = None
        A string value representing an unstructured address written as a standard street,
        city, state address, and/or as a postal code.
    phone_number : str | None, default = None
        A string value representing a telephone number. This element is used by Google
        Maps Mobile only. The industry standard for Java-enabled cellular phones is
        RFC2806.
    snippet : str | None, default = None
        A short description of the `Feature`. In Google Earth, this description is
        displayed in the "Places" panel under the name of the `Feature`. If a `<Snippet>`
        is not supplied, the first two lines of the `<description>` are used. In Google
        Earth, if a `Placemark` contains both a `<description>` and a `<Snippet>`, the
        `<Snippet>` appears beneath the `Placemark` in the "Places" panel, and the
        `<description>` appears in the `Placemark`'s description balloon. This tag does
        not support HTML markup.
    snippet_max_lines : int | None, default = None
    description : str | None, default = None
        User-supplied content that appears in the description balloon. HTML *is*
        supported, but it is **highly** recommended to read the detailed documentation
        at
        https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-feature
    abstract_view : AbstractView | None, default = None
        Any concrete subclass of :class:`pyLiveKML.objects.AbstractView`, i.e. either a
        :class:`pyLiveKML.objects.Camera` or :class:`pyLiveKML.objects.LookAt`
    time_primitive : TimePrimitive | None, default = None
        Any concrete subclass of :class:`pyLiveKML.objects.TimePrimitive`, i.e. either a
        :class:`pyLiveKML.objects.TimeStamp` or :class:`pyLiveKML.objects.TimeSpan`
    style_url : str | None = None
        URL of a `<Style>` or `<StyleMap>` defined in a `<Document>`. If the style is in
        the same file, use a # reference. If the style is defined in an external file,
        use a full URL along with # referencing.
    styles : StyleSelector | Iterable[StyleSelector] | None, default = None
        One or more `Style`s and `StyleMap`s can be defined to customize the appearance
        of any element derived from `Feature` or of the `Geometry` in a `Placemark`. A
        style defined within a `Feature` is called an "inline style" and applies only to
        the `Feature` that contains it. A style defined as the child of a `<Document>` is
        called a "shared style." A shared style must have an id defined for it. This id
        is referenced by one or more `Features` within the `<Document>`. In cases where
        a style element is defined both in a shared style and in an inline style for a
        `Feature` — that is, a `Folder`, `GroundOverlay`, `NetworkLink`, `Placemark`, or
        `ScreenOverlay` — the value for the `Feature`'s inline style takes precedence over
        the value for the shared style.
    region : Region | None, default = None
        `Feature`s and `Geometry`'s associated with a `Region` are drawn only when the
        `Region` is active.
    extended_data : ExtendedData | None, default = None
        Allows you to add custom data to a KML file. This data can be:
        * Data that references an external XML schema.
        * Untyped data/value pairs.
        * Typed data.

        A given KML `Feature` can contain a combination of these types of custom data.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "PhotoOverlay"
    _kml_fields = Overlay._kml_fields + (
        _FieldDef("shape"),
        _FieldDef("rotation"),
    )
    _kml_children = Overlay._kml_children + (
        _ChildDef("point"),
        _ChildDef("view_volume"),
        _ChildDef("image_pyramid"),
    )

    def __init__(
        self,
        # PhotoOverlay parameters
        point: Point,
        shape: OverlayShapeEnum | None = None,
        rotation: float | None = None,
        view_volume: ViewVolume | None = None,
        image_pyramid: ImagePyramid | None = None,
        # Overlay parameters
        icon: str | Icon | None = None,
        color: GeoColor | int | None = None,
        draw_order: int | None = None,
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
        styles: StyleSelector | Iterable[StyleSelector] | None = None,
        region: Region | None = None,
        extended_data: ExtendedData | None = None,
    ):
        """PhotoOverlay instance constructor."""
        Overlay.__init__(
            self,
            icon=icon,
            color=color,
            draw_order=draw_order,
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
            extended_data=extended_data,
        )
        self.point = point
        self.shape = shape
        self.rotation = rotation
        self.view_volume = view_volume
        self.image_pyramid = image_pyramid
