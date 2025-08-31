"""IconStyle module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML import ColorModeEnum
from pyLiveKML.KML._BaseObject import _BaseObject, _FieldDef, NoDump
from pyLiveKML.KML.GeoColor import GeoColor
from pyLiveKML.KML.Vec2 import HotSpot
from pyLiveKML.KMLObjects.ColorStyle import ColorStyle
from pyLiveKML.KMLObjects.Object import _ChildDef


class _IconStyle_Icon(_BaseObject):
    """A minimalist Icon class, used only within `IconStyle`."""

    _kml_tag = "Icon"
    _kml_fields = _BaseObject._kml_fields + (_FieldDef("href"),)

    def __init__(self, href: str):
        """_IconStyle_Icon instance constructor."""
        super().__init__()
        self.href = href


class IconStyle(ColorStyle):
    """A KML 'IconStyle', per https://developers.google.com/kml/documentation/kmlreference#iconstyle.

    Specifies various properties that define how a
    :class:`~pyLiveKML.KMLObjects.Icon` is drawn.  Applies to
    :class:`~pyLiveKML.KMLObjects.Point` geometries.

    :param str icon: A URI for an image or icon file.
    :param float scale: The (optional) relative scale of the icon.
    :param float heading: The (optional) heading, in degrees, that the icon will be rotated to point towards.
    :param int|None color: The (optional) color of the icon, as a 32-bit ABGR value.
    :param ColorMode|None color_mode: The (optional) :class:`~pyLiveKML.KML.KML.ColorMode` used to color the icon;
        either 'NORMAL' or 'RANDOM'.
    """

    _kml_tag = "IconStyle"
    _kml_fields = ColorStyle._kml_fields + (
        _FieldDef("icon", dumper=NoDump),
        _FieldDef("scale"),
        _FieldDef("heading"),
    )
    _direct_children = ColorStyle._direct_children + (
        _ChildDef("icon"),
        _ChildDef("hot_spot"),
    )

    def __init__(
        self,
        icon: str,
        scale: float = 1.0,
        heading: float | None = None,
        color: GeoColor | int | None = None,
        color_mode: ColorModeEnum | None = None,
        hot_spot: HotSpot | None = None,
    ):
        """IconStyle instance constructor."""
        ColorStyle.__init__(self, color=color, color_mode=color_mode)
        self.scale = scale
        self.heading = heading
        self.icon = _IconStyle_Icon(icon)
        self.hot_spot = hot_spot
