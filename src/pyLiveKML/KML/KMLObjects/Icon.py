from typing import Optional, NamedTuple

from lxml import etree  # type: ignore

from ..KML import RefreshMode
from .Link import Link


GxParams = NamedTuple("GxParams", [("x", int), ("y", int), ("w", int), ("h", int)])


class Icon(Link):
    """A KML 'Icon', per https://developers.google.com/kml/documentation/kmlreference#icon.
    :class:`~pyLiveKML.KML.KMLObjects.Icon` instances are used to specify an image file that will be displayed in a GEP
    overlay.  Note that only time-based refresh of :class:`~pyLiveKML.KML.KMLObjects.Icon` instances is currently
    supported by pyLiveKML.

    :param Optional[str] href: An (optional) href for the file that is referenced by the
        :class:`~pyLiveKML.KML.KMLObjects.Icon`.
    :param Optional[RefreshMode] refresh_mode: The (optional) :class:`~pyLiveKML.KML.KML.RefreshMode` that will be used
        for file loading.
    :param Optional[float] refresh_interval: The (optional) refresh interval, in seconds, that will be used for file
        loading.
    :param Optional[GxParams] gx_params: Optional :class:`GxParams` instance that defines how GEP will treat the icon
        image.
    """

    def __init__(
        self,
        href: Optional[str] = None,
        refresh_mode: Optional[RefreshMode] = None,
        refresh_interval: Optional[float] = None,  # 4.0
        gx_params: Optional[GxParams] = None,  # GxParams(0, 0, -1, -1)
    ):
        Link.__init__(
            self,
            href=href,
            refresh_mode=refresh_mode,
            refresh_interval=refresh_interval,
        )
        self._gx_params: Optional[GxParams] = gx_params

    @property
    def kml_type(self) -> str:
        """Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set the KML tag name to
        'Icon'"""
        return "Icon"

    @property
    def gx_params(self) -> Optional[GxParams]:
        """A :class:`GxParams` named tuple that describes how the icon is treated by GEP."""
        return self._gx_params

    @gx_params.setter
    def gx_params(self, value: Optional[GxParams]) -> None:
        self._gx_params = value
        self.field_changed()

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        if self._href:
            etree.SubElement(root, "href").text = self._href
        if self._gx_params:
            if self._gx_params.x != 0:
                etree.SubElement(root, "gx:x").text = str(self._gx_params.x)
            if self._gx_params.y != 0:
                etree.SubElement(root, "gx:y").text = str(self._gx_params.y)
            if self._gx_params.w != -1:
                etree.SubElement(root, "gx:w").text = str(self._gx_params.w)
            if self._gx_params.h != -1:
                etree.SubElement(root, "gx:h").text = str(self._gx_params.h)
        if self._refresh_mode is not None:
            etree.SubElement(root, "refreshMode").text = self._refresh_mode.value
        if self._refresh_interval is not None:
            etree.SubElement(root, "refreshInterval").text = (
                f"{self._refresh_interval:0.1f}"
            )
        # if self.view_refresh_mode is not None:
        #     etree.SubElement(root, 'viewRefreshMode').text = self.view_refresh_mode.value
        # if self.view_refresh_time is not None:
        #     etree.SubElement(root, 'viewRefreshTime').text = f'{self.view_refresh_time:0.1f}'
        # if self.view_bound_scale is not None:
        #     etree.SubElement(root, 'viewBoundScale').text = f'{self.view_bound_scale:0.1f}'
        # # TODO: view format is not being handled at all, may need to be corrected
        # if self.view_format is not None:
        #     etree.SubElement(root, 'viewFormat').text = self.view_format
        # if self.http_query:
        #     etree.SubElement(root, 'httpQuery').text = self.http_query
