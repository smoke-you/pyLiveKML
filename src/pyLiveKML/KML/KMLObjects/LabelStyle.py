from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import ColorMode
from pyLiveKML.KML.KMLObjects.ColorStyle import ColorStyle


class LabelStyle(ColorStyle):
    """A KML 'LabelStyle', per https://developers.google.com/kml/documentation/kmlreference#iconstyle.  Specifies
    various properties that define how the name of a :class:`~pyLiveKML.KML.KMLObjects.Feature` is drawn in GEP.

    :param float|None scale: The (optional) relative scale of the text.
    :param int|None color: The (optional) color of the text, as a 32-bit ABGR value.
    :param ColorMode|None color_mode: The (optional) :class:`~pyLiveKML.KML.KML.ColorMode` used to color the text;
        either 'NORMAL' or 'RANDOM'.
    """

    def __init__(
        self,
        scale: float | None = None,
        color: int | None = None,
        color_mode: ColorMode | None = None,
    ):
        ColorStyle.__init__(self, color=color, color_mode=color_mode)
        self._scale = scale

    @property
    def kml_type(self) -> str:
        """Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set the KML tag name to
        'LabelStyle'
        """
        return "LabelStyle"

    @property
    def scale(self) -> float | None:
        """Relative scale of the text."""
        return self._scale

    @scale.setter
    def scale(self, value: float | None) -> None:
        if self._scale != value:
            self._scale = value
            self.field_changed()

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        if self.color is not None:
            etree.SubElement(root, "color").text = f"{self.color:08x}"
        if self.color_mode is not None:
            etree.SubElement(root, "colorMode").text = self.color_mode.value
        if self.scale is not None:
            etree.SubElement(root, "scale").text = f"{self.scale:0.3f}"

    def __str__(self) -> str:
        return f"{self.kml_type}"

    def __repr__(self) -> str:
        return self.__str__()
