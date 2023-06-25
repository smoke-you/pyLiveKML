from datetime import datetime
from typing import Optional

from src.pyLiveKML.KML.GeoCoordinates import GeoCoordinates
from src.pyLiveKML.KML.KML import AltitudeMode


class AircraftData:
    def __init__(
        self,
        timestamp: datetime,
        lon: float,
        lat: float,
        alt: Optional[float],
        speed: float,
        heading: float,
    ):
        self.coordinates = GeoCoordinates(lon, lat, alt)
        self.altitude_mode = (
            AltitudeMode.CLAMP_TO_GROUND if alt is None else AltitudeMode.ABSOLUTE
        )
        self.timestamp = timestamp
        self.speed = speed
        self.heading = heading
