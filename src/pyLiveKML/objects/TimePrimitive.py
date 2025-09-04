"""TimePrimitive module."""

from abc import ABC

from pyLiveKML.objects.Object import Object


class TimePrimitive(Object, ABC):
    """A KML 'TimePrimitive', per https://developers.google.com/kml/documentation/kmlreference."""

    def __init__(self) -> None:
        """TimePrimitive instance constructor."""
        Object.__init__(self)
        ABC.__init__(self)
