from typing import Optional

from lxml import etree

from ..KML import ColorMode
from .ColorStyle import ColorStyle
from ..Vec2 import Vec2


class IconStyle(ColorStyle):
    """
    A KML 'IconStyle', per https://developers.google.com/kml/documentation/kmlreference#iconstyle.  Specifies
    various properties that define how a :class:`~pyLiveKML.KML.KMLObjects.Icon` is drawn.  Applies to
    :class:`~pyLiveKML.KML.KMLObjects.Point` geometries.

    :param str icon: A URI for an image or icon file.
    :param float scale: The (optional) relative scale of the icon.
    :param float heading: The (optional) heading, in degrees, that the icon will be rotated to point towards.
    :param Optional[int] color: The (optional) color of the icon, as a 32-bit ABGR value.
    :param Optional[ColorMode] color_mode: The (optional) :class:`~pyLiveKML.KML.KML.ColorMode` used to color the icon;
        either 'NORMAL' or 'RANDOM'.
    """

    @property
    def kml_type(self) -> str:
        """Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set the KML tag name to
        'IconStyle'"""
        return 'IconStyle'

    @property
    def icon(self) -> Optional[str]:
        """URI for the image that will be displayed in GEP as the icon.
        """
        return self._icon

    @icon.setter
    def icon(self, value: Optional[str]):
        if self._icon != value:
            self._icon = value
            self.field_changed()

    @property
    def scale(self) -> Optional[float]:
        """Relative scale at which the icon will be displayed in GEP.
        """
        return self._scale

    @scale.setter
    def scale(self, value: Optional[float]):
        if self._scale != value:
            self._scale = value
            self.field_changed()

    @property
    def heading(self) -> Optional[float]:
        """Heading (in degrees) that the icon will be displayed pointing towards in GEP.
        """
        return self._heading

    @heading.setter
    def heading(self, value: Optional[float]):
        if self._heading != value:
            self._heading = value
            self.field_changed()

    @property
    def hotspot(self) -> Optional[Vec2]:
        """Relative position in the icon that is anchored to the associated :class:`~pyLiveKML.KML.KMLObjects.Point`
        """
        return self._hotspot

    @hotspot.setter
    def hotspot(self, value: Optional[Vec2]):
        value.name = 'hotSpot'
        if self._hotspot != value:
            self._hotspot = value
            self.field_changed()

    def build_kml(self, root: etree.Element, with_children=True):
        if self.color is not None:
            etree.SubElement(root, 'color').text = f'{self.color:08x}'
        if self.color_mode is not None:
            etree.SubElement(root, 'colorMode').text = self.color_mode.value
        if self.scale is not None:
            etree.SubElement(root, 'scale').text = f'{self.scale:0.3f}'
        if self.heading is not None:
            etree.SubElement(root, 'heading').text = f'{self.heading:0.1f}'
        if self.icon is not None:
            etree.SubElement(etree.SubElement(root, 'Icon'), 'href').text = self.icon
        if self.hotspot is not None:
            root.append(self.hotspot.xml)

    def __init__(
            self,
            icon: str,
            scale: float = 1.0,
            heading: float = 0.0,
            color: Optional[int] = None,
            color_mode: Optional[ColorMode] = None,
    ):
        ColorStyle.__init__(self, color=color, color_mode=color_mode)
        self._scale = scale
        self._heading = heading
        self._icon = icon
        self._hotspot: Optional[Vec2] = None

    def __str__(self):
        return f'{self.kml_type}'

    def __repr__(self):
        return self.__str__()
