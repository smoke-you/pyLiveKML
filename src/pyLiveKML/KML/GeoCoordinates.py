"""GeoCoordinates module."""

from typing import Any

from pyLiveKML.KML.Object import Angle90, Angle180


class GeoCoordinates:
    """The GeoCoordinates type describes a single instance of a Lon-Lat-Alt (LLA) position.

    These objects are used in
    :class:`~pyLiveKML.KMLObjects.Point`, :class:`~pyLiveKML.KMLObjects.LineString` and
    :class:`~pyLiveKML.KMLObjects.LinearRing` objects. Note that the GeoCoordinates type is *not* explicitly
    referenced by the KML specification; rather, it is a construct of convenience for the pyLiveKML package.

    :param float lon: The longitude.
    :param float lat: The latitude.
    :param Optional[float] alt: The (optional) altitude.
    :var float lon: The longitude, in decimal degrees.
    :var float lat: The latitude, in decimal degrees.
    :var float|None alt: The (optional) altitude, in metres.
    """

    def __init__(
        self,
        lon: float = 0,
        lat: float = 0,
        alt: float | None = None,
    ):
        """GeoCoordinates instance constructor."""
        self.lon = lon
        self.lat = lat
        self.alt = alt

    def __setattr__(self, name: str, value: Any) -> None:
        """GeoCoordinates __setattr__ implementation."""
        if name == "lon":
            value = Angle180.parse(value)
        elif name == "lat":
            value = Angle90.parse(value)
        super().__setattr__(name, value)

    def __str__(self) -> str:
        """Return a string representation."""
        if self.alt is None:
            return f"{self.lon:0.6f},{self.lat:0.6f}"
        else:
            return f"{self.lon:0.6f},{self.lat:0.6f},{self.alt:0.1f}"
