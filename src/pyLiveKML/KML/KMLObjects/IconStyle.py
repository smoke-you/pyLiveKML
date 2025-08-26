"""IconStyle module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML.GeoColor import GeoColor
from pyLiveKML.KML.KML import ColorMode, ArgParser, NoDump, NoParse, DumpDirect
from pyLiveKML.KML.KMLObjects.ColorStyle import ColorStyle
from pyLiveKML.KML.Vec2 import Vec2


class IconStyle(ColorStyle):
    """A KML 'IconStyle', per https://developers.google.com/kml/documentation/kmlreference#iconstyle.

    Specifies various properties that define how a
    :class:`~pyLiveKML.KML.KMLObjects.Icon` is drawn.  Applies to
    :class:`~pyLiveKML.KML.KMLObjects.Point` geometries.

    :param str icon: A URI for an image or icon file.
    :param float scale: The (optional) relative scale of the icon.
    :param float heading: The (optional) heading, in degrees, that the icon will be rotated to point towards.
    :param int|None color: The (optional) color of the icon, as a 32-bit ABGR value.
    :param ColorMode|None color_mode: The (optional) :class:`~pyLiveKML.KML.KML.ColorMode` used to color the icon;
        either 'NORMAL' or 'RANDOM'.
    """

    _kml_type = "IconStyle"
    _kml_fields = (
        ArgParser("icon", NoParse, "", NoDump),
        ArgParser("scale", NoParse, "scale", DumpDirect),
        ArgParser("heading", NoParse, "heading", DumpDirect),
        ArgParser("color", NoParse, "color", DumpDirect),
        ArgParser("color_mode", NoParse, "colorMode", DumpDirect),
    )

    def __init__(
        self,
        icon: str,
        scale: float = 1.0,
        heading: float | None = None,
        color: GeoColor | int | None = None,
        color_mode: ColorMode | None = None,
    ):
        """IconStyle instance constructor."""
        ColorStyle.__init__(self, color=color, color_mode=color_mode)
        self.scale = scale
        self.heading = heading
        self.icon = icon
        self._hotspot: Vec2 | None = None

    @property
    def hotspot(self) -> Vec2 | None:
        """Relative position in the icon that is anchored to the associated :class:`~pyLiveKML.KML.KMLObjects.Point`."""
        return self._hotspot

    @hotspot.setter
    def hotspot(self, value: Vec2 | None) -> None:
        if value is not None:
            value.name = "hotSpot"
        if self._hotspot != value:
            self._hotspot = value
            self.field_changed()

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        if self.icon is not None:
            etree.SubElement(etree.SubElement(root, "Icon"), "href").text = self.icon
        if self.hotspot is not None:
            root.append(self.hotspot.xml)
