"""TimeStamp module."""

from datetime import datetime
from typing import Iterator

from lxml import etree  # type: ignore

from pyLiveKML.KML.KMLObjects.TimePrimitive import TimePrimitive
from pyLiveKML.KML.KMLObjects.Object import ObjectChild


class TimeStamp(TimePrimitive):
    """A KML 'TimeStamp', per https://developers.google.com/kml/documentation/kmlreference#style."""

    _kml_type = "TimeStamp"

    def __init__(self, when: datetime):
        """TimeStamp instance constructor."""
        TimePrimitive.__init__(self)
        self._when: datetime = when

    @property
    def when(self) -> datetime:
        """A :class:`datetime.datetime` embedded in this :class:`~pyLiveKML.KML.KMLObjects.TimeStamp`."""
        return self._when

    @when.setter
    def when(self, value: datetime) -> None:
        if value != self._when:
            self._when = value
            self.field_changed()

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        etree.SubElement(root, "when").text = self.when.isoformat()

    def __str__(self) -> str:
        """Return a string representation."""
        return f"{self.kml_type}"

    def __repr__(self) -> str:
        """Return a debug representation."""
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        """Check equality."""
        return isinstance(other, TimeStamp) and self.when == other.when

    def __ne__(self, other: object) -> bool:
        """Check negative equality."""
        return not self.__eq__(other)
