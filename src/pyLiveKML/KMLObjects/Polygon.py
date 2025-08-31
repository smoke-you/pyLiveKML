"""Polygon module."""

from typing import Iterable, Iterator

from lxml import etree  # type: ignore

from pyLiveKML.KML import AltitudeModeEnum
from pyLiveKML.KML._BaseObject import _FieldDef
from pyLiveKML.KMLObjects.Geometry import Geometry
from pyLiveKML.KMLObjects.LinearRing import LinearRing
from pyLiveKML.KMLObjects.Object import Object, ObjectChild, _ChildDef


class _OuterBoundary(Object):
    _kml_tag = "outerBoundaryIs"
    _direct_children = Object._direct_children + (_ChildDef("boundary"),)
    _suppress_id = True

    def __init__(self, boundary: LinearRing) -> None:
        super().__init__()
        self.boundary = boundary


class _InnerBoundary(Object):
    _kml_tag = "innerBoundaryIs"
    _direct_children = Object._direct_children + (_ChildDef("boundary"),)
    _suppress_id = True

    def __init__(self, boundary: LinearRing) -> None:
        super().__init__()
        self.boundary = boundary


class Polygon(Geometry):
    """A Polygon geometry, as per https://developers.google.com/kml/documentation/kmlreference#polygon.

    :class:`~pyLiveKML.KMLObjects.Polygon` objects are made up of an outer boundary that is a
    :class:`~pyLiveKML.KMLObjects.LinearRing` and zero or more inner boundaries, each of which is also a
    :class:`~pyLiveKML.KMLObjects.LinearRing`.

    :param LinearRing outer_boundary: A :class:`~pyLiveKML.KMLObjects.LinearRing` that defines the outer extents of
        the :class:`~pyLiveKML.KMLObjects.Polygon`.
    :param Iterable[LinearRing]|None inner_boundaries: An (optional) iterable of
        :class:`~pyLiveKML.KMLObjects.LinearRing` objects that define any cutouts within the
        :class:`~pyLiveKML.KMLObjects.Polygon`.
    :param AltitudeMode|None altitude_mode: The (optional) :class:`~pyLiveKML.KML.KML.AltitudeMode` that will be
        applied by GEP to all the points that make up the :class:`~pyLiveKML.KMLObjects.Polygon`.
    :param bool|None extrude: An (optional) flag to indicate whether the points that make up the
        :class:`~pyLiveKML.KMLObjects.Polygon` should be shown in GEP connected to the ground with vertical lines.
    :param bool|None tessellate: An (optional) flag to indicate whether the boundaries of the
        :class:`~pyLiveKML.KMLObjects.Polygon` should follow the terrain.
    """

    _kml_tag = "Polygon"
    _kml_fields = Geometry._kml_fields + (
        _FieldDef("altitude_mode", "gx:altitudeMode"),
        _FieldDef("extrude"),
        _FieldDef("tessellate"),
    )
    _direct_children = Geometry._direct_children + (
        _ChildDef("outer_boundary"),
        _ChildDef("inner_boundaries"),
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
        return self._outer_boundary.boundary

    @outer_boundary.setter
    def outer_boundary(self, value: LinearRing) -> None:
        self._outer_boundary = _OuterBoundary(value)

    @property
    def inner_boundaries(self) -> Iterator[LinearRing]:
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
