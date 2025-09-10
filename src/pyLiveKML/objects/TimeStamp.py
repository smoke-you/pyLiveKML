"""TimeStamp module."""

from datetime import datetime

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import _FieldDef, DateTimeParse
from pyLiveKML.objects.TimePrimitive import TimePrimitive


class TimeStamp(TimePrimitive):
    """A KML `<TimeStamp>` tag constructor.

    Represents a single moment in time. This is a simple element and contains no
    children. Its value is a `datetime`, specified in XML time. The precision of the
    `TimeStamp` is dictated by the value of `when`.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#style
    * http://www.w3.org/TR/xmlschema-2/#isoformats

    Parameters
    ----------
    when : datetime | str

    Attributes
    ----------
    when : datetime

    """

    _kml_tag = "TimeStamp"
    _kml_fields = TimePrimitive._kml_fields + (_FieldDef("when", parser=DateTimeParse),)

    def __init__(
        self,
        when: datetime | str,
    ):
        """TimeStamp instance constructor."""
        TimePrimitive.__init__(self)
        self.when = when
