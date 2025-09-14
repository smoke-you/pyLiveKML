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

"""GeoEllipse module."""

import math
from typing import Optional, Iterator

from numpy import ndarray, array
from scipy.spatial.transform import Rotation
from pyLiveKML import GeoCoordinates, AltitudeModeEnum

from .GeoShape import GeoShape


def ellipse_gen(
    x_rad: float,
    y_rad: float,
    rotation: Optional[Rotation] = None,
    num_vertices: int = 32,
) -> Iterator[ndarray]:
    """Construct an ellipse as a set of points."""
    step = 2 * math.pi / num_vertices
    angle = -step
    for i in range(0, num_vertices):
        angle += step
        point = array([x_rad * math.cos(angle), y_rad * math.sin(angle), 0])
        if rotation is not None:
            point = rotation.apply(point)
        yield point


class GeoEllipse(GeoShape):
    """The GeoEllipse class represents a simple ellipse."""

    def __init__(
        self,
        origin: GeoCoordinates,
        x_radius: float,
        y_radius: float,
        rotation: Optional[Rotation] = None,
        num_vertices: int = 32,
        border_width: float = 1.0,
        border_color: int = 0xFFFFFFFF,
        fill_color: int = 0xFFFFFFFF,
        name: Optional[str] = None,
        selected: bool = False,
        altitude_mode: AltitudeModeEnum = AltitudeModeEnum.CLAMP_TO_GROUND,
    ):
        """GeoEllipse instance constructor."""
        GeoShape.__init__(
            self,
            origin=origin,
            outer_bound=list(ellipse_gen(x_radius, y_radius, rotation, num_vertices)),
            inner_bounds=None,
            border_width=border_width,
            border_color=border_color,
            fill_color=fill_color,
            name=name,
            selected=selected,
            altitude_mode=altitude_mode,
        )
