"""Polygon module."""

from typing import Iterable, Iterator

from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import AltitudeMode, ObjectState, ArgParser, NoParse, DumpDirect
from pyLiveKML.KML.KMLObjects.Geometry import Geometry
from pyLiveKML.KML.KMLObjects.LinearRing import LinearRing
from pyLiveKML.KML.KMLObjects.Object import Object, ObjectChild


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
        ArgParser("altitude_mode", NoParse, "altitudeMode", DumpDirect),
        ArgParser("extrude", NoParse, "extrude", DumpDirect),
        ArgParser("tessellate", NoParse, "tessellate", DumpDirect),
    )
    def __init__(
        self,
        outer_boundary: LinearRing,
        inner_boundaries: Iterable[LinearRing] | None = None,
        altitude_mode: AltitudeMode | None = None,
        extrude: bool | None = None,
        tessellate: bool | None = None,
    ):
        """Polygon instance constructor."""
        Geometry.__init__(self)
        self._outer_boundary = outer_boundary
        self._inner_boundaries = list[LinearRing]()
        if inner_boundaries:
            self._inner_boundaries.extend(inner_boundaries)
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
        yield ObjectChild(parent=self, child=self.outer_boundary)
        for b in self.inner_boundaries:
            yield ObjectChild(parent=self, child=b)

    @property
    def outer_boundary(self) -> LinearRing:
        """The outer boundary of the instance.

        The :class:`~pyLiveKML.KML.KMLObjects.LinearRing` that defines the outer extents of the
        :class:`~pyLiveKML.KML.KMLObjects.Polygon`.
        """
        return self._outer_boundary

    @outer_boundary.setter
    def outer_boundary(self, value: LinearRing) -> None:
        if self._outer_boundary != value:
            self._outer_boundary = value
            self.field_changed()

    @property
    def inner_boundaries(self) -> Iterator[LinearRing]:
        """The inner boundaries of the instance.

        A generator to retrieve the :class:`~pyLiveKML.KML.KMLObjects.LinearRing` objects that define cutouts within
        the :attr:`outer_boundary`.

        :returns: A generator of :class:`~pyLiveKML.KML.KMLObjects.LinearRing` objects.
        """
        yield from self._inner_boundaries

    def update_kml(self, parent: "Object", update: etree.Element) -> None:
        """Retrieve a complete child <Create>, <Change> or <Delete> KML tag as a child of an <Update> tag.

        Overrides the Object.update_kml() method to correctly handle the boundaries.
        Polygon boundaries are a special case for children, because they *must* be
        wrapped in an additional tag.
        """
        Object.update_kml(self, parent, update)
        if self._outer_boundary.state == ObjectState.CHANGING:
            self._outer_boundary.change_kml(update)
        self._outer_boundary.update_generated()
        for b in self._inner_boundaries:
            if b.state == ObjectState.CHANGING:
                b.change_kml(update)
            b.update_generated()

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        if with_children:
            if self._outer_boundary:
                etree.SubElement(root, "outerBoundaryIs").append(
                    self._outer_boundary.construct_kml()
                )
                if self._outer_boundary._state == ObjectState.IDLE:
                    self._outer_boundary._state = ObjectState.CREATED
            for b in self._inner_boundaries:
                etree.SubElement(root, "innerBoundaryIs").append(b.construct_kml())
                if b._state == ObjectState.IDLE:
                    b._state = ObjectState.CREATED
