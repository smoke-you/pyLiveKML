"""SoundCue module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML.Object import _FieldDef
from pyLiveKML.KMLObjects.TourPrimitive import TourPrimitive


class SoundCue(TourPrimitive):
    """A KML 'gx:SoundCue', per https://developers.google.com/kml/documentation/kmlreference#gxsoundcue."""

    _kml_tag = "gx:SoundCue"
    _kml_fields = TourPrimitive._kml_fields + (
        _FieldDef("href"),
        _FieldDef("delayed_start", "gx:delayedStart"),
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
