"""Geometry module."""

from abc import ABC

from pyLiveKML.objects.Object import Object


class Geometry(Object, ABC):
    """A KML 'Geometry', per https://developers.google.com/kml/documentation/kmlreference#geometry.

    The :class:`~pyLiveKML.KMLObjects.Geometry` class is the abstract base class
    for KML :class:`~pyLiveKML.KMLObjects.Object` instances that have an existence
    as geospatial objects in GEP and that are children of
    :class:`~pyLiveKML.KMLObjects.Placemark` instances.
    """

    def __init__(self) -> None:
        """Geometry instance constructor."""
        Object.__init__(self)
        ABC.__init__(self)
