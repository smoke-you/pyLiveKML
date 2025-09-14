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
    MultiGeometry,
    Point,
    Style,
    Placemark,
    TimeSpan,
    ViewerOption,
    ViewerOptionEnum,
)
from pyLiveKML.objects.Object import _BaseObject, ObjectState

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
        g_point = Point(
            coordinates=(*positions[0].coordinates.values[:2], 0),
            altitude_mode=AltitudeModeEnum.CLAMP_TO_GROUND,
            extrude=False,
        )
        style = Style(
            BalloonStyle(bg_color=0x20FF4000),
            IconStyle(
                icon="http://maps.google.com/mapfiles/kml/shapes/track.png",
                heading=positions[0].heading,
                scale=1.0,
            ),
            LabelStyle(color=0xC00000FF),
            LineStyle(color=0xFF0000FF),
        )
        # the example lookat is simpler to use than the camera, so we'll use that instead
        lookat = LookAt(
            lla=positions[0].coordinates,
            tilt=64,
            range=40000,
            altitude_mode=AltitudeModeEnum.ABSOLUTE,
            time_primitive=TimeSpan(positions[0].timestamp, positions[-1].timestamp),
            viewer_options=[
                ViewerOption(ViewerOptionEnum.HISTORICAL_IMAGERY, False),
                ViewerOption(ViewerOptionEnum.STREETVIEW, False),
                ViewerOption(ViewerOptionEnum.SUNLIGHT, False),
            ],
        )
        # the example camera just looks straight down, to avoid having to recalcuate the
        # camera position each update
        # leaving it here as an explanatory note
        camera = Camera(
            lla=(*positions[0].coordinates.values[:2], 50000),
            tilt=0,
            altitude_mode=AltitudeModeEnum.ABSOLUTE,
        )
        Placemark.__init__(
            self,
            geometry=MultiGeometry(
                (
                    point,
                    g_point,
                )
            ),
            name=flight,
            description="",
            snippet="",
            snippet_max_lines=0,
            inline_style=style,
            abstract_view=lookat,
        )
        self._point = point
        self._g_point = g_point
        self._style = style
        self._lookat = lookat
        self._camera = camera
        self._positions = positions
        self._transponder = transponder
        self._flight = flight
        self._pid = -1

    def activate(self, value: bool, cascade: bool = False) -> None:
        """Overridden to calculate the first position for display."""
        if value:
            self._next_position()
        super().activate(value, cascade)

    def synchronized(self) -> None:
        """Overridden to calculate the next position for display."""
        super().synchronized()
        self._next_position()

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

    def _next_position(self) -> None:
        self._pid += 1
        if self._pid >= len(self._positions):
            self._pid = 0
        pos = self._positions[self._pid]
        self._point.coordinates = pos.coordinates
        self._point.altitude_mode = pos.altitude_mode
        self._g_point.coordinates = (*pos.coordinates.values[:2], 0)
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
