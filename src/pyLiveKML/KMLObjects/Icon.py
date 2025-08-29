"""Icon module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML import RefreshModeEnum, ViewRefreshModeEnum
from pyLiveKML.KML._BaseObject import _FieldDef
from pyLiveKML.KMLObjects.Link import Link


class Icon(Link):
    """A KML 'Icon', per https://developers.google.com/kml/documentation/kmlreference#icon.

    :class:`~pyLiveKML.KMLObjects.Icon` instances are used to specify an image file that will be displayed in a GEP
    overlay.  Note that only time-based refresh of :class:`~pyLiveKML.KMLObjects.Icon` instances is currently
    supported by pyLiveKML.

    :param str|None href: An (optional) href for the file that is referenced by the
        :class:`~pyLiveKML.KMLObjects.Icon`.
    :param RefreshMode|None refresh_mode: The (optional) :class:`~pyLiveKML.KML.KML.RefreshMode` that will be used
        for file loading.
    :param float|None refresh_interval: The (optional) refresh interval, in seconds, that will be used for file
        loading.
    :param ViewRefreshMode|Node view_refresh_mode: The (optional) view refresh mode.
    :param float|None view_refresh_time: The (optional) view refresh time in seconds.
    :param float|None view_bound_scale: The (optional) scaling of the view bounds.
    :param str|None view_format: An (optional) string to describe how the view should be formatted.
    :param str|None http_query: An (optional) set of parameters for the href.
    :param GxParams|None gx_params: Optional :class:`GxParams` instance that defines how GEP will treat the icon
        image.
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
