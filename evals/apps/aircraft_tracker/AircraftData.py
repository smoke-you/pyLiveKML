"""AircraftData module."""

from datetime import datetime
from typing import Optional

from pyLiveKML import GeoCoordinates, GxAltitudeModeEnum


class AircraftData:
    """Transform raw ADSB exchange data into a Python object."""

    def __init__(
        self,
        timestamp: datetime,
        lon: float,
        lat: float,
        alt: Optional[float],
        speed: float,
        heading: float,
    ):
        """AircraftData instance constructor."""
        self.coordinates = GeoCoordinates(lon, lat, alt)
        self.altitude_mode = (
            GxAltitudeModeEnum.CLAMP_TO_GROUND
            if alt is None
            else GxAltitudeModeEnum.ABSOLUTE
        )
        self.timestamp = timestamp
        self.speed = speed
        self.heading = heading
