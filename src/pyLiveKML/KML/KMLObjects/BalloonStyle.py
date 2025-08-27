"""BalloonStyle module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML.GeoColor import GeoColor
from pyLiveKML.KML.KML import DisplayMode, ArgParser, NoParse, ColorParse, DumpDirect
from pyLiveKML.KML.KMLObjects.SubStyle import SubStyle


class BalloonStyle(SubStyle):
    """A KML 'BalloonStyle', per https://developers.google.com/kml/documentation/kmlreference#balloonstyle.

    Specifies how the description balloon of
    :class:`~pyLiveKML.KML.KMLObjects.Placemark` objects is drawn.

    :param str|None text: The (optional) text to be displayed in the balloon.
    :param int|None text_color: The (optional) color of the text to be displayed, in 32-bit ABGR format.
    :param int|None bg_color: The (optional) background color of the balloon, in 32-bit ABGR format.
    :param DisplayMode|None display_mode: The (optional) :class:`~pyLiveKML.KML.KML.DisplayMode` of the balloon.
    """

    _kml_type = "BalloonStyle"
    _kml_fields = (
        ArgParser("bg_color", ColorParse, "bgColor", DumpDirect),
        ArgParser("text_color", ColorParse, "textColor", DumpDirect),
        ArgParser("text", NoParse, "text", DumpDirect),
        ArgParser("display_mode", NoParse, "displayMode", DumpDirect),
    )

    def __init__(
        self,
        text: str | None = None,
        text_color: GeoColor | int | None = None,
        bg_color: GeoColor | int | None = None,
        display_mode: DisplayMode | None = None,
    ):
        """BalloonStyle instance constructor."""
        SubStyle.__init__(self)
        self.text = text
        self.display_mode = display_mode
        self.bg_color = bg_color
        self.text_color = text_color
