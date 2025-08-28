"""IconStyle module."""

from typing import Iterator

from lxml import etree  # type: ignore

from pyLiveKML.KML.GeoColor import GeoColor
from pyLiveKML.KML.KML import ColorMode, _FieldDef, NoDump, NoParse, DumpDirect
from pyLiveKML.KML.KMLObjects.ColorStyle import ColorStyle
from pyLiveKML.KML.KMLObjects.Object import Object, ObjectChild
from pyLiveKML.KML._BaseObject import _BaseObject
from pyLiveKML.KML.Vec2 import HotSpot


class _IconStyle_Icon(_BaseObject):
    """A minimalist Icon class, used only within `IconStyle`."""

    _kml_type = "Icon"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("href", NoParse, "href", DumpDirect),
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
    _kml_fields = ColorStyle._kml_fields + (
        _FieldDef("icon", NoParse, "", NoDump),
        _FieldDef("scale", NoParse, "scale", DumpDirect),
        _FieldDef("heading", NoParse, "heading", DumpDirect),
    )
    _direct_children = ColorStyle._direct_children + ("icon",)

    def __init__(
        self,
        icon: str,
        scale: float = 1.0,
        heading: float | None = None,
        color: GeoColor | int | None = None,
        color_mode: ColorMode | None = None,
        hot_spot: HotSpot | None = None,
    ):
        """IconStyle instance constructor."""
        ColorStyle.__init__(self, color=color, color_mode=color_mode)
        self.scale = scale
        self.heading = heading
        self.icon = _IconStyle_Icon(icon)
        self.hot_spot = hot_spot

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        if self.hot_spot:
            self.hot_spot.build_kml(root, False)
