"""IconStyle module."""

from typing import Iterator

from lxml import etree  # type: ignore

from pyLiveKML.KML.GeoColor import GeoColor
from pyLiveKML.KML.KML import ColorMode, ArgParser, NoDump, NoParse, DumpDirect
from pyLiveKML.KML.KMLObjects.ColorStyle import ColorStyle
from pyLiveKML.KML.KMLObjects.Object import Object, ObjectChild
from pyLiveKML.KML.Vec2 import Vec2

class _IconStyle_Icon(Object):
    """A minimalist Icon class, used only within `IconStyle`."""

    _kml_type = "Icon"
    _kml_fields = (
        ArgParser("href", NoParse, "href", DumpDirect),
    )

    def __init__(self, href: str):
        """_IconStyle_Icon instance constructor."""
        super().__init__()
        self.href = href


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
        ArgParser("hot_spot", NoParse, "", NoDump),
    )

    def __init__(
        self,
        icon: str,
        scale: float = 1.0,
        heading: float | None = None,
        color: GeoColor | int | None = None,
        color_mode: ColorMode | None = None,
        hot_spot: Vec2 | None = None,
    ):
        """IconStyle instance constructor."""
        ColorStyle.__init__(self, color=color, color_mode=color_mode)
        self.scale = scale
        self.heading = heading
        self.icon = _IconStyle_Icon(icon)
        self.hot_spot = hot_spot

    @property
    def children(self) -> Iterator[ObjectChild]:
        yield ObjectChild(self, self.icon)

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        root.append(self.icon.construct_kml())
        if self.hot_spot is not None:
            root.append(self.hot_spot.xml)

