from typing import Optional, cast

from .AircraftData import AircraftData
from src.pyLiveKML.KML.GeoCoordinates import GeoCoordinates
from src.pyLiveKML.KML.KML import AltitudeMode
from src.pyLiveKML.KML.KMLObjects.IconStyle import IconStyle
from src.pyLiveKML.KML.KMLObjects.Placemark import Placemark
from src.pyLiveKML.KML.KMLObjects.Point import Point
from src.pyLiveKML.KML.KMLObjects.Style import Style


class AircraftPosition(Placemark):

    def __init__(self, data: AircraftData):
        altitude_mode = (
            AltitudeMode.CLAMP_TO_GROUND
            if data.coordinates.alt is None
            else AltitudeMode.ABSOLUTE
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
    def heading(self) -> Optional[float]:
        return cast(IconStyle, cast(Style, self._styles[0]).icon_style).heading

    @property
    def coordinates(self) -> GeoCoordinates:
        return cast(Point, self.geometry).coordinates
