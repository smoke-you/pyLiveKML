"""AircraftPosition module."""

from datetime import datetime
from typing import Optional, cast

from apps.helpers import description_builder
from pyLiveKML import (
    AltitudeModeEnum,
    GeoCoordinates,
    IconStyle,
    Point,
    Style,
    TimeStamp,
)
from pyLiveKML.KML.KMLObjects.Placemark import Placemark


class AircraftPosition(Placemark):
    """Records a single position of an aircraft."""

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
        """AircraftPosition instance constructor."""
        Placemark.__init__(
            self,
            geometry=Point(
                coordinates=GeoCoordinates(lon, lat, alt),
                altitude_mode=(
                    AltitudeModeEnum.CLAMP_TO_GROUND
                    if alt is None
                    else AltitudeModeEnum.ABSOLUTE
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
        self.time_primitive = TimeStamp(timestamp)
        self.description = description_builder(
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
        """Return a string representation."""
        return f"{self.transponder},{self.flight},{self.timestamp}"
