"""TimeStamp module."""

from datetime import datetime

from lxml import etree  # type: ignore

from pyLiveKML.KML.Object import _FieldDef
from pyLiveKML.KMLObjects.TimePrimitive import TimePrimitive


class TimeStamp(TimePrimitive):
    """A KML 'TimeStamp', per https://developers.google.com/kml/documentation/kmlreference#style."""

    _kml_tag = "TimeStamp"
    _kml_fields = TimePrimitive._kml_fields + (_FieldDef("when"),)

    def __init__(self, when: datetime):
        """TimeStamp instance constructor."""
        TimePrimitive.__init__(self)
        self.when: datetime = when


class GxTimeStamp(TimeStamp):
    """Version of `TimeStamp` under the `gx` namespace.

    Available for use by `AbstractView` subclasses. Refer to Google KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#gx:timespan-and-gx:timestamp.
    """

    _kml_tag = "gx:TimeStamp"
