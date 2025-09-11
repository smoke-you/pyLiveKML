"""TimeSpan module."""

from datetime import datetime

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import _FieldDef, _DateTimeParse
from pyLiveKML.objects.TimePrimitive import TimePrimitive


class TimeSpan(TimePrimitive):
    """A KML `<TimeSpan>` tag constructor.

    Represents an extent in time bounded by begin and end `datetime`s.

    Notes
    -----
    If `begin` or `end` is `None`, then that end of the period is unbounded.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#style

    Parameters
    ----------
    begin: datetime | str | None, default = None
    end: datetime | str | None, default = None

    Attributes
    ----------
    begin: datetime | None
    end: datetime | None

    """

    _kml_tag = "TimeSpan"
    _kml_fields = TimePrimitive._kml_fields + (
        _FieldDef("begin", parser=_DateTimeParse),
        _FieldDef("end", parser=_DateTimeParse),
    )

    def __init__(
        self,
        begin: datetime | str | None = None,
        end: datetime | str | None = None,
    ):
        """TimeSpan instance constructor."""
        TimePrimitive.__init__(self)
        self.begin = begin
        self.end = end
