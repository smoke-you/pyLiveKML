from typing import Optional

from lxml import etree

from pyLiveKML.KML.KML import RefreshMode
from pyLiveKML.KML.KMLObjects.Object import Object


class Link(Object):
    """A KML 'Link', per https://developers.google.com/kml/documentation/kmlreference#link.
    :class:`~pyLiveKML.KML.KMLObjects.Link` objects are used to specify a KML file to be fetched with a
    :class:`~pyLiveKML.KML.KMLObjects.NetworkLink`; or an image file to be used in a GEP overlay, using the
    :class:`~pyLiveKML.KML.KMLObjects.Icon` class that inherits from :class:`~pyLiveKML.KML.KMLObjects.Link`.  The KML
    specification also uses :class:`~pyLiveKML.KML.KMLObjects.Link` objects to specify the location of Models, but
    Models are not currently implemented in pyLiveKML.

    :note: Only time-based refresh is currently supported by pyLiveKML.

    :param Optional[str] href: An (optional) href for the file that is referenced by the
        :class:`~pyLiveKML.KML.KMLObjects.Link`.
    :param Optional[RefreshMode] refresh_mode: The (optional) refresh mode that will be used for file loading.
    :param Optional[float] refresh_interval: The (optional) refresh interval, in seconds, that will be used for file
        loading.
    """
    @property
    def kml_type(self) -> str:
        """Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set the KML tag name to
        'Link'"""
        return 'Link'

    @property
    def href(self) -> Optional[str]:
        """A URI that specifies the location of the resource that is linked to.
        """
        return self._href

    @href.setter
    def href(self, value: Optional[str]):
        if self._href != value:
            self._href = value
            self.field_changed()

    @property
    def refresh_mode(self) -> Optional[RefreshMode]:
        """The :class:`~pyLiveKML.KML.KML.RefreshMode` that controls when the file specified by the 'href' property is
        retrieved.
        """
        return self._refresh_mode

    @refresh_mode.setter
    def refresh_mode(self, value: Optional[RefreshMode]):
        if self._refresh_mode != value:
            self._refresh_mode = value
            self.field_changed()

    @property
    def refresh_interval(self) -> Optional[float]:
        """The refresh interval, in seconds, that will be used if the :attr:`refresh_mode` property is set to
        :attr:`~pyLiveKML.KML.KML.RefreshMode.ON_INTERVAL`.
        """
        return self._refresh_interval

    @refresh_interval.setter
    def refresh_interval(self, value: Optional[float]):
        if self._refresh_interval != value:
            self._refresh_interval = value
            self.field_changed()

    def build_kml(self, root: etree.Element, with_children=True):
        if self._href:
            etree.SubElement(root, 'href').text = self._href
        if self._refresh_mode is not None:
            etree.SubElement(root, 'refreshMode').text = self._refresh_mode.value
        if self._refresh_interval is not None:
            etree.SubElement(root, 'refreshInterval').text = f'{self._refresh_interval:0.3f}'
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

    def __init__(
            self,
            href: Optional[str] = None,
            refresh_mode: Optional[RefreshMode] = None,
            refresh_interval: Optional[float] = None,
    ):
        Object.__init__(self)
        self._href = href
        self._refresh_mode = refresh_mode
        self._refresh_interval = refresh_interval
        # self.view_refresh_mode: Optional[ViewRefreshMode] = None
        # self.view_refresh_time: Optional[float] = None
        # self.view_bound_scale: Optional[float] = None
        # self.view_format: Optional[str] = None
        # self.http_query: Optional[str] = None
