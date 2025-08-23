"""AircraftData module."""

from datetime import datetime
from typing import Optional

from pyLiveKML import GeoCoordinates


class AircraftData:
    """Transform raw ADSB exchange data into a Python object."""

    def __init__(
        self,
        transponder: str,
        flight: str,
        timestamp: datetime,
        lon: float,
        lat: float,
        alt: Optional[float],
        speed: Optional[float],
        heading: Optional[float],
    ):
        """AircraftData instance constructor."""
        self.transponder = transponder
        self.flight = flight
        self.timestamp = timestamp
        self.coordinates = GeoCoordinates(lon, lat, alt)
        self.speed = speed
        self.heading = heading
