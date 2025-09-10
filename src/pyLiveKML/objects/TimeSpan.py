"""TimeSpan module."""

from datetime import datetime

from dateutil.parser import parse as dtparser
from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import _FieldDef
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
        _FieldDef("begin"),
        _FieldDef("end"),
    )

    def __init__(
        self,
        begin: datetime | str | None = None,
        end: datetime | str | None = None,
    ):
        """TimeSpan instance constructor."""
        TimePrimitive.__init__(self)
        self.begin: datetime | None
        self.end: datetime | None
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

    Available for use by `AbstractView` subclasses.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#gx:timespan-and-gx:timestamp

    """

    _kml_tag = "gx:TimeSpan"
