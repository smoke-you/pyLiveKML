"""TourPrimitive module."""

from abc import ABC

from pyLiveKML.KMLObjects.Object import Object


class TourPrimitive(Object, ABC):
    """A KML 'TourPrimitive', per https://developers.google.com/kml/documentation/kmlreference#tourprimitive."""

    def __init__(self) -> None:
        """TourPrimitive instance constructor."""
        Object.__init__(self)
        ABC.__init__(self)
