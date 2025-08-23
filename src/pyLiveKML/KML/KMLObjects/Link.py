"""Link module."""

from typing import Any
from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import RefreshMode, ViewRefreshMode
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

    _kml_type = "Link"

    def __init__(
        self,
        href: str | None = None,
        refresh_mode: RefreshMode | None = None,
        refresh_interval: float | None = None,
        view_refresh_mode: ViewRefreshMode | None = None,
        view_refresh_time: float | None = None,
        view_bound_scale: float | None = None,
        view_format: str | None = None,
        http_query: str | None = None,
    ):
        """Link instance constructor."""
        Object.__init__(self)
        self._href: str | None = href
        self._refresh_mode: RefreshMode | None = refresh_mode
        self._refresh_interval: float | None = refresh_interval
        self._view_refresh_mode: ViewRefreshMode | None = view_refresh_mode
        self._view_refresh_time: float | None = view_refresh_time
        self._view_bound_scale: float | None = view_bound_scale
        self._view_format: str | None = view_format
        self._http_query: str | None = http_query

    # def __setattr__(self, name: str, value: Any) -> None:
    #     if name not in ("href", "refresh_mode", "refresh_interval", "view_refresh_mode", "view_refresh_time", "view_bound_scale", "view_format", "http_query"):
    #         super().__setattr__(name, value)
    #     else:
    #         if getattr(self, name) != value:
    #             super().__setattr__(name, value)
    #             self.field_changed()

    @property
    def href(self) -> str | None:
        """A URI that specifies the location of the resource that is linked to."""
        return self._href

    @href.setter
    def href(self, value: str | None) -> None:
        if self._href != value:
            self._href = value
            self.field_changed()

    @property
    def refresh_mode(self) -> RefreshMode | None:
        """The refresh mode of the instance.

        The :class:`~pyLiveKML.KML.KML.RefreshMode` that controls when the file specified by the 'href' property is
        retrieved.
        """
        return self._refresh_mode

    @refresh_mode.setter
    def refresh_mode(self, value: RefreshMode | None) -> None:
        if self._refresh_mode != value:
            self._refresh_mode = value
            self.field_changed()

    @property
    def refresh_interval(self) -> float | None:
        """The refresh interval of the instance.

        The refresh interval, in seconds, that will be used if the :attr:`refresh_mode`
        property is set to :attr:`~pyLiveKML.KML.KML.RefreshMode.ON_INTERVAL`.
        """
        return self._refresh_interval

    @refresh_interval.setter
    def refresh_interval(self, value: float | None) -> None:
        if self._refresh_interval != value:
            self._refresh_interval = value
            self.field_changed()

    @property
    def view_refresh_mode(self) -> ViewRefreshMode | None:
        """Specifies how the link is refreshed when the "camera" changes."""
        return self._view_refresh_mode

    @view_refresh_mode.setter
    def view_refresh_mode(self, value: ViewRefreshMode | None) -> None:
        if value != self._view_refresh_mode:
            self._view_refresh_mode = value
            self.field_changed()

    @property
    def view_refresh_time(self) -> float | None:
        """After camera movement stops, specifies the number of seconds to wait before refreshing the view."""
        return self._view_refresh_time

    @view_refresh_time.setter
    def view_refresh_time(self, value: float | None) -> None:
        if value != self._view_refresh_time:
            self._view_refresh_time = value
            self.field_changed()

    @property
    def view_bound_scale(self) -> float | None:
        """Scales the BBOX parameters before sending them to the server.

        A value less than 1 specifies to use less than the full view (screen).
        A value greater than 1 specifies to fetch an area that extends beyond the edges
        of the current view.
        """
        return self._view_bound_scale

    @view_bound_scale.setter
    def view_bound_scale(self, value: float | None) -> None:
        if value != self._view_bound_scale:
            self._view_bound_scale = value
            self.field_changed()

    @property
    def view_format(self) -> str | None:
        """Specifies the format of the query string that is appended to the Link's <href> before the file is fetched.

        If the <href> specifies a local file, this element is ignored.
        """
        return self._view_format

    @view_format.setter
    def view_format(self, value: str | None) -> None:
        if value != self._view_format:
            self._view_format = value
            self.field_changed()

    @property
    def http_query(self) -> str | None:
        """Appends information to the query string, based on the parameters specified.

        Google Earth substitutes the appropriate current value at the time it creates
        the query string. The following parameters are supported:

            * [clientVersion]
            * [kmlVersion]
            * [clientName]
            * [language]
        """
        return self._http_query

    @http_query.setter
    def http_query(self, value: str | None) -> None:
        if value != self._http_query:
            self._http_query = value
            self.field_changed()

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        if self._href:
            etree.SubElement(root, "href").text = self._href
        if self._refresh_mode is not None:
            etree.SubElement(root, "refreshMode").text = self._refresh_mode.value
        if self._refresh_interval is not None:
            etree.SubElement(root, "refreshInterval").text = (
                f"{self._refresh_interval:0.3f}"
            )
        if self._view_refresh_mode is not None:
            etree.SubElement(root, "viewRefreshMode").text = (
                self._view_refresh_mode.value
            )
        if self._view_refresh_time is not None:
            etree.SubElement(root, "viewRefreshTime").text = (
                f"{self._view_refresh_time:0.3f}"
            )
        if self._view_bound_scale is not None:
            etree.SubElement(root, "viewBoundScale").text = (
                f"{self._view_bound_scale:0.3f}"
            )
        if self._view_format is not None:
            etree.SubElement(root, "viewFormat").text = self._view_format
        if self._http_query:
            etree.SubElement(root, "httpQuery").text = self._http_query
