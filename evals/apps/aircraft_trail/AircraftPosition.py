"""AircraftPosition module."""

from typing import cast
from pyLiveKML import GeoCoordinates, GxAltitudeModeEnum, IconStyle, Point, Style
from pyLiveKML.KML.KMLObjects.Placemark import Placemark

from .AircraftData import AircraftData


class AircraftPosition(Placemark):
    """Record a single position for an AircraftTrail."""

    def __init__(self, data: AircraftData):
        """AircraftPosition instance constructor."""
        altitude_mode = (
            GxAltitudeModeEnum.CLAMP_TO_GROUND
            if data.coordinates.alt is None
            else GxAltitudeModeEnum.ABSOLUTE
        )
        point = Point(coordinates=data.coordinates, altitude_mode=altitude_mode)
        style = Style(
            icon_style=IconStyle(
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
