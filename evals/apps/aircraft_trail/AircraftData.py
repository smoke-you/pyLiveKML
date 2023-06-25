from datetime import datetime
from typing import Optional

from src.pyLiveKML.KML.GeoCoordinates import GeoCoordinates


class AircraftData:
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
        self.transponder = transponder
        self.flight = flight
        self.timestamp = timestamp
        self.coordinates = GeoCoordinates(lon, lat, alt)
        self.speed = speed
        self.heading = heading
