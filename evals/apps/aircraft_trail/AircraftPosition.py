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

from typing import cast
from pyLiveKML import (
    AltitudeModeEnum,
    GeoCoordinates,
    IconStyle,
    Placemark,
    Point,
    Style,
)

from .AircraftData import AircraftData


class AircraftPosition(Placemark):
    """Record a single position for an AircraftTrail."""

    def __init__(self, data: AircraftData):
        """AircraftPosition instance constructor."""
        altitude_mode = (
            AltitudeModeEnum.CLAMP_TO_GROUND
            if data.coordinates.alt is None
            else AltitudeModeEnum.ABSOLUTE
        )
        point = Point(coordinates=data.coordinates, altitude_mode=altitude_mode)
        style = Style(
            IconStyle(
                icon="http://maps.google.com/mapfiles/kml/shapes/track.png",
                heading=data.heading,
            )
        )
        Placemark.__init__(self, geometry=point, inline_style=style)
        self.timestamp = data.timestamp
        self.speed = data.speed

    @property
    def heading(self) -> float | None:
        """The heading of the aircraft."""
        return cast(IconStyle, cast(Style, self._styles[0]).icon_style).heading

    @property
    def coordinates(self) -> GeoCoordinates:
        """The position of the aircraft."""
        return cast(Point, self.geometry).coordinates
