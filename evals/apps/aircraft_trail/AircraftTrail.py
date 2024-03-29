from lxml import etree

from .AircraftData import AircraftData
from .AircraftPosition import AircraftPosition
from evals.apps.helpers import description_builder
from src.pyLiveKML.KML.KML import State, ListItemType
from src.pyLiveKML.KML.KMLObjects.Object import Object
from src.pyLiveKML.KML.KMLObjects.Folder import Folder
from src.pyLiveKML.KML.KMLObjects.ListStyle import ListStyle
from src.pyLiveKML.KML.KMLObjects.Style import Style


class AircraftTrail(Folder):
    def update_kml(self, parent: Object, update: etree.Element):
        # calculate trail behaviour **before** generating the update - see note in trail(), below
        self.trail()
        Folder.update_kml(self, parent, update)

    def trail(self):
        if self.state != State.CREATED:
            # If the Folder has not already been created, **do not** process the trail. Otherwise, a <Delete> tag will
            # be generated for a Placemark that does not exist, which will likely cause GEP to throw an error.
            return
        self.__idx += 1
        if self.__idx >= len(self.data):
            self.__idx = 0
        data_point = self.data[self.__idx]
        new_pos = AircraftPosition(data_point)
        new_pos.select(True)
        self.append(new_pos)
        while len(self) > self.trail_sz:
            self.remove(self[0])
        self._description = description_builder(
            src={
                'Transponder': data_point.transponder,
                'Flight': data_point.flight,
                'Position': (data_point.coordinates, 'LLA'),
                'Speed': (f'{data_point.speed:0.0f}', 'km/h'),
                'Heading': (f'{data_point.heading:0.1f}', 'deg'),
                'Timestamp': data_point.timestamp,
            },
            title_color=0x7F007F,
        )
        self.field_changed()

    def __init__(
        self,
        data: list[AircraftData],
        trail_sz: int = 20,
    ):
        Folder.__init__(
            self,
            name=data[0].flight,
            is_open=False,
            styles=[
                Style(
                    list_style=ListStyle(
                        list_item_type=ListItemType.CHECK_HIDE_CHILDREN
                    )
                )
            ],
        )
        self.data = data
        self.trail_sz = trail_sz
        self.__idx: int = -1
