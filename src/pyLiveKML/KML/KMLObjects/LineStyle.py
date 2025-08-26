"""LineStyle module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML.GeoColor import GeoColor
from pyLiveKML.KML.KMLObjects.ColorStyle import ColorStyle
from pyLiveKML.KML.KML import ArgParser, NoParse, ColorParse, DumpDirect


class LineStyle(ColorStyle):
    """A KML 'LineStyle', per https://developers.google.com/kml/documentation/kmlreference#linestyle.

    Specifies various properties of a :class:`~pyLiveKML.KML.KMLObjects.Geometry`, typically either a
    :class:`~pyLiveKML.KML.KMLObjects.LineString` or :class:`~pyLiveKML.KML.KMLObjects.LinearRing`, including
    the inner and outer boundaries of :class:`~pyLiveKML.KML.KMLObjects.Polygon` objects.

    :param float|None width: The (optional) width of the line, in pixels.
    :param int|None color: The (optional) color of the line, as a 32-bit ABGR value.
    """

    _kml_type = "LineStyle"
    _kml_fields = ColorStyle._kml_fields + (
        ArgParser("width", NoParse, "width", DumpDirect),
        ArgParser("gx_outer_color", ColorParse, "gx:outerColor", DumpDirect),
        ArgParser("gx_outer_width", NoParse, "gx:outerWidth", DumpDirect),
        ArgParser("gx_physical_width", NoParse, "gx:physicalWidth", DumpDirect),
        ArgParser("gx_label_visibility", NoParse, "gx:labelVisibility", DumpDirect),
    )

    def __init__(
        self,
        width: float | None = None,
        color: GeoColor | int | None = None,
    ):
        """LineStyle instance constructor."""
        ColorStyle.__init__(self, color)
        self.width = width
        self.gx_outer_color: int | None = None
        self.gx_outer_width: float | None = None
        self.gx_physical_width: float | None = None
        self.gx_label_visibility: bool | None = None
