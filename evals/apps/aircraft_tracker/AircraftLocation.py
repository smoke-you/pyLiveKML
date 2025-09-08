"""AircraftLocation module."""

from typing import Optional, Sequence, cast

from lxml import etree  # type: ignore
from pyLiveKML import (
    AltitudeModeEnum,
    BalloonStyle,
    Camera,
    IconStyle,
    LabelStyle,
    LineStyle,
    LookAt,
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
            extrude=True,
        )
        style = Style(
            balloon_style=BalloonStyle(bg_color=0x20FF4000),
            icon_style=IconStyle(
                icon="http://maps.google.com/mapfiles/kml/shapes/track.png",
                heading=positions[0].heading,
                scale=1.0,
            ),
            label_style=LabelStyle(color=0xC00000FF),
            line_style=LineStyle(color=0xFF0000FF),
        )
        # the example lookat is simpler to use than the camera, so we'll use that instead
        lookat = LookAt(
            lla=positions[0].coordinates,
            tilt=64,
            range=40000,
            altitude_mode=AltitudeModeEnum.ABSOLUTE,
        )
        # the example camera just looks straight down, to avoid having to recalcuate the
        # camera position each update
        # leaving it here as an explanatory note
        camera = Camera(
            lla=positions[0].coordinates,
            tilt=0,
            altitude_mode=AltitudeModeEnum.ABSOLUTE,
        )
        camera.alt += 40000
        Placemark.__init__(
            self,
            geometry=point,
            name=flight,
            description="",
            snippet="",
            snippet_max_lines=0,
            inline_style=style,
            abstract_view=lookat,
        )
        self._point = point
        self._style = style
        self._lookat = lookat
        self._camera = camera
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
    def synchronized(self) -> None:
        """Record that a KML update has been emitted."""
        if self._state == ObjectState.CREATING or self._state == ObjectState.CHANGING:
            """Note transition to CHANGING rather than CREATED"""
            self._state = ObjectState.CHANGING
        elif (
            self._state == ObjectState.DELETE_CREATED
            or self._state == ObjectState.DELETE_CHANGED
        ):
            self._state = ObjectState.IDLE
        self._pid += 1
        if self._pid >= len(self._positions):
            self._pid = 0
        pos = self._positions[self._pid]
        self._point.coordinates = pos.coordinates
        self._point.altitude_mode = pos.altitude_mode
        self.description = self._build_description()
        cast(IconStyle, self._style.icon_style).heading = pos.heading
        self._lookat.lla = pos.coordinates
        # self._camera.lla = pos.coordinates
        # self._camera.alt += 40000

    def __str__(self) -> str:
        """Return a string representation."""
        return f"{self.kml_tag}:{self.name}"

    def __repr__(self) -> str:
        """Return a debug representation."""
        return self.__str__()
