"""ScreenOverlay module."""

from abc import ABC
from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML.objects.AbstractView import AbstractView
from pyLiveKML.objects.ExtendedData import ExtendedData
from pyLiveKML.objects.Icon import Icon
from pyLiveKML.objects.Object import _ChildDef, _FieldDef
from pyLiveKML.objects.Overlay import Overlay
from pyLiveKML.objects.Region import Region
from pyLiveKML.objects.StyleSelector import StyleSelector
from pyLiveKML.objects.TimePrimitive import TimePrimitive
from pyLiveKML.types.GeoColor import GeoColor
from pyLiveKML.types.Vec2 import OverlayXY, RotationXY, ScreenXY, Size


class ScreenOverlay(Overlay):
    """A KML `<ScreenOverlay>` tag constructor.

    Draws an image overlay fixed to the screen. Sample uses for `ScreenOverlay`s are
    compasses, logos, and heads-up displays. `ScreenOverlay` sizing is determined by the
    `size` attribute. Positioning of the overlay is handled by mapping a point in the
    image specified by `overlay_xy` to a point on the screen specified by `screen_xy`.
    Then the image is rotated by `rotation` degrees about a point relative to the screen
    specified by `rotation_xy`.

    Notes
    -----
    `icon` specifies the image to be used as the overlay. This file can be either on a
    local file system or on a web server. If `icon` is `None`, a rectangle is drawn using
    the color and size defined by the screen overlay.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#screenoverlay.

    Parameters
    ----------
    overlay_xy: OverlayXY
        Specifies a point on (or outside of) the overlay image that is mapped to the
        screen coordinate `screen_xy`. It requires `x` and `y` values, and the units for
        those values.
    screen_xy: ScreenXY
        Specifies a point relative to the screen origin that the overlay image is mapped
        to.
    rotation_xy: RotationXY
        Point relative to the screen about which the screen overlay is rotated.
    size: Size
        Specifies the size of the image for the screen overlay.
    rotation: float, default = 0
        Indicates the angle of rotation of the parent object. A value of 0 means no
        rotation. The value is an angle in degrees counterclockwise starting from north.
        Use ±180 to indicate the rotation of the parent object from 0. The center of the
        `rotation`, if not (.5,.5), is specified in `rotation_xy`.
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

    _kml_tag = "ScreenOverlay"
    _kml_fields = Overlay._kml_fields + (_FieldDef("rotation"),)
    _kml_children = Overlay._kml_children + (
        _ChildDef("overlay_xy"),
        _ChildDef("screen_xy"),
        _ChildDef("rotation_xy"),
        _ChildDef("size"),
    )

    def __init__(
        self,
        # ScreenOverlay parameters
        overlay_xy: OverlayXY | None = None,
        screen_xy: ScreenXY | None = None,
        rotation_xy: RotationXY | None = None,
        size: Size | None = None,
        rotation: float = 0,
        # Overlay parameters
        icon: str | Icon | None = None,
        draw_order: int | None = None,
        color: GeoColor | int | None = None,
        name: str | None = None,
        visibility: bool | None = None,
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
        """IconStyle instance constructor."""
        Overlay.__init__(
            self,
            icon=icon,
            draw_order=draw_order,
            color=color,
            name=name,
            visibility=visibility,
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
        ABC.__init__(self)
        self.overlay_xy = overlay_xy
        self.screen_xy = screen_xy
        self.rotation_xy = rotation_xy
        self.size = size
        self.rotation = rotation
