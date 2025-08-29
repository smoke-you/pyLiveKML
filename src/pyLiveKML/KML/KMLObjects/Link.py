"""Link module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML import RefreshModeEnum, ViewRefreshModeEnum
from pyLiveKML.KML._BaseObject import _FieldDef, NoParse, DumpDirect
from pyLiveKML.KML.KMLObjects.Object import Object


class Link(Object):
    """A KML 'Link', per https://developers.google.com/kml/documentation/kmlreference#link.

    :class:`~pyLiveKML.KML.KMLObjects.Link` objects are used to specify a KML file to be fetched with a
    :class:`~pyLiveKML.KML.KMLObjects.NetworkLink`; or an image file to be used in a GEP overlay, using the
    :class:`~pyLiveKML.KML.KMLObjects.Icon` class that inherits from :class:`~pyLiveKML.KML.KMLObjects.Link`.  The KML
    specification also uses :class:`~pyLiveKML.KML.KMLObjects.Link` objects to specify the location of Models, but
    Models are not currently implemented in pyLiveKML.

    :note: Only time-based refresh is currently supported by pyLiveKML.

    :param str|None href: An (optional) href for the file that is referenced by the
        :class:`~pyLiveKML.KML.KMLObjects.Link`.
    :param RefreshMode|None refresh_mode: The (optional) refresh mode that will be used for file loading.
    :param float|None refresh_interval: The (optional) refresh interval, in seconds, that will be used for file
        loading.
    :param ViewRefreshMode|Node view_refresh_mode: The (optional) view refresh mode.
    :param float|None view_refresh_time: The (optional) view refresh time in seconds.
    :param float|None view_bound_scale: The (optional) scaling of the view bounds.
    :param str|None view_format: An (optional) string to describe how the view should be formatted.
    :param str|None http_query: An (optional) set of parameters for the href.
    """

    _kml_tag = "Link"
    _kml_fields = Object._kml_fields + (
        _FieldDef("href", NoParse, "href", DumpDirect),
        _FieldDef("refresh_mode", NoParse, "refreshMode", DumpDirect),
        _FieldDef("refresh_interval", NoParse, "refreshInterval", DumpDirect),
        _FieldDef("view_refresh_mode", NoParse, "viewRefreshMode", DumpDirect),
        _FieldDef("view_refresh_time", NoParse, "viewRefreshTime", DumpDirect),
        _FieldDef("view_bound_scale", NoParse, "viewBoundScale", DumpDirect),
        _FieldDef("view_format", NoParse, "viewFormat", DumpDirect),
        _FieldDef("http_query", NoParse, "httpQuery", DumpDirect),
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
