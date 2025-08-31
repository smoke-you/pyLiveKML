"""LineStyle module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML.Object import _FieldDef, ColorParse
from pyLiveKML.KML.GeoColor import GeoColor
from pyLiveKML.KMLObjects.ColorStyle import ColorStyle


class LineStyle(ColorStyle):
    """A KML 'LineStyle', per https://developers.google.com/kml/documentation/kmlreference#linestyle.

    Specifies various properties of a :class:`~pyLiveKML.KMLObjects.Geometry`, typically either a
    :class:`~pyLiveKML.KMLObjects.LineString` or :class:`~pyLiveKML.KMLObjects.LinearRing`, including
    the inner and outer boundaries of :class:`~pyLiveKML.KMLObjects.Polygon` objects.

    :param float|None width: The (optional) width of the line, in pixels.
    :param int|None color: The (optional) color of the line, as a 32-bit ABGR value.
    """

    _kml_tag = "LineStyle"
    _kml_fields = ColorStyle._kml_fields + (
        _FieldDef("width"),
        _FieldDef("gx_outer_color", "gx:outerColor", ColorParse),
        _FieldDef("gx_outer_width", "gx:outerWidth"),
        _FieldDef("gx_physical_width", "gx:physicalWidth"),
        _FieldDef("gx_label_visibility", "gx:labelVisibility"),
    )

    def __init__(
        self,
        width: float | None = None,
        color: GeoColor | int | None = None,
        gx_outer_color: GeoColor | int | None = None,
        gx_outer_width: float | None = None,
        gx_physical_width: float | None = None,
        gx_label_visibility: bool | None = None,
    ):
        """LineStyle instance constructor."""
        ColorStyle.__init__(self, color)
        self.width = width
        self.gx_outer_color = gx_outer_color
        self.gx_outer_width = gx_outer_width
        self.gx_physical_width = gx_physical_width
        self.gx_label_visibility = gx_label_visibility
