from typing import Optional


class GeoCoordinates:
    """
    The GeoCoordinates type describes a single instance of a Lon-Lat-Alt (LLA) position, as used in
    :class:`~pyLiveKML.KML.KMLObjects.Point`, :class:`~pyLiveKML.KML.KMLObjects.LineString` and
    :class:`~pyLiveKML.KML.KMLObjects.LinearRing` objects. Note that the GeoCoordinates type is *not* explicitly
    referenced by the KML specification; rather, it is a construct of convenience for the pyLiveKML package.

    :param float lon: The longitude.
    :param float lat: The latitude.
    :param Optional[float] alt: The (optional) altitude.
    :var float lon: The longitude, in decimal degrees.
    :var float lat: The latitude, in decimal degrees.
    :var Optional[float] alt: The (optional) altitude, in metres.
    """

    def __init__(
        self,
        lon: float = 0,
        lat: float = 0,
        alt: Optional[float] = None,
    ):
        self.lon: float = lon
        self.lat: float = lat
        self.alt: Optional[float] = alt

    def __str__(self) -> str:
        if self.alt is None:
            return f"{self.lon:0.6f},{self.lat:0.6f}"
        else:
            return f"{self.lon:0.6f},{self.lat:0.6f},{self.alt:0.1f}"

    def __repr__(self) -> str:
        return self.__str__()
