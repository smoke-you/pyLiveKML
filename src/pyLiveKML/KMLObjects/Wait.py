"""Wait module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML._BaseObject import _FieldDef
from pyLiveKML.KMLObjects.TourPrimitive import TourPrimitive


class GxWait(TourPrimitive):
    """A KML 'gx:Wait', per https://developers.google.com/kml/documentation/kmlreference#gxwait."""

    _kml_tag = "gx:Wait"
    _kml_fields = TourPrimitive._kml_fields + (_FieldDef("duration"),)

    def __init__(
        self,
        duration: float = 0,
    ) -> None:
        """GxWait instance constructor."""
        TourPrimitive.__init__(self)
        self.duration = duration
