"""TimeStamp module."""

from datetime import datetime
from typing import Iterator, Any

from lxml import etree  # type: ignore

from pyLiveKML.KML.KMLObjects.TimePrimitive import TimePrimitive
from pyLiveKML.KML.KML import _FieldDef, NoParse, DumpDirect


class TimeStamp(TimePrimitive):
    """A KML 'TimeStamp', per https://developers.google.com/kml/documentation/kmlreference#style."""

    _kml_type = "TimeStamp"
    _kml_fields = TimePrimitive._kml_fields + (
        _FieldDef("when", NoParse, "when", DumpDirect),
    )

    def __init__(self, when: datetime):
        """TimeStamp instance constructor."""
        TimePrimitive.__init__(self)
        self.when: datetime = when


class GxTimeStamp(TimeStamp):
    """Version of `TimeStamp` under the `gx` namespace.

    Available for use by `AbstractView` subclasses. Refer to Google KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#gx:timespan-and-gx:timestamp.
    """

    _kml_type = "gx:TimeStamp"
