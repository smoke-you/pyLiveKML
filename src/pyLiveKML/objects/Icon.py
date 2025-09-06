"""Icon module."""

from lxml import etree  # type: ignore

from pyLiveKML.types import RefreshModeEnum, ViewRefreshModeEnum
from pyLiveKML.objects.Object import _FieldDef
from pyLiveKML.objects.Link import Link


class Icon(Link):
    """A KML `<Icon>` tag constructor.

    Defines an image associated with an `IconStyle` or `Overlay`. The `href` attribute
    defines the location of the image to be used as the overlay or as the icon for the
    placemark. This location can either be on a local file system or a remote web server.
    The `x`, `y`, `w`, and `h` attributes are used to select one icon from an image that
    contains multiple icons (often referred to as an icon palette).

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#icon

    Parameters
    ----------
    href: str | None, default = None
        An HTTP address or a local file specification used to load an icon.
    refresh_mode: RefreshModeEnum | None, default = None,
        Specifies a time-based refresh mode.
    refresh_interval: float | None, default = None
        Indicates to refresh the file every n seconds.
    view_refresh_mode: ViewRefreshModeEnum, default | None = None
        Specifies how the link is refreshed when the "camera" changes.
    view_refresh_time: float | None, default = None
        After camera movement stops, specifies the number of seconds to wait before
        refreshing the view.
    view_bound_scale: float | None, default = None
        Scales the BBOX parameters before sending them to the server. A value less than 1
        specifies to use less than the full view (screen). A value greater than 1
        specifies to fetch an area that extends beyond the edges of the current view.
    view_format: str | None, default = None
        Specifies the format of the query string that is appended to `href` before the
        file is fetched.
    http_query: str | None, default = None
        Appends information to the query string, based on the parameters specified.
        (Google Earth substitutes the appropriate current value at the time it creates
        the query string.) The following parameters are supported:
        * [clientVersion]
        * [kmlVersion]
        * [clientName]
        * [language]
    x: int, default = 0
        If `href` specifies an icon palette, `x` and `y` identify the offsets, in
        pixels, from the lower-left corner of the icon palette. If no values are
        specified for `x` and `y`, the lower left corner of the icon palette is assumed
        to be the lower-left corner of the icon to use.
    y: int, default = 0
        If `href` specifies an icon palette, `x` and `y` identify the offsets, in
        pixels, from the lower-left corner of the icon palette. If no values are
        specified for `x` and `y`, the lower left corner of the icon palette is assumed
        to be the lower-left corner of the icon to use.
    w: int, default = -1
        If `href` specifies an icon palette, `w` and `h` specify the width and height, in
        pixels, of the icon to use.
    h: int, default = -1
        If `href` specifies an icon palette, `w` and `h` specify the width and height, in
        pixels, of the icon to use.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "Icon"
    _kml_fields = Link._kml_fields + (
        _FieldDef("x", "gx:x"),
        _FieldDef("y", "gx:y"),
        _FieldDef("w", "gx:w"),
        _FieldDef("h", "gx:h"),
    )

    def __init__(
        self,
        href: str | None = None,
        refresh_mode: RefreshModeEnum | None = None,
        refresh_interval: float | None = None,  # 4.0
        view_refresh_mode: ViewRefreshModeEnum | None = None,
        view_refresh_time: float | None = None,
        view_bound_scale: float | None = None,
        view_format: str | None = None,
        http_query: str | None = None,
        x: int = 0,
        y: int = 0,
        w: int = -1,
        h: int = -1,
    ):
        """Icon instance constructor."""
        Link.__init__(
            self,
            href=href,
            refresh_mode=refresh_mode,
            refresh_interval=refresh_interval,
            view_refresh_mode=view_refresh_mode,
            view_refresh_time=view_refresh_time,
            view_bound_scale=view_bound_scale,
            view_format=view_format,
            http_query=http_query,
        )
        self.x = x
        self.y = y
        self.w = w
        self.h = h
