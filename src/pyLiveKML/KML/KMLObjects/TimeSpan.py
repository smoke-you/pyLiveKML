"""TimeSpan module."""

from datetime import datetime
from typing import Iterator

from lxml import etree  # type: ignore

from pyLiveKML.KML.KMLObjects.TimePrimitive import TimePrimitive
from pyLiveKML.KML.KML import _FieldDef, NoParse, DumpDirect


class TimeSpan(TimePrimitive):
    """A KML 'TimeSpan', per https://developers.google.com/kml/documentation/kmlreference#style."""

    _kml_type = "TimeSpan"
    _kml_fields = TimePrimitive._kml_fields + (
        _FieldDef("begin", NoParse, "begin", DumpDirect),
        _FieldDef("end", NoParse, "end", DumpDirect),
    )

    def __init__(self, begin: datetime, end: datetime):
        """TimeSpan instance constructor."""
        TimePrimitive.__init__(self)
        self.begin = begin
        self.end = end


class GxTimeSpan(TimeSpan):

    _kml_type = "gx:TimeSpan"
