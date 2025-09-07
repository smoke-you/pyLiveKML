"""AircraftTrail module."""

from lxml import etree  # type: ignore

from pyLiveKML import Folder, ListItemTypeEnum, ListStyle, Style
from pyLiveKML.objects.Object import ObjectState, _BaseObject

from .AircraftData import AircraftData
from .AircraftPosition import AircraftPosition
from ..helpers import description_builder


class AircraftTrail(Folder):
    """Display the current and previous locations of an aircraft by displaying a trail of the last few points."""

    def __init__(
        self,
        data: list[AircraftData],
        trail_sz: int = 20,
    ) -> None:
        """AircraftTrail instance constructor."""
        Folder.__init__(
            self,
            name=data[0].flight,
            is_open=False,
            styles=[
                Style(
                    list_style=ListStyle(
                        list_item_type=ListItemTypeEnum.CHECK_HIDE_CHILDREN,
                        bg_color=0xFF404000,
                    )
                )
            ],
        )
        self.data = data
        self.trail_sz = trail_sz
        self.snippet = "Aircraft Trail"
        self.__idx: int = -1

    def activate(self, value: bool, cascade: bool = False) -> None:
        """Activate the instance."""
        if value:
            self.clear()
            self._deleted.clear()
            self.force_features_idle()
        return super().activate(value, cascade)

    def create_kml(self, root: etree.Element, parent: _BaseObject) -> etree.Element:
        """Publish create."""
        elem = super().create_kml(root, parent)
        self.trail()
        return elem

    def change_kml(self, root: etree.Element) -> None:
        """Publish change."""
        self.trail()
        super().change_kml(root)

    def trail(self) -> None:
        """Update the trail, adding a new point at the head and removing the tail."""
        if self.state != ObjectState.CREATED:
            # If the Folder has not already been created, **do not** process the trail. Otherwise, a <Delete> tag will
            # be generated for a Placemark that does not exist, which will likely cause GEP to throw an error.
            return
        self.__idx += 1
        if self.__idx >= len(self.data):
            self.__idx = 0
        data_point = self.data[self.__idx]
        new_pos = AircraftPosition(data_point)
        new_pos.activate(True)
        self.append(new_pos)
        while len(self) > self.trail_sz:
            self.remove(self[0])
        self.description = description_builder(
            src={
                "Transponder": data_point.transponder,
                "Flight": data_point.flight,
                "Position": (data_point.coordinates, "LLA"),
                "Speed": (f"{data_point.speed:0.0f}", "km/h"),
                "Heading": (f"{data_point.heading:0.1f}", "deg"),
                "Timestamp": data_point.timestamp,
            },
            title_color=0x7F007F,
        )
