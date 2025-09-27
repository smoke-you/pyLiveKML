# pyLiveKML: A python library that streams geospatial data using the KML protocol.
# Copyright (C) 2022 smoke-you

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
from pyLiveKML.objects.Placemark import Placemark


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
                altitude_mode=(None if alt is None else AltitudeModeEnum.ABSOLUTE),
            ),
            inline_style=Style(
                IconStyle(
                    icon="http://maps.google.com/mapfiles/kml/shapes/track.png",
                    heading=heading,
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
