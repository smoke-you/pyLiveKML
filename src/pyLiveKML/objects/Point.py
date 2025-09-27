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

"""Point module."""

from typing import Any

from lxml import etree  # type: ignore

from pyLiveKML.objects.Geometry import Geometry
from pyLiveKML.objects.Object import _FieldDef
from pyLiveKML.types import AltitudeModeEnum, GeoCoordinates


class Point(Geometry):
    """A KML `<Point>` tag constructor.

    A geographic location defined by longitude, latitude, and (optional) altitude. When a
    `Point` is contained by a `Placemark`, the point itself determines the position of
    the `Placemark`'s name and icon. When a `Point` is extruded, it is connected to the
    ground with a line. This "tether" uses the current `LineStyle`.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#point

    Parameters
    ----------
    coordinates : GeoCoordinates | tuple[float, float, float] | tuple[float, float]
        A single tuple consisting of floating point values for longitude, latitude, and
        altitude (in that order). Longitude and latitude values are in decimal degrees
        and are constrained to their circular or half-circular limit respectively.
    altitude_mode : AltitudeModeEnum | None, default = None
        Specifies how altitude components in `coordinates` are interpreted.
    extrude : bool | None, default = None
        Specifies whether to connect the `Point` to the ground with a line. To extrude a
        `Point`, the value for `altitude_mode` must be one of `RELATIVE_TO_GROUND`,
        `RELATIVE_TO_SEAFLOOR` or `ABSOLUTE`. The point is extruded toward the center of
        the Earth's geoid.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "Point"
    _kml_fields = Geometry._kml_fields + (
        _FieldDef("coordinates"),
        _FieldDef("altitude_mode", "gx:altitudeMode"),
        _FieldDef("extrude"),
    )

    def __init__(
        self,
        coordinates: GeoCoordinates | tuple[float, float, float] | tuple[float, float],
        altitude_mode: AltitudeModeEnum | None = None,
        extrude: bool | None = None,
        **kwargs: Any,
    ):
        """Point instance constructor."""
        Geometry.__init__(self, **kwargs)
        self._coordinates: GeoCoordinates
        self.coordinates = coordinates
        self.extrude = extrude
        self.altitude_mode = altitude_mode

    @property
    def coordinates(self) -> GeoCoordinates:
        """Get or set the current `coordinates` of the `Point`.

        Parameters
        ----------
        value : GeoCoordinates | tuple[float, float, float] | tuple[float, float]
            The new coordinates value, expressable as a 2- or 3-tuple of floats for
            convenience.

        Returns
        -------
        GeoCoordinates
            The current `coordinates`, as a `GeoCoordinates` instance.

        """
        return self._coordinates

    @coordinates.setter
    def coordinates(
        self, value: GeoCoordinates | tuple[float, float, float] | tuple[float, float]
    ) -> None:
        if isinstance(value, GeoCoordinates):
            self._coordinates = value
        else:
            self._coordinates = GeoCoordinates(*value)
