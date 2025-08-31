"""TourControl module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML import PlayModeEnum
from pyLiveKML.KML.Object import _FieldDef
from pyLiveKML.KMLObjects.TourPrimitive import TourPrimitive


class TourControl(TourPrimitive):
    """A KML 'gx:TourControl', per https://developers.google.com/kml/documentation/kmlreference#gxtourcontrol."""

    _kml_tag = "gx:TourControl"
    _kml_fields = TourPrimitive._kml_fields + (_FieldDef("play_mode", "gx:playMode"),)

    def __init__(
        self,
        play_mode: PlayModeEnum = PlayModeEnum.PAUSE,
    ) -> None:
        """GxTourControl instance constructor."""
        TourPrimitive.__init__(self)
        self.play_mode = play_mode
