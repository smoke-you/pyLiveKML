"""TimeSpan module."""

from datetime import datetime
from dateutil.parser import parse as dtparser

from lxml import etree  # type: ignore

from pyLiveKML.KML.Object import _FieldDef
from pyLiveKML.KMLObjects.TimePrimitive import TimePrimitive


class TimeSpan(TimePrimitive):
    """A KML 'TimeSpan', per https://developers.google.com/kml/documentation/kmlreference#style."""

    _kml_tag = "TimeSpan"
    _kml_fields = TimePrimitive._kml_fields + (
        _FieldDef("begin"),
        _FieldDef("end"),
    )

    def __init__(self, begin: datetime | str, end: datetime | str):
        """TimeSpan instance constructor."""
        TimePrimitive.__init__(self)
        self.begin: datetime
        self.end: datetime
        if isinstance(begin, str):
            self.begin = dtparser(begin)
        else:
            self.begin = begin
        if isinstance(end, str):
            self.end = dtparser(end)
        else:
            self.end = end


class GxTimeSpan(TimeSpan):
    """Version of `TimeSpan` under the `gx` namespace.

    Available for use by `AbstractView` subclasses. Refer to Google KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#gx:timespan-and-gx:timestamp.
    """

    _kml_tag = "gx:TimeSpan"
