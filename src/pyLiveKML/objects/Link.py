"""Link module."""

from lxml import etree  # type: ignore

from pyLiveKML.types import RefreshModeEnum, ViewRefreshModeEnum
from pyLiveKML.objects.Object import _FieldDef, Object


class Link(Object):
    """A KML `<Link>` tag constructor.

    Specifies the location of any of the following:
    * KML files fetched by network links.
    * Image files used in any `Overlay`.
    * Model files used in `Model`.

    The file is conditionally loaded and refreshed, depending on the refresh parameters
    supplied here. Two different sets of refresh parameters can be specified: one set is
    based on time (`refresh_mode` and `refresh_interval`) and one is based on the current
    "camera" view (`view_refresh_mode` and `view_refresh_time`). In addition, `Link`
    specifies whether to scale the bounding box parameters that are sent to the server
    (`view_bound_scale`) and provides a set of optional viewing parameters that can be
    sent to the server (`view_format`) as well as a set of optional parameters containing
    version and language information.

    When a file is fetched, the URL that is sent to the server is composed of three
    pieces of information:

    * The href that specifies the file to load.
    * An arbitrary format string that is created from:
        * parameters that you specify in the `view_format` attribute, or
        * bounding box parameters (this is the default and is used if no `view_format`
        attribute is set)
    * A second format string that is specified in the `http_query` attribute.

    If the file specified in `href` is a local file, the `view_format` and `http_query`
    attributes are not used.

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

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "Link"
    _kml_fields = Object._kml_fields + (
        _FieldDef("href"),
        _FieldDef("refresh_mode", "refreshMode"),
        _FieldDef("refresh_interval", "refreshInterval"),
        _FieldDef("view_refresh_mode", "viewRefreshMode"),
        _FieldDef("view_refresh_time", "viewRefreshTime"),
        _FieldDef("view_bound_scale", "viewBoundScale"),
        _FieldDef("view_format", "viewFormat"),
        _FieldDef("http_query", "httpQuery"),
    )

    def __init__(
        self,
        href: str | None = None,
        refresh_mode: RefreshModeEnum | None = None,
        refresh_interval: float | None = None,
        view_refresh_mode: ViewRefreshModeEnum | None = None,
        view_refresh_time: float | None = None,
        view_bound_scale: float | None = None,
        view_format: str | None = None,
        http_query: str | None = None,
    ):
        """Link instance constructor."""
        Object.__init__(self)
        self.href = href
        self.refresh_mode = refresh_mode
        self.refresh_interval = refresh_interval
        self.view_refresh_mode = view_refresh_mode
        self.view_refresh_time = view_refresh_time
        self.view_bound_scale = view_bound_scale
        self.view_format = view_format
        self.http_query = http_query
