"""GeoCoordinates module."""

from typing import Any

from pyLiveKML.objects.Object import Angle90, Angle180


class GeoCoordinates:
    """The GeoCoordinates type describes a single instance of a Lon-Lat-Alt (LLA) position.

    Notes
    -----
    The GeoCoordinates type is *not* explicitly referenced by the KML specification;
    rather, it is a construct of convenience for the pyLiveKML package.

    Parameters
    ----------
    lon : float
        The longitude, in decimal degrees
    lat : float
        The latitude, in decimal degrees
    alt : float | None, default = None
        The altitude, in metres

    Attributes
    ----------
    lon : float
        The longitude, in decimal degrees
    lat : float
        The latitude, in decimal degrees
    alt : float | None, default = None
        The altitude, in metres

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

    @property
    def values(self) -> tuple[float, float, float | None]:
        """Get or set the LLA as a tuple.

        Parameters
        ----------
        values : tuple[float, float, float|None] | tuple[float, float]
            The LLA as a 2- or 3-tuple, in lon-lat[-alt] order.

        Returns
        -------
        tuple[float, float, float|None]
            The LLA as a tuple

        """
        return (self.lon, self.lat, self.alt)

    @values.setter
    def values(
        self, value: tuple[float, float, float | None] | tuple[float, float]
    ) -> None:
        if len(value) == 3:
            self.lon, self.lat, self.alt = value
        else:
            self.lon, self.lat, self.alt = (*value[:2], None)

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
