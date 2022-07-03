from typing import Optional

from lxml import etree

from pyLiveKML.KML.KML import ColorMode
from pyLiveKML.KML.KMLObjects.ColorStyle import ColorStyle


class LabelStyle(ColorStyle):
    """
    A KML 'LabelStyle', per https://developers.google.com/kml/documentation/kmlreference#iconstyle.  Specifies
    various properties that define how the name of a :class:`~pyLiveKML.KML.KMLObjects.Feature` is drawn in GEP.

    :param Optional[float] scale: The (optional) relative scale of the text.
    :param Optional[int] color: The (optional) color of the text, as a 32-bit ABGR value.
    :param Optional[ColorMode] color_mode: The (optional) :class:`~pyLiveKML.KML.KML.ColorMode` used to color the text;
        either 'NORMAL' or 'RANDOM'.
    """

    @property
    def kml_type(self) -> str:
        """Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set the KML tag name to
        'LabelStyle'"""
        return 'LabelStyle'

    @property
    def scale(self) -> Optional[float]:
        """Relative scale of the text.
        """
        return self._scale

    @scale.setter
    def scale(self, value: Optional[float]):
        if self._scale != value:
            self._scale = value
            self.field_changed()

    def build_kml(self, root: etree.Element, with_children=True):
        if self.color is not None:
            etree.SubElement(root, 'color').text = f'{self.color:08x}'
        if self.color_mode is not None:
            etree.SubElement(root, 'colorMode').text = self.color_mode.value
        if self.scale is not None:
            etree.SubElement(root, 'scale').text = f'{self.scale:0.3f}'

    def __init__(
            self,
            scale: Optional[float] = None,
            color: Optional[int] = None,
            color_mode: Optional[ColorMode] = None,
    ):
        ColorStyle.__init__(self, color=color, color_mode=color_mode)
        self._scale = scale

    def __str__(self):
        return f'{self.kml_type}'

    def __repr__(self):
        return self.__str__()
