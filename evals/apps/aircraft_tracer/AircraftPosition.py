from datetime import datetime
from typing import Optional, cast

from apps.helpers import description_builder
from pyLiveKML import GeoCoordinates, AltitudeMode, IconStyle, Placemark, Point, Style


class AircraftPosition(Placemark):

    def __init__(
        self,
        transponder: str,
        flight: str,
        timestamp: datetime,
        lon: float,
        lat: float,
        alt: Optional[float],
        speed: float,
        heading: float,
    ) -> None:
        Placemark.__init__(
            self,
            geometry=Point(
                coordinates=GeoCoordinates(lon, lat, alt),
                altitude_mode=(
                    AltitudeMode.CLAMP_TO_GROUND
                    if alt is None
                    else AltitudeMode.ABSOLUTE
                ),
            ),
            inline_style=Style(
                icon_style=IconStyle(
                    icon="http://maps.google.com/mapfiles/kml/shapes/track.png",
                    heading=heading,
                    scale=1.0,
                )
            ),
        )
        self.transponder = transponder
        self.flight = flight
        self.speed = speed
        self.heading = heading
        self.timestamp = timestamp
        self._description = description_builder(
            src={
                "Transponder": self.transponder,
                "Flight": self.flight,
                "Position": (cast(Point, self.geometry).coordinates.__str__(), "LLA"),
                "Speed": (f"{self.speed:0.0f}", "km/h"),
                "Heading": (f"{self.heading:0.1f}", "deg"),
                "Timestamp": self.timestamp,
            },
            title_color=0x007F7F,
        )

    def __str__(self) -> str:
        return f"{self.transponder},{self.flight},{self.timestamp}"
