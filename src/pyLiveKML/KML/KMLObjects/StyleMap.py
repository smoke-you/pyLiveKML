from typing import Optional, Iterator

from lxml import etree

from pyLiveKML.KML.KMLObjects.Object import ObjectChild
from pyLiveKML.KML.KMLObjects.Style import Style
from pyLiveKML.KML.KMLObjects.StyleSelector import StyleSelector


class StyleMap(StyleSelector):
    """A KML 'StyleMap', per https://developers.google.com/kml/documentation/kmlreference#stylemap. Maps between two
    different :class:`~pyLiveKML.KML.KMLObjects.Style` objects for the :attr:`~pyLiveKML.KML.KML.StyleState.NORMAL` and
    :attr:`~pyLiveKML.KML.KML.StyleState.HIGHLIGHT` states of a :class:`~pyLiveKML.KML.KMLObjects.Feature` when it is
    displayed in GEP. The child :class:`~pyLiveKML.KML.KMLObjects.Style` objects may be referenced by URI, or in-line
    in the :class:`~pyLiveKML.KML.KMLObjects.StyleMap`.

    :param Optional[str] normal_style_url: An (optional) URI reference for a :class:`~pyLiveKML.KML.KMLObjects.Style`
        to be employed in :attr:`~pyLiveKML.KML.KML.StyleState.NORMAL` display mode.
    :param Optional[Style] normal_style: An (optional) inline :class:`~pyLiveKML.KML.KMLObjects.Style` to be employed
        in :attr:`~pyLiveKML.KML.KML.StyleState.NORMAL` display mode.
    :param Optional[str] highlight_style_url: An (optional) URI reference for a
        :class:`~pyLiveKML.KML.KMLObjects.Style` to be employed in :attr:`~pyLiveKML.KML.KML.StyleState.HIGHLIGHT`
        display mode.
    :param Optional[Style] highlight_style: An (optional) inline :class:`~pyLiveKML.KML.KMLObjects.Style` to be
        employed in :attr:`~pyLiveKML.KML.KML.StyleState.HIGHLIGHT` display mode.

    :note: It is both possible and reasonable to assign both a :attr:`styleUrl` and a
        :class:`~pyLiveKML.KML.KMLObjects.Style` to either or both of the :attr:`~pyLiveKML.KML.KML.StyleState.NORMAL`
        and :attr:`~pyLiveKML.KML.KML.StyleState.HIGHLIGHT` states. Per the rules discussed at
        https://developers.google.com/kml/documentation/kmlreference#feature, an inline
        :class:`~pyLiveKML.KML.KMLObjects.Style` will override a URI-referenced
        :class:`~pyLiveKML.KML.KMLObjects.Style`.
    """

    @property
    def kml_type(self) -> str:
        """Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set the KML tag name to
        'StyleMap'"""
        return 'StyleMap'

    @property
    def children(self) -> Iterator[ObjectChild]:
        """Overridden from :attr:`pyLiveKML.KML.KMLObjects.Object.Object.children` to yield the children of a
        :class:`~pyLiveKML.KML.KMLObjects.Style`, i.e. up to two :class:`~pyLiveKML.KML.KMLObjects.Style` instances.
        """
        if self._normal_style:
            yield ObjectChild(parent=self, child=self._normal_style)
        if self._highlight_style:
            yield ObjectChild(parent=self, child=self._highlight_style)

    @property
    def normal_style_url(self) -> Optional[str]:
        """A URI that references the :class:`~pyLiveKML.KML.KMLObjects.Style` that will be employed when the target
        :class:`~pyLiveKML.KML.KMLObjects.Feature` is displayed in :attr:`~pyLiveKML.KML.KML.StyleState.NORMAL` mode.
        """
        return self._normal_style_url
    
    @normal_style_url.setter
    def normal_style_url(self, value: Optional[str]):
        if self._normal_style_url != value:
            self._normal_style_url = value
            self.field_changed()

    @property
    def normal_style(self) -> Optional[Style]:
        """An inline :class:`~pyLiveKML.KML.KMLObjects.Style` that will be employed when the target
        :class:`~pyLiveKML.KML.KMLObjects.Feature` is displayed in :attr:`~pyLiveKML.KML.KML.StyleState.NORMAL` mode.
        """
        return self._normal_style

    @normal_style.setter
    def normal_style(self, value: Optional[Style]):
        if self._normal_style != value:
            self._normal_style = value
            self.field_changed()

    @property
    def highlight_style_url(self) -> Optional[str]:
        """A URI that references the :class:`~pyLiveKML.KML.KMLObjects.Style` that will be employed when the target
        :class:`~pyLiveKML.KML.KMLObjects.Feature` is displayed in :attr:`~pyLiveKML.KML.KML.StyleState.HIGHLIGHT` mode.
        """
        return self._highlight_style_url

    @highlight_style_url.setter
    def highlight_style_url(self, value: Optional[str]):
        if self._highlight_style_url != value:
            self._highlight_style_url = value
            self.field_changed()

    @property
    def highlight_style(self) -> Optional[Style]:
        """An inline :class:`~pyLiveKML.KML.KMLObjects.Style` that will be employed when the target
        :class:`~pyLiveKML.KML.KMLObjects.Feature` is displayed in :attr:`~pyLiveKML.KML.KML.StyleState.HIGHLIGHT` mode.
        """
        return self._highlight_style

    @highlight_style.setter
    def highlight_style(self, value: Optional[Style]):
        if self._highlight_style != value:
            self._highlight_style = value
            self.field_changed()

    def build_kml(self, root: etree.Element, with_children=True):
        if with_children:
            if self._normal_style_url or self._normal_style:
                normal = etree.SubElement(root, 'Pair')
                etree.SubElement(normal, 'key').text = 'normal'
                if self._normal_style:
                    normal.append(self._normal_style.construct_kml())
                if self._normal_style_url:
                    etree.SubElement(normal, 'styleUrl').text = self._normal_style_url
            if self._highlight_style_url or self._highlight_style:
                highlight = etree.SubElement(root, 'Pair')
                etree.SubElement(highlight, 'key').text = 'highlight'
                if self._highlight_style:
                    highlight.append(self._highlight_style.construct_kml())
                if self._highlight_style_url:
                    etree.SubElement(highlight, 'styleUrl').text = self._highlight_style_url

    def __init__(
            self,
            normal_style_url: Optional[str] = None,
            normal_style: Optional[Style] = None,
            highlight_style_url: Optional[str] = None,
            highlight_style: Optional[Style] = None,
    ):
        super().__init__()
        self._normal_style_url = normal_style_url
        self._normal_style = normal_style
        self._highlight_style_url = highlight_style_url
        self._highlight_style = highlight_style
            