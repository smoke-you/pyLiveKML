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

"""GeoRing module."""

from typing import Optional, Iterator

from numpy import ndarray, array
from pyLiveKML import GeoCoordinates, AltitudeModeEnum
from scipy.spatial.transform import Rotation

from .GeoShape import GeoShape


def circle_gen(
    radius: float, rotation: Rotation = None, num_v: int = 32
) -> Iterator[ndarray]:
    """Construct a circle as a set of points."""
    point = array([radius, 0, 0])
    r = Rotation.from_euler("z", 360.0 / num_v, degrees=True)
    for i in range(0, num_v):
        yield rotation.apply(point) if rotation is not None else point
        point = r.apply(point)


class GeoRing(GeoShape):
    """The GeoRing class represents a circular shape with a coaxial internal circular cutout."""

    def __init__(
        self,
        origin: GeoCoordinates,
        outer_radius: float,
        inner_radius: float,
        num_vertices: int = 32,
        border_width: float = 1.0,
        border_color: int = 0xFFFFFFFF,
        fill_color: int = 0xFFFFFFFF,
        name: Optional[str] = None,
        selected: bool = False,
        altitude_mode: AltitudeModeEnum = AltitudeModeEnum.CLAMP_TO_GROUND,
    ):
        """GeoRing instance constructor."""
        GeoShape.__init__(
            self,
            origin=origin,
            outer_bound=list(circle_gen(outer_radius, None, num_vertices)),
            inner_bounds=[
                list(circle_gen(inner_radius, None, num_vertices)),
            ],
            border_width=border_width,
            border_color=border_color,
            fill_color=fill_color,
            name=name,
            selected=selected,
            altitude_mode=altitude_mode,
        )
