"""PolyStyle module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML import ColorModeEnum
from pyLiveKML.KML._BaseObject import _FieldDef, DumpDirect, NoParse
from pyLiveKML.KML.GeoColor import GeoColor
from pyLiveKML.KML.KMLObjects.ColorStyle import ColorStyle


class PolyStyle(ColorStyle):
    """A KML 'PolyStyle', per https://developers.google.com/kml/documentation/kmlreference#polystyle.

    Specifies various properties that define how a :class:`~pyLiveKML.KML.KMLObjects.Polygon` is drawn.

    :param int|None color: The (optional) color, as a 32-bit ABGR value, that will be used to :attr:`fill` the
        polygon's area in GEP.
    :param ColorMode|None color_mode: An (optional) :class:`~pyLiveKML.KML.KML.ColorMode` that determines how GEP
        chooses the polygon :attr:`fill` color.
    :param bool|None fill: Optional flag to indicate whether GEP should fill in the polygon with a color.
    :param bool|None outline: Optional flag to indicate whether GEP should draw the polygon's outline.
    """

    _kml_type = "PolyStyle"
    _kml_fields = ColorStyle._kml_fields + (
        _FieldDef("fill", NoParse, "fill", DumpDirect),
        _FieldDef("outline", NoParse, "outline", DumpDirect),
    )

    def __init__(
        self,
        color: GeoColor | int | None = None,
        color_mode: ColorModeEnum | None = None,
        fill: bool | None = None,
        outline: bool | None = None,
    ):
        """PolyStyle instance constructor."""
        ColorStyle.__init__(self, color, color_mode)
        self.fill = fill
        self.outline = outline
