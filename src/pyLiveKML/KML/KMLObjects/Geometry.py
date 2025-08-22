from abc import ABC

from pyLiveKML.KML.KMLObjects.Object import Object


class Geometry(Object, ABC):
    """A KML 'Geometry', per https://developers.google.com/kml/documentation/kmlreference#geometry. The
    :class:`~pyLiveKML.KML.KMLObjects.Geometry` class is the abstract base class for KML
    :class:`~pyLiveKML.KML.KMLObjects.Object` instances that have an existence as geospatial objects in GEP and that
    are children of :class:`~pyLiveKML.KML.KMLObjects.Placemark` instances.
    """

    def __init__(self) -> None:
        Object.__init__(self)
        ABC.__init__(self)
