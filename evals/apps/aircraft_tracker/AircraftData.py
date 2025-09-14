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

"""AircraftData module."""

from datetime import datetime
from typing import Optional

from pyLiveKML import GeoCoordinates, AltitudeModeEnum


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
            AltitudeModeEnum.CLAMP_TO_GROUND
            if alt is None
            else AltitudeModeEnum.ABSOLUTE
        )
        self.timestamp = timestamp
        self.speed = speed
        self.heading = heading
