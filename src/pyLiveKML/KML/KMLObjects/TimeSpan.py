"""TimeSpan module."""

from datetime import datetime
from typing import Iterator

from lxml import etree  # type: ignore

from pyLiveKML.KML.KMLObjects.TimePrimitive import TimePrimitive
from pyLiveKML.KML.KMLObjects.Object import ObjectChild


class TimeSpan(TimePrimitive):
    """A KML 'TimeSpan', per https://developers.google.com/kml/documentation/kmlreference#style."""

    _kml_type = "TimeSpan"

    def __init__(self, begin: datetime, end: datetime):
        """TimeSpan instance constructor."""
        TimePrimitive.__init__(self)
        self._begin: datetime = begin
        self._end: datetime = end

    @property
    def begin(self) -> datetime:
        """A :class:`datetime.datetime` embedded in this :class:`~pyLiveKML.KML.KMLObjects.TimeStamp`."""
        return self._begin

    @begin.setter
    def begin(self, value: datetime) -> None:
        if value != self._begin:
            self._begin = value
            self.field_changed()

    @property
    def end(self) -> datetime:
        """A :class:`datetime.datetime` embedded in this :class:`~pyLiveKML.KML.KMLObjects.TimeStamp`."""
        return self._end

    @end.setter
    def end(self, value: datetime) -> None:
        if value != self._end:
            self._end = value
            self.field_changed()


    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        etree.SubElement(root, "begin").text = self.begin.isoformat()
        etree.SubElement(root, "end").text = self.end.isoformat()

    def __str__(self) -> str:
        """Return a string representation."""
        return f"{self.kml_type}"

    def __repr__(self) -> str:
        """Return a debug representation."""
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        """Check equality."""
        return isinstance(other, TimeSpan) and self.begin == other.begin and self.end == other.end

    def __ne__(self, other: object) -> bool:
        """Check negative equality."""
        return not self.__eq__(other)
