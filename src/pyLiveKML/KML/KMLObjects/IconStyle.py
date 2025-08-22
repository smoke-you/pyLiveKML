from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import ColorMode
from pyLiveKML.KML.KMLObjects.ColorStyle import ColorStyle
from pyLiveKML.KML.Vec2 import Vec2


class IconStyle(ColorStyle):
    """
    A KML 'IconStyle', per https://developers.google.com/kml/documentation/kmlreference#iconstyle.  Specifies
    various properties that define how a :class:`~pyLiveKML.KML.KMLObjects.Icon` is drawn.  Applies to
    :class:`~pyLiveKML.KML.KMLObjects.Point` geometries.

    :param str icon: A URI for an image or icon file.
    :param float scale: The (optional) relative scale of the icon.
    :param float heading: The (optional) heading, in degrees, that the icon will be rotated to point towards.
    :param int|None color: The (optional) color of the icon, as a 32-bit ABGR value.
    :param ColorMode|None color_mode: The (optional) :class:`~pyLiveKML.KML.KML.ColorMode` used to color the icon;
        either 'NORMAL' or 'RANDOM'.
    """

    def __init__(
        self,
        icon: str,
        scale: float = 1.0,
        heading: float | None = None,
        color: int | None = None,
        color_mode: ColorMode | None = None,
    ):
        ColorStyle.__init__(self, color=color, color_mode=color_mode)
        self._scale: float | None = scale
        self._heading: float | None = heading
        self._icon: str | None = icon
        self._hotspot: Vec2 | None = None

    @property
    def kml_type(self) -> str:
        """Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set the KML tag name to
        'IconStyle'"""
        return "IconStyle"

    @property
    def icon(self) -> str | None:
        """URI for the image that will be displayed in GEP as the icon."""
        return self._icon

    @icon.setter
    def icon(self, value: str | None) -> None:
        if self._icon != value:
            self._icon = value
            self.field_changed()

    @property
    def scale(self) -> float | None:
        """Relative scale at which the icon will be displayed in GEP."""
        return self._scale

    @scale.setter
    def scale(self, value: float | None) -> None:
        if self._scale != value:
            self._scale = value
            self.field_changed()

    @property
    def heading(self) -> float | None:
        """Heading (in degrees) that the icon will be displayed pointing towards in GEP."""
        return self._heading

    @heading.setter
    def heading(self, value: float | None) -> None:
        if self._heading != value:
            self._heading = value
            self.field_changed()

    @property
    def hotspot(self) -> Vec2 | None:
        """Relative position in the icon that is anchored to the associated :class:`~pyLiveKML.KML.KMLObjects.Point`"""
        return self._hotspot

    @hotspot.setter
    def hotspot(self, value: Vec2 | None) -> None:
        if value is not None:
            value.name = "hotSpot"
        if self._hotspot != value:
            self._hotspot = value
            self.field_changed()

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        if self.color is not None:
            etree.SubElement(root, "color").text = f"{self.color:08x}"
        if self.color_mode is not None:
            etree.SubElement(root, "colorMode").text = self.color_mode.value
        if self.scale is not None:
            etree.SubElement(root, "scale").text = f"{self.scale:0.3f}"
        if self.heading is not None:
            etree.SubElement(root, "heading").text = f"{self.heading:0.1f}"
        if self.icon is not None:
            etree.SubElement(etree.SubElement(root, "Icon"), "href").text = self.icon
        if self.hotspot is not None:
            root.append(self.hotspot.xml)

    def __str__(self) -> str:
        return f"{self.kml_type}"

    def __repr__(self) -> str:
        return self.__str__()
