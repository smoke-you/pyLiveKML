from datetime import datetime
from typing import Optional

from evals.apps.helpers import description_builder
from src.pyLiveKML.KML.GeoCoordinates import GeoCoordinates
from src.pyLiveKML.KML.KML import AltitudeMode
from src.pyLiveKML.KML.KMLObjects.IconStyle import IconStyle
from src.pyLiveKML.KML.KMLObjects.Placemark import Placemark
from src.pyLiveKML.KML.KMLObjects.Point import Point
from src.pyLiveKML.KML.KMLObjects.Style import Style


class AircraftPosition(Placemark):
    def __str__(self):
        return f'{self.transponder},{self.flight},{self.timestamp}'

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
    ):
        Placemark.__init__(
            self,
            geometry=Point(
                coordinates=GeoCoordinates(lon, lat, alt),
                altitude_mode=AltitudeMode.CLAMP_TO_GROUND
                if alt is None
                else AltitudeMode.ABSOLUTE,
            ),
            inline_style=Style(
                icon_style=IconStyle(
                    icon='http://maps.google.com/mapfiles/kml/shapes/track.png',
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
                'Transponder': self.transponder,
                'Flight': self.flight,
                'Position': (self.geometry.coordinates.__str__(), 'LLA'),
                'Speed': (f'{self.speed:0.0f}', 'km/h'),
                'Heading': (f'{self.heading:0.1f}', 'deg'),
                'Timestamp': self.timestamp,
            },
            title_color=0x007F7F,
        )
