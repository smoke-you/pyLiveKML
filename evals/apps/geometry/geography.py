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

"""geography module."""

from typing import Iterator

import numpy
from numpy import ndarray
from pyproj import Proj, Transformer
from scipy.spatial.transform import Rotation
from pyLiveKML import GeoCoordinates


ecef = Proj(proj="geocent", ellps="WGS84", datum="WGS84")
lla = Proj(proj="latlong", ellps="WGS84", datum="WGS84")
lla2ecef = Transformer.from_proj(lla, ecef)
ecef2lla = Transformer.from_proj(ecef, lla)


def project_shape(
    shape_3d: list[ndarray], origin: GeoCoordinates
) -> Iterator[GeoCoordinates]:
    """Project a Cartesian shape in the geoid."""
    p_org = lla2ecef.transform(origin.lon, origin.lat, origin.alt)
    r_geo = Rotation.from_euler("zyz", (90, 90 - origin.lat, origin.lon), degrees=True)
    for s in shape_3d:
        yield GeoCoordinates(*(ecef2lla.transform(*(numpy.add(r_geo.apply(s), p_org)))))
