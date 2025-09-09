"""Polygon module."""

from typing import Iterable, Iterator

from lxml import etree  # type: ignore

from pyLiveKML.types import AltitudeModeEnum
from pyLiveKML.objects.Object import _FieldDef, _DependentDef, Object, ObjectState
from pyLiveKML.objects.Geometry import Geometry
from pyLiveKML.objects.LinearRing import LinearRing


class _OuterBoundary(Object):
    """Private wrapper class for polygon outer boundaries."""

    _kml_tag = "outerBoundaryIs"
    _kml_dependents = Object._kml_dependents + (_DependentDef("boundary"),)
    _suppress_id = True

    def __init__(self, boundary: LinearRing) -> None:
        super().__init__()
        self.boundary = boundary


class _InnerBoundary(Object):
    """Private wrapper class for polygon inner boundaries."""

    _kml_tag = "innerBoundaryIs"
    _kml_dependents = Object._kml_dependents + (_DependentDef("boundary"),)
    _suppress_id = True

    def __init__(self, boundary: LinearRing) -> None:
        super().__init__()
        self.boundary = boundary


class Polygon(Geometry):
    """A KML `<Polygon>` tag constructor.

    A `Polygon` is defined by an outer boundary and 0 or more inner boundaries. The
    boundaries, in turn, are defined by `LinearRing`s. When a `Polygon` is extruded, its
    boundaries are connected to the ground to form additional polygons, which gives the
    appearance of a building or a box. Extruded `Polygon`s use `PolyStyle` for their
    `color`, `color mode`, and `fill`.

    The `coordinates` for `Polygon`s (or, more precisely, the `LinearRing`s that make up
    `Polygon`s) **must** be specified in counterclockwise order. `Polygon`s follow the
    "right-hand rule," which states that if you place the fingers of your right hand in
    the direction in which the coordinates are specified, your thumb points in the
    general direction of the geometric normal for the `Polygon`. (In 3D graphics, the
    geometric normal is used for lighting and points away from the front face of the
    `Polygon`.) Since Google Earth fills only the front face of `Polygon`s, you will
    achieve the desired effect only when the coordinates are specified in the proper
    order. Otherwise, the `Polygon` will be gray.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#polygon.

    Parameters
    ----------
    outer_boundary : LinearRing
    inner_boundaries : LinearRing | Iterable[LinearRing] | None = None
    altitude_mode : AltitudeModeEnum | None = None
        Specifies how `altitude` attributes in the `coordinates` attribute are
        interpreted.
    extrude : bool | None = None
        Specifies whether to connect the Polygon to the ground. Only the vertices are
        extruded, not the geometry itself; for example, a rectangle turns into a box with
        five faces. The vertices of the `Polygon` are extruded toward the center of the
        Earth's geoid.
    tessellate : bool | None = None
        This field is not used by Polygon.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "Polygon"
    _kml_fields = Geometry._kml_fields + (
        _FieldDef("altitude_mode", "gx:altitudeMode"),
        _FieldDef("extrude"),
        _FieldDef("tessellate"),
    )
    _kml_dependents = Geometry._kml_dependents + (
        _DependentDef("_outer_boundary"),
        _DependentDef("_inner_boundaries"),
    )

    def __init__(
        self,
        outer_boundary: LinearRing,
        inner_boundaries: LinearRing | Iterable[LinearRing] | None = None,
        altitude_mode: AltitudeModeEnum | None = None,
        extrude: bool | None = None,
        tessellate: bool | None = None,
    ):
        """Polygon instance constructor."""
        Geometry.__init__(self)
        self._outer_boundary = _OuterBoundary(outer_boundary)
        self._inner_boundaries = list[_InnerBoundary]()
        self.inner_boundaries = inner_boundaries
        self.extrude = extrude
        self.tessellate = tessellate
        self.altitude_mode = altitude_mode

    @property
    def outer_boundary(self) -> LinearRing:
        """Outer boundary."""
        return self._outer_boundary.boundary

    @outer_boundary.setter
    def outer_boundary(self, value: LinearRing) -> None:
        self._outer_boundary = _OuterBoundary(value)
        self._outer_boundary.boundary._state = ObjectState.CHANGING

    @property
    def inner_boundaries(self) -> Iterator[LinearRing]:
        """Generator across inner boundaries."""
        for b in self._inner_boundaries:
            yield b.boundary

    @inner_boundaries.setter
    def inner_boundaries(self, value: LinearRing | Iterable[LinearRing] | None) -> None:
        self._inner_boundaries.clear()
        if value is not None:
            if isinstance(value, LinearRing):
                self._inner_boundaries.append(_InnerBoundary(value))
            else:
                self._inner_boundaries.extend(map(_InnerBoundary, value))
        for b in self._inner_boundaries:
            b.boundary._state = ObjectState.CHANGING
