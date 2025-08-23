"""Icon module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import RefreshMode, ViewRefreshMode, GxParams
from pyLiveKML.KML.KMLObjects.Link import Link


class Icon(Link):
    """A KML 'Icon', per https://developers.google.com/kml/documentation/kmlreference#icon.

    :class:`~pyLiveKML.KML.KMLObjects.Icon` instances are used to specify an image file that will be displayed in a GEP
    overlay.  Note that only time-based refresh of :class:`~pyLiveKML.KML.KMLObjects.Icon` instances is currently
    supported by pyLiveKML.

    :param str|None href: An (optional) href for the file that is referenced by the
        :class:`~pyLiveKML.KML.KMLObjects.Icon`.
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

    _kml_type = "Icon"

    def __init__(
        self,
        href: str | None = None,
        refresh_mode: RefreshMode | None = None,
        refresh_interval: float | None = None,  # 4.0
        view_refresh_mode: ViewRefreshMode | None = None,
        view_refresh_time: float | None = None,
        view_bound_scale: float | None = None,
        view_format: str | None = None,
        http_query: str | None = None,
        gx_params: GxParams | None = None,  # GxParams(0, 0, -1, -1)
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
        self._gx_params: GxParams | None = gx_params

    @property
    def gx_params(self) -> GxParams | None:
        """A :class:`GxParams` named tuple that describes how the icon is treated by GEP."""
        return self._gx_params

    @gx_params.setter
    def gx_params(self, value: GxParams | None) -> None:
        self._gx_params = value
        self.field_changed()

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        if self._gx_params:
            if self._gx_params.x != 0:
                etree.SubElement(root, "gx:x").text = str(self._gx_params.x)
            if self._gx_params.y != 0:
                etree.SubElement(root, "gx:y").text = str(self._gx_params.y)
            if self._gx_params.w != -1:
                etree.SubElement(root, "gx:w").text = str(self._gx_params.w)
            if self._gx_params.h != -1:
                etree.SubElement(root, "gx:h").text = str(self._gx_params.h)
