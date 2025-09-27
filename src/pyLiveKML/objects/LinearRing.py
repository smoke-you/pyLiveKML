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

"""LinearRing module."""

from typing import Any, Iterable, Iterator, cast

from lxml import etree  # type: ignore

from pyLiveKML.errors import LinearRingCoordsError
from pyLiveKML.objects.Geometry import Geometry
from pyLiveKML.objects.Object import _FieldDef, _KMLDump, _KMLParser
from pyLiveKML.types import AltitudeModeEnum, GeoCoordinates


class _CoordsParser(_KMLParser):

    @classmethod
    def parse(cls, value: Any) -> Any:
        if isinstance(next(iter(value)), GeoCoordinates):
            result = value
        else:
            result = tuple((GeoCoordinates(*c) for c in value))
        if len(result) < 3:
            raise LinearRingCoordsError(
                "There must be at least three points in the boundary."
            )
        return result


class _CoordsDumper(_KMLDump):

    @classmethod
    def dump(cls, value: Any) -> Any:
        def _build() -> Iterable[str]:
            v = cast(Iterable[GeoCoordinates], value)
            v0 = str(next(iter(v)))
            yield v0
            yield from (str(c) for c in v)
            yield v0

        return " ".join(_build())


class LinearRing(Geometry):
    """A KML `<LinearRing>` geometry tag constructor.

    Defines a closed line string, typically the outer boundary of a `Polygon`.
    Optionally, a `LinearRing` can also be used as the inner boundary of a `Polygon` to
    create holes in the `Polygon`. A `Polygon` can contain multiple `<LinearRing>`
    elements used as inner boundaries.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#linearring.

    Parameters
    ----------
    coordinates : Iterable[GeoCoordinates] | Iterable[tuple[float, float, float]] | Iterable[tuple[float, float]]
        The coordinates of the vertices of the `LinearRing`. Note that there is no need
        to append a final joining coordinate, such that c[0] == c[-1]; c[0] will be
        appended automatically when the coordinates are published.
    altitude_mode : AltitudeModeEnum | None, default = None
        Specifies how altitude components in the `coordinates` attribute are interpreted.
    extrude : bool | None, default = None
        Specifies whether to connect the `LinearRing` to the ground. To extrude this
        geometry, `altitude_mode` must be one of RELATIVE_TO_GROUND,
        RELATIVE_TO_SEAFLOOR or ABSOLUTE. Only the vertices of the `LinearRing` are
        extruded, not the center of the geometry. The vertices are extruded toward
        the center of the Earth's geoid.
    tessellate : bool | None, default = None
        Specifies whether to allow the `LinearRing` to follow the terrain. To enable
        tessellation, `altitude_mode` must be CLAMP_TO_GROUND or CLAMP_TO_SEAFLOOR.
        Very large `LinearRing`s should enable tessellation so that they follow the
        curvature of the earth; otherwise, they may go underground and be hidden.
    altitude_offset : float | None, default = None
        Modifies how the altitude values are rendered. This offset allows you to move an
        entire `LinearRing` up or down as a unit without modifying all the individual
        coordinate values that make up the `LinearRing`. (Although the `LinearRing` is
        displayed using the altitude offset value, the original altitude values are
        preserved in the KML file). Units are in meters.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "LinearRing"
    _kml_fields = Geometry._kml_fields + (
        _FieldDef("altitude_mode", "gx:altitudeMode"),
        _FieldDef("coordinates", parser=_CoordsParser, dumper=_CoordsDumper),
        _FieldDef("extrude"),
        _FieldDef("tessellate"),
        _FieldDef("altitude_offset", "gx:altitudeOffset"),
    )

    def __init__(
        self,
        coordinates: (
            Iterable[GeoCoordinates]
            | Iterable[tuple[float, float, float]]
            | Iterable[tuple[float, float]]
        ),
        altitude_mode: AltitudeModeEnum | None = None,
        extrude: bool | None = None,
        tessellate: bool | None = None,
        altitude_offset: float | None = None,
        **kwargs: Any,
    ):
        """LinearRing instance constructor."""
        Geometry.__init__(self, **kwargs)
        self.altitude_offset = altitude_offset
        self.extrude = extrude
        self.tessellate = tessellate
        self.altitude_mode = altitude_mode
        self._coordinates = list[GeoCoordinates]()
        self.coordinates = coordinates

    @property
    def coordinates(self) -> Iterator[GeoCoordinates]:
        """Retrieve a generator over the `GeoCoordinates` of this `LinearRing`.

        If the property setter is called, replaces the current list of coordinates with
        those provided.

        Parameters
        ----------
        value : Iterable[GeoCoordinates] | Iterable[tuple[float, float, float]] | Iterable[tuple[float, float]]
            The new coordinates for the `LinearRing`.

        :returns: A generator over the `GeoCoordinates` of the `LinearRing`.
        :rtype: Iterator[GeoCoordinate]
        :raises: LinearRingCoordsError
            If less than 3 coordinate values are supplied.

        """
        yield from self._coordinates

    @coordinates.setter
    def coordinates(
        self,
        value: (
            Iterable[GeoCoordinates]
            | Iterable[tuple[float, float, float]]
            | Iterable[tuple[float, float]]
        ),
    ) -> None:
        self._coordinates.clear()
        self._coordinates.extend(cast(Iterable[GeoCoordinates], value))
