"""TimeStamp module."""

from datetime import datetime
from typing import Iterator, Any

from lxml import etree  # type: ignore

from pyLiveKML.KML.KMLObjects.TimePrimitive import TimePrimitive
from pyLiveKML.KML.KMLObjects.Object import ObjectChild
from pyLiveKML.KML.KML import ArgParser, Direct


class TimeStamp(TimePrimitive):
    """A KML 'TimeStamp', per https://developers.google.com/kml/documentation/kmlreference#style."""

    _kml_type = "TimeStamp"
    _kml_fields = (ArgParser("when", Direct.parse),)

    def __init__(self, when: datetime):
        """TimeStamp instance constructor."""
        TimePrimitive.__init__(self)
        self.when: datetime = when

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        etree.SubElement(root, "when").text = self.when.isoformat()

    def __str__(self) -> str:
        """Return a string representation."""
        return f"{self.kml_type}"

    def __repr__(self) -> str:
        """Return a debug representation."""
        return self.__str__()
