from typing import Optional

from lxml import etree

from pyLiveKML.KML.KML import ColorMode
from pyLiveKML.KML.KMLObjects.ColorStyle import ColorStyle


class PolyStyle(ColorStyle):
    """
    A KML 'PolyStyle', per https://developers.google.com/kml/documentation/kmlreference#polystyle.  Specifies
    various properties that define how a :class:`~pyLiveKML.KML.KMLObjects.Polygon` is drawn.

    :param Optional[int] color: The (optional) color, as a 32-bit ABGR value, that will be used to :attr:`fill` the
        polygon's area in GEP.
    :param Optional[ColorMode] color_mode: An (optional) :class:`~pyLiveKML.KML.KML.ColorMode` that determines how GEP
        chooses the polygon :attr:`fill` color.
    :param Optional[bool] fill: Optional flag to indicate whether GEP should fill in the polygon with a color.
    :param Optional[bool] outline: Optional flag to indicate whether GEP should draw the polygon's outline.
    """

    @property
    def kml_type(self) -> str:
        """Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set the KML tag name to
        'PolyStyle'"""
        return 'PolyStyle'

    @property
    def fill(self) -> bool:
        """True if the affected :class:`~pyLiveKML.KML.KMLObjects.Polygon` is to be filled in using the :attr:`color`
        property. False if it is not. None implies True.
        """
        return self._fill

    @fill.setter
    def fill(self, value: bool):
        if self._fill != value:
            self._fill = value
            self.field_changed()

    @property
    def outline(self) -> bool:
        """True if the outline of the :class:`~pyLiveKML.KML.KMLObjects.Polygon` is to be drawn using a separate
        :class:`~pyLiveKML.KML.KMLObjects.LineStyle`, specified in the :class:`~pyLiveKML.KML.KMLObjects.StyleSelector`
        that is the parent of this :class:`~pyLiveKML.KML.KMLObjects.PolyStyle` instance. False if it is not. None
        implies True.
        """
        return self._outline

    @outline.setter
    def outline(self, value: bool):
        if self._outline != value:
            self._outline = value
            self.field_changed()

    def build_kml(self, root: etree.Element, with_children=True):
        if self.color is not None:
            etree.SubElement(root, 'color').text = f'{self.color:08x}'
        if self.color_mode is not None:
            etree.SubElement(root, 'colorMode').text = self.color_mode.value
        if self._fill is not None:
            etree.SubElement(root, 'fill').text = str(int(self._fill))
        if self._outline is not None:
            etree.SubElement(root, 'outline').text = str(int(self._outline))

    def __init__(
            self,
            color: Optional[int] = None,
            color_mode: Optional[ColorMode] = None,
            fill: Optional[bool] = None,
            outline: Optional[bool] = None
    ):
        ColorStyle.__init__(self, color, color_mode)
        self._fill: Optional[bool] = fill
        self._outline: Optional[bool] = outline
