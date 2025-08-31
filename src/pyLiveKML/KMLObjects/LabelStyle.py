"""ColorStyle module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML import ColorModeEnum
from pyLiveKML.KML.Object import _FieldDef
from pyLiveKML.KML.GeoColor import GeoColor
from pyLiveKML.KMLObjects.ColorStyle import ColorStyle


class LabelStyle(ColorStyle):
    """A KML 'LabelStyle', per https://developers.google.com/kml/documentation/kmlreference#iconstyle.

    Specifies various properties that define how the name of a
    :class:`~pyLiveKML.KMLObjects.Feature` is drawn in GEP.

    :param float|None scale: The (optional) relative scale of the text.
    :param int|None color: The (optional) color of the text, as a 32-bit ABGR value.
    :param ColorMode|None color_mode: The (optional) :class:`~pyLiveKML.KML.KML.ColorMode` used to color the text;
        either 'NORMAL' or 'RANDOM'.
    """

    _kml_tag = "LabelStyle"
    _kml_fields = ColorStyle._kml_fields + (_FieldDef("scale"),)

    def __init__(
        self,
        scale: float | None = None,
        color: GeoColor | int | None = None,
        color_mode: ColorModeEnum | None = None,
    ):
        """ColorStyle instance constructor."""
        super().__init__(color=color, color_mode=color_mode)
        self.scale = scale
