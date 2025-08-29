"""SoundCue module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML._BaseObject import (
    _FieldDef,
    DumpDirect,
    NoParse,
)
from pyLiveKML.KML.KMLObjects.TourPrimitive import TourPrimitive


class GxSoundCue(TourPrimitive):
    """A KML 'gx:SoundCue', per https://developers.google.com/kml/documentation/kmlreference#gxsoundcue."""

    _kml_type = "gx:SoundCue"
    _kml_fields = TourPrimitive._kml_fields + (
        _FieldDef("href", NoParse, "href", DumpDirect),
        _FieldDef("delayed_start", NoParse, "gx:delayedStart", DumpDirect),
    )

    def __init__(
        self,
        href: str,
        delayed_start: float = 0,
    ) -> None:
        """GxSoundCue instance constructor."""
        TourPrimitive.__init__(self)
        self.href = href
        self.delayed_start = delayed_start
