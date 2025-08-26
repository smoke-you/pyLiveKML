"""PolyStyle module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML.GeoColor import GeoColor
from pyLiveKML.KML.KMLObjects.ColorStyle import ColorStyle
from pyLiveKML.KML.KML import ColorMode, ArgParser, NoParse, DumpDirect


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
        ArgParser("fill", NoParse, "fill", DumpDirect),
        ArgParser("outline", NoParse, "outline", DumpDirect),
    )

    def __init__(
        self,
        color: GeoColor | int | None = None,
        color_mode: ColorMode | None = None,
        fill: bool | None = None,
        outline: bool | None = None,
    ):
        """PolyStyle instance constructor."""
        ColorStyle.__init__(self, color, color_mode)
        self.fill: bool | None = fill
        self.outline: bool | None = outline

    # def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
    #     """Construct the KML content and append it to the provided etree.Element."""
    #     if self.color is not None:
    #         etree.SubElement(root, "color").text = str(self.color)
    #     if self.color_mode is not None:
    #         etree.SubElement(root, "colorMode").text = self.color_mode.value
    #     if self._fill is not None:
    #         etree.SubElement(root, "fill").text = str(int(self._fill))
    #     if self._outline is not None:
    #         etree.SubElement(root, "outline").text = str(int(self._outline))
