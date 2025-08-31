"""BalloonStyle module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML import DisplayModeEnum
from pyLiveKML.KML.Object import _FieldDef, ColorParse
from pyLiveKML.KML.GeoColor import GeoColor
from pyLiveKML.KMLObjects.SubStyle import SubStyle


class BalloonStyle(SubStyle):
    """A KML 'BalloonStyle', per https://developers.google.com/kml/documentation/kmlreference#balloonstyle.

    Specifies how the description balloon of
    :class:`~pyLiveKML.KMLObjects.Placemark` objects is drawn.

    :param str|None text: The (optional) text to be displayed in the balloon.
    :param int|None text_color: The (optional) color of the text to be displayed, in 32-bit ABGR format.
    :param int|None bg_color: The (optional) background color of the balloon, in 32-bit ABGR format.
    :param DisplayMode|None display_mode: The (optional) :class:`~pyLiveKML.KML.KML.DisplayMode` of the balloon.
    """

    _kml_tag = "BalloonStyle"
    _kml_fields = SubStyle._kml_fields + (
        _FieldDef("bg_color", "bgColor", ColorParse),
        _FieldDef("text_color", "textColor", ColorParse),
        _FieldDef("text"),
        _FieldDef("display_mode", "displayMode"),
    )

    def __init__(
        self,
        text: str | None = None,
        text_color: GeoColor | int | None = None,
        bg_color: GeoColor | int | None = None,
        display_mode: DisplayModeEnum | None = None,
    ):
        """BalloonStyle instance constructor."""
        SubStyle.__init__(self)
        self.text = text
        self.display_mode = display_mode
        self.bg_color = bg_color
        self.text_color = text_color
