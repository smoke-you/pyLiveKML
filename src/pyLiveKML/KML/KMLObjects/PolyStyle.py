"""PolyStyle module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML.KMLObjects.ColorStyle import ColorStyle
from pyLiveKML.KML.KML import ColorMode


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

    def __init__(
        self,
        color: int | None = None,
        color_mode: ColorMode | None = None,
        fill: bool | None = None,
        outline: bool | None = None,
    ):
        """PolyStyle instance constructor."""
        ColorStyle.__init__(self, color, color_mode)
        self._fill: bool | None = fill
        self._outline: bool | None = outline

    @property
    def kml_type(self) -> str:
        """The class' KML type string.

        Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set
        the KML tag name to 'PolyStyle'
        """
        return "PolyStyle"

    @property
    def fill(self) -> bool | None:
        """Flag indicating whether polygons using this style should be filled.

        True if the affected :class:`~pyLiveKML.KML.KMLObjects.Polygon` is to be filled in using the :attr:`color`
        property. False if it is not. None implies True.
        """
        return self._fill

    @fill.setter
    def fill(self, value: bool | None) -> None:
        if self._fill != value:
            self._fill = value
            self.field_changed()

    @property
    def outline(self) -> bool | None:
        """Flag to indicate whether polygons using this style should be drawn with distinct boundary line/s.

        True if the outline of the :class:`~pyLiveKML.KML.KMLObjects.Polygon` is to be drawn using a separate
        :class:`~pyLiveKML.KML.KMLObjects.LineStyle`, specified in the :class:`~pyLiveKML.KML.KMLObjects.StyleSelector`
        that is the parent of this :class:`~pyLiveKML.KML.KMLObjects.PolyStyle` instance. False if it is not. None
        implies True.
        """
        return True if self._outline is None else self._outline

    @outline.setter
    def outline(self, value: bool | None) -> None:
        if self._outline != value:
            self._outline = value
            self.field_changed()

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        if self.color is not None:
            etree.SubElement(root, "color").text = f"{self.color:08x}"
        if self.color_mode is not None:
            etree.SubElement(root, "colorMode").text = self.color_mode.value
        if self._fill is not None:
            etree.SubElement(root, "fill").text = str(int(self._fill))
        if self._outline is not None:
            etree.SubElement(root, "outline").text = str(int(self._outline))
