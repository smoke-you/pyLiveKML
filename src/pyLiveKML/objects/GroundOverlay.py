"""GroundOverlay module."""

from abc import ABC
from typing import Any, Iterable

from lxml import etree  # type: ignore

from pyLiveKML.objects.AbstractView import AbstractView
from pyLiveKML.objects.Object import (
    _BaseObject,
    _ChildDef,
    _FieldDef,
    _KMLDump,
    _KMLParser,
    Angle180,
    Angle90,
    Object,
)
from pyLiveKML.objects.Overlay import Overlay
from pyLiveKML.objects.Region import Region
from pyLiveKML.objects.StyleSelector import StyleSelector
from pyLiveKML.objects.TimePrimitive import TimePrimitive
from pyLiveKML.types.GeoColor import GeoColor


class LatLonBox(Object):
    """A `<LatLonBox>` KML tag constructor.

    Specific to the `<GroundOverlay>` KML tag. Specifies where the top, bottom, right,
    and left sides of a bounding box for the ground overlay are aligned.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-groundoverlay

    Parameters
    ----------
    north : float
        Specifies the latitude of the north edge of the bounding box, in decimal degrees
        from 0 to ±90.
    south : float
        Specifies the latitude of the south edge of the bounding box, in decimal degrees
        from 0 to ±90.
    east : float
        Specifies the longitude of the east edge of the bounding box, in decimal degrees
        from 0 to ±180. (For overlays that overlap the meridian of 180° longitude, values
        can extend beyond that range.)
    west : float
        Specifies the longitude of the west edge of the bounding box, in decimal degrees
        from 0 to ±180. (For overlays that overlap the meridian of 180° longitude, values
        can extend beyond that range.)
    rotation : float, default = 0
        Specifies a rotation of the overlay about its center, in degrees. Values can be
        ±180. The default is 0 (north). Rotations are specified in a counterclockwise
        direction.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "LatLonBox"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("north", parser=Angle90),
        _FieldDef("south", parser=Angle90),
        _FieldDef("east", parser=Angle180),
        _FieldDef("west", parser=Angle180),
        _FieldDef("rotation", parser=Angle180),
    )
    _suppress_id = True

    def __init__(
        self,
        north: float,
        south: float,
        east: float,
        west: float,
        rotation: float = 0,
    ) -> None:
        """LatLonBox instance constructor."""
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.rotation = rotation


class _QuadParser(_KMLParser):
    """Custom parser for LatLonQuad coordinates field."""

    @classmethod
    def parse(cls, value: Any) -> Any:
        return (
            (Angle180.parse(value[0][0]), Angle90.parse(value[0][1])),
            (Angle180.parse(value[1][0]), Angle90.parse(value[1][1])),
            (Angle180.parse(value[2][0]), Angle90.parse(value[2][1])),
            (Angle180.parse(value[3][0]), Angle90.parse(value[3][1])),
        )


class _QuadDump(_KMLDump):
    """Custom dumper for LatLonQuad coordinates field."""

    @classmethod
    def dump(cls, value: Any) -> Any:
        return " ".join((",".join(map(str, x)) for x in value))


class LatLonQuad(Object):
    """A `<LatLonQuad>` KML tag constructor.

    Specific to the `<GroundOverlay>` KML tag. Allows nonrectangular quadrilateral ground
    overlays.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#gx:latlonquad

    Parameters
    ----------
    coordinates : tuple[tuple[float, float], tuple[float, float], tuple[float, float], tuple[float, float]]
        Specifies the coordinates of the four corner points of a quadrilateral defining
        the overlay area. Exactly four coordinate tuples have to be provided, each
        consisting of floating point values for longitude and latitude. Insert a space
        between tuples. Do not include spaces within a tuple. The coordinates must be
        specified in counter-clockwise order with the first coordinate corresponding to
        the lower-left corner of the overlayed image. The shape described by these
        corners must be convex.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "gx:LatLonQuad"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("coordinates", parser=_QuadParser, dumper=_QuadDump),
    )
    _suppress_id = True

    def __init__(
        self,
        coordinates: tuple[
            tuple[float, float],
            tuple[float, float],
            tuple[float, float],
            tuple[float, float],
        ],
    ) -> None:
        """LatLonQuad instance constructor."""
        self.coordinates = coordinates


class GroundOverlay(Overlay):
    """A KML `<GroundOverlay>` tag constructor.

    This element draws an image overlay draped onto the terrain. The `<href>` child of
    `<Icon>` specifies the image to be used as the overlay. This file can be either on
    a local file system or on a web server. If this element is omitted or contains no
    `<href>`, a rectangle is drawn using the color and `<LatLonBox>` bounds defined by
    the ground overlay.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#groundoverlay

    Parameters
    ----------
    quad : LatLonQuad | None, default = None
        A non-rectilinear bounding box definition
    box : LatLonBox | None, default = None
        A rectilinear bounding box definition
    icon : str | None, default = None
        The href of the icon
    draw_order : int | None, default = None
        Defines the stacking order for the images in overlapping overlays. Overlays with
        higher `draw_order` values are drawn on top of overlays with lower `draw_order`
        values.
    color : GeoColor | int | None, default = None
        The color of the overlay.
    name : str|None, default = None
        User-defined text displayed in the 3D viewer as the label for the object.
    visibility : bool | None, default = None
        Specifies whether the `Feature` is drawn in the 3D viewer when it is initially
        loaded. In order for a `Feature` to be visible, the `<visibility>` tag of all
        its ancestors must also be set `True`.
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

    Attributes
    ----------
    Same as parameters

    """

    _kml_tag = "GroundOverlay"
    _kml_fields = Overlay._kml_fields + (
        _FieldDef("altitude"),
        _FieldDef("altitude_mode", "gx:altitudeMode"),
    )
    _kml_children = Overlay._kml_children + (
        _ChildDef("box"),
        _ChildDef("quad"),
    )

    def __init__(
        self,
        # GroundOverlay parameters
        quad: LatLonQuad | None = None,
        box: LatLonBox | None = None,
        # Overlay parameters
        icon: str | None = None,
        draw_order: int | None = None,
        color: GeoColor | int | None = None,
        # Feature parameters
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
        )
        ABC.__init__(self)
        self.quad = quad
        self.box = box
