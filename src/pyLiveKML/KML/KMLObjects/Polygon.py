"""Polygon module."""

from typing import Iterable, Iterator

from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import AltitudeMode, _FieldDef, NoParse, DumpDirect
from pyLiveKML.KML.KMLObjects.Geometry import Geometry
from pyLiveKML.KML.KMLObjects.LinearRing import LinearRing
from pyLiveKML.KML.KMLObjects.Object import Object, ObjectChild


class _OuterBoundary(Object):
    _kml_type = "outerBoundaryIs"
    _direct_children = ("boundary",)
    _suppress_id = True

    def __init__(self, boundary: LinearRing) -> None:
        super().__init__()
        self.boundary = boundary


class _InnerBoundary(Object):
    _kml_type = "innerBoundaryIs"
    _direct_children = ("boundary",)
    _suppress_id = True

    def __init__(self, boundary: LinearRing) -> None:
        super().__init__()
        self.boundary = boundary


class Polygon(Geometry):
    """A Polygon geometry, as per https://developers.google.com/kml/documentation/kmlreference#polygon.

    :class:`~pyLiveKML.KML.KMLObjects.Polygon` objects are made up of an outer boundary that is a
    :class:`~pyLiveKML.KML.KMLObjects.LinearRing` and zero or more inner boundaries, each of which is also a
    :class:`~pyLiveKML.KML.KMLObjects.LinearRing`.

    :param LinearRing outer_boundary: A :class:`~pyLiveKML.KML.KMLObjects.LinearRing` that defines the outer extents of
        the :class:`~pyLiveKML.KML.KMLObjects.Polygon`.
    :param Iterable[LinearRing]|None inner_boundaries: An (optional) iterable of
        :class:`~pyLiveKML.KML.KMLObjects.LinearRing` objects that define any cutouts within the
        :class:`~pyLiveKML.KML.KMLObjects.Polygon`.
    :param AltitudeMode|None altitude_mode: The (optional) :class:`~pyLiveKML.KML.KML.AltitudeMode` that will be
        applied by GEP to all the points that make up the :class:`~pyLiveKML.KML.KMLObjects.Polygon`.
    :param bool|None extrude: An (optional) flag to indicate whether the points that make up the
        :class:`~pyLiveKML.KML.KMLObjects.Polygon` should be shown in GEP connected to the ground with vertical lines.
    :param bool|None tessellate: An (optional) flag to indicate whether the boundaries of the
        :class:`~pyLiveKML.KML.KMLObjects.Polygon` should follow the terrain.
    """

    _kml_type = "Polygon"
    _kml_fields = Geometry._kml_fields + (
        _FieldDef("altitude_mode", NoParse, "altitudeMode", DumpDirect),
        _FieldDef("extrude", NoParse, "extrude", DumpDirect),
        _FieldDef("tessellate", NoParse, "tessellate", DumpDirect),
    )
    _direct_children = ("outer_boundary", "inner_boundaries")

    def __init__(
        self,
        outer_boundary: LinearRing,
        inner_boundaries: LinearRing | Iterable[LinearRing] | None = None,
        altitude_mode: AltitudeMode | None = None,
        extrude: bool | None = None,
        tessellate: bool | None = None,
    ):
        """Polygon instance constructor."""
        Geometry.__init__(self)
        self.outer_boundary = _OuterBoundary(outer_boundary)
        self.inner_boundaries = list[_InnerBoundary]()
        if inner_boundaries is not None:
            if isinstance(inner_boundaries, LinearRing):
                self.inner_boundaries.append(_InnerBoundary(inner_boundaries))
            else:
                self.inner_boundaries.extend(map(_InnerBoundary, inner_boundaries))
        self.extrude = extrude
        self.tessellate = tessellate
        self.altitude_mode = altitude_mode

    @property
    def children(self) -> Iterator[ObjectChild]:
        """The children of the instance.

        Overridden from :attr:`pyLiveKML.KML.KMLObjects.Object.Object.children` to yield the children of a
        :class:`~pyLiveKML.KML.KMLObjects.Polygon`, i.e. one or more :class:`~pyLiveKML.KML.KMLObjects.LinearRing`
        instances, being the :attr:`outer_boundary` and zero or more :attr:`inner_boundaries`.
        """
        yield ObjectChild(parent=self, child=self.outer_boundary.boundary)
        for b in self.inner_boundaries:
            yield ObjectChild(parent=self, child=b.boundary)
