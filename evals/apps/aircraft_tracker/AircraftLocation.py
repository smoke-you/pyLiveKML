"""AircraftLocation module."""

from typing import Optional, Sequence

from lxml import etree  # type: ignore
from pyLiveKML import (
    IconStyle,
    Point,
    Style,
    Placemark,
)
from pyLiveKML.objects.Object import ObjectState

from .AircraftData import AircraftData
from ..helpers import description_builder


class AircraftLocation(Placemark):
    """Records a single position of an aircraft."""

    def __init__(
        self, transponder: str, flight: str, positions: Sequence[AircraftData]
    ) -> None:
        """AircraftLocation instance constructor."""
        point = Point(
            coordinates=positions[0].coordinates,
            altitude_mode=positions[0].altitude_mode,
        )
        style = Style(
            icon_style=IconStyle(
                icon="http://maps.google.com/mapfiles/kml/shapes/track.png",
                heading=positions[0].heading,
                scale=1.0,
            )
        )
        Placemark.__init__(self, geometry=point, name=flight, inline_style=style)
        self._point = point
        self._style = style
        self._positions = positions
        self._transponder = transponder
        self._flight = flight
        self._pid = -1
        self._state: ObjectState

    def _build_description(self) -> Optional[str]:
        try:
            pos = self._positions[self._pid]
            descriptors = {
                "Transponder": self._transponder,
                "Flight": self._flight,
                "Position": (self._point.coordinates.__str__(), "LLA"),
                "Speed": (
                    (f"{pos.speed:0.0f}", "km/h")
                    if pos.speed is not None
                    else ("?", "")
                ),
                "Heading": (
                    (f"{pos.heading:0.1f}", "deg")
                    if pos.heading is not None
                    else ("?", "")
                ),
                "Timestamp": f"{pos.timestamp}" if pos.timestamp is not None else "?",
            }
            return description_builder(src=descriptors, title_color=0x7F7F00)
        except Exception:
            return None

    # This method is overridden so that the instance is always ready to provide a Change tag
    def update_generated(self) -> None:
        """Record that a KML update has been emitted."""
        if self._state == ObjectState.CREATING or self._state == ObjectState.CHANGING:
            # self._state = State.CREATED
            """Note transition to CHANGING rather than CREATED"""
            self._state = ObjectState.CHANGING
        elif (
            self._state == ObjectState.DELETE_CREATED
            or self._state == ObjectState.DELETE_CHANGED
        ):
            self._state = ObjectState.IDLE

    # Loop through the positions from 0 to len-1 then restart
    def change_kml(self, root: etree.Element) -> None:
        """Construct a complete <Change> KML tag."""
        self._pid += 1
        if self._pid >= len(self._positions):
            self._pid = 0
        pos = self._positions[self._pid]
        self._point.coordinates = pos.coordinates
        self._point.altitude_mode = pos.altitude_mode
        self._point._state = ObjectState.IDLE
        self._style._state = ObjectState.IDLE
        if self._style.icon_style:
            self._style.icon_style.heading = pos.heading
            self._style.icon_style._state = ObjectState.IDLE

        pm = etree.SubElement(
            root, _tag=self.kml_tag, attrib={"targetId": str(self.id)}
        )
        etree.SubElement(pm, "description").text = self._build_description()
        point = etree.SubElement(
            root, _tag=self._point.kml_tag, attrib={"targetId": str(self._point.id)}
        )
        etree.SubElement(point, "coordinates").text = pos.coordinates.__str__()
        etree.SubElement(point, "altitudeMode").text = pos.altitude_mode.value
        style = etree.SubElement(
            root, _tag=self._style.kml_tag, attrib={"targetId": str(self._style.id)}
        )
        icon_style = etree.SubElement(style, "IconStyle")
        etree.SubElement(icon_style, "heading").text = (
            "0" if pos.heading is None else f"{pos.heading:0.1f}"
        )

    def __str__(self) -> str:
        """Return a string representation."""
        return f"{self.kml_tag}:{self.name}"

    def __repr__(self) -> str:
        """Return a debug representation."""
        return self.__str__()
