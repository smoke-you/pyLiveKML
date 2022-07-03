from typing import Optional, Iterable, Iterator

from lxml import etree

from pyLiveKML.KML.KML import AltitudeMode, State
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
    :param Optional[Iterable[LinearRing]] inner_boundaries: An (optional) iterable of
        :class:`~pyLiveKML.KML.KMLObjects.LinearRing` objects that define any cutouts within the
        :class:`~pyLiveKML.KML.KMLObjects.Polygon`.
    :param Optional[AltitudeMode] altitude_mode: The (optional) :class:`~pyLiveKML.KML.KML.AltitudeMode` that will be
        applied by GEP to all the points that make up the :class:`~pyLiveKML.KML.KMLObjects.Polygon`.
    :param Optional[bool] extrude: An (optional) flag to indicate whether the points that make up the
        :class:`~pyLiveKML.KML.KMLObjects.Polygon` should be shown in GEP connected to the ground with vertical lines.
    :param Optional[bool] tessellate: An (optional) flag to indicate whether the boundaries of the
        :class:`~pyLiveKML.KML.KMLObjects.Polygon` should follow the terrain.
    """

    @property
    def kml_type(self) -> str:
        """Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set the KML tag name to
        'Polygon'"""
        return 'Polygon'

    @property
    def children(self) -> Iterator[ObjectChild]:
        """Overridden from :attr:`pyLiveKML.KML.KMLObjects.Object.Object.children` to yield the children of a
        :class:`~pyLiveKML.KML.KMLObjects.Polygon`, i.e. one or more :class:`~pyLiveKML.KML.KMLObjects.LinearRing`
        instances, being the :attr:`outer_boundary` and zero or more :attr:`inner_boundaries`.
        """
        yield ObjectChild(parent=self, child=self.outer_boundary)
        for b in self._inner_boundaries:
            yield ObjectChild(parent=self, child=b)

    @property
    def outer_boundary(self) -> LinearRing:
        """The :class:`~pyLiveKML.KML.KMLObjects.LinearRing` that defines the outer extents of the
        :class:`~pyLiveKML.KML.KMLObjects.Polygon`.
        """
        return self._outer_boundary

    @outer_boundary.setter
    def outer_boundary(self, value: LinearRing):
        if self._outer_boundary != value:
            self._outer_boundary = value
            self.field_changed()

    @property
    def inner_boundaries(self) -> Iterator[LinearRing]:
        """A generator to retrieve the :class:`~pyLiveKML.KML.KMLObjects.LinearRing` objects that define cutouts within
        the :attr:`outer_boundary`.

        :returns: A generator of :class:`~pyLiveKML.KML.KMLObjects.LinearRing` objects.
        """
        yield from self._inner_boundaries

    @property
    def extrude(self) -> Optional[bool]:
        """True if a vertical line (using the current :class:`~pyLiveKML.KML.KMLObjects.LineStyle`) connects each of
        the :attr:`outer_boundary` and :attr:`inner_boundaries` objects' points to the ground in GEP, False otherwise.
        None implies False.
        """
        return self._extrude

    @extrude.setter
    def extrude(self, value: Optional[bool]):
        if self._extrude != value:
            self._extrude = value
            self.field_changed()

    @property
    def tessellate(self) -> Optional[bool]:
        """True if the inner and outer boundary lines of the :class:`~pyLiveKML.KML.KMLObjects.Polygon` follows the
        terrain in GEP, otherwise False.

        :note: The :attr:`altitude_mode` property must be set to CLAMP_TO_GROUND to enable tessellation.
        """
        return self._tessellate

    @tessellate.setter
    def tessellate(self, value: Optional[bool]):
        if self._tessellate != value:
            self._tessellate = value
            self.field_changed()

    @property
    def altitude_mode(self) -> Optional[AltitudeMode]:
        """An :class:`~pyLiveKML.KML.KML.AltitudeMode` instance that defines how GEP displays the
        :class:`~pyLiveKML.KML.GeoCoordinates` objects that make up the inner and outer boundaries of the
        :class:`~pyLiveKML.KML.KMLObjects.Polygon` and treats their altitudes.
        """
        return self._altitude_mode

    @altitude_mode.setter
    def altitude_mode(self, value: Optional[AltitudeMode]):
        if self._altitude_mode != value:
            self._altitude_mode = value
            self.field_changed()

    def update_kml(self, parent: 'Object', update: etree.Element):
        # overrides the Object.update_kml() method to correctly handle the boundaries
        # Polygon boundaries are a special case for children, because they *must* be wrapped in an additional tag
        Object.update_kml(self, parent, update)
        if self._outer_boundary.state == State.CHANGING:
            self._outer_boundary.change_kml(update)
        self._outer_boundary.update_generated()
        for b in self._inner_boundaries:
            if b.state == State.CHANGING:
                b.change_kml(update)
            b.update_generated()

    def build_kml(self, root: etree.Element, with_children=True):
        if self._extrude is not None:
            etree.SubElement(root, 'extrude').text = str(int(self._extrude))
        if self._tessellate is not None:
            etree.SubElement(root, 'tessellate').text = str(int(self._tessellate))
        if self._altitude_mode is not None:
            etree.SubElement(root, 'altitudeMode').text = self._altitude_mode.value
        if with_children:
            if self._outer_boundary:
                etree.SubElement(root, 'outerBoundaryIs').append(self._outer_boundary.construct_kml())
                if self._outer_boundary._state == State.IDLE:
                    self._outer_boundary._state = State.CREATED
            for b in self._inner_boundaries:
                etree.SubElement(root, 'innerBoundaryIs').append(b.construct_kml())
                if b._state == State.IDLE:
                    b._state = State.CREATED

    def __init__(
            self,
            outer_boundary: LinearRing,
            inner_boundaries: Optional[Iterable[LinearRing]] = None,
            altitude_mode: Optional[AltitudeMode] = None,
            extrude: Optional[bool] = None,
            tessellate: Optional[bool] = None,
    ):
        Geometry.__init__(self)
        self._outer_boundary = outer_boundary
        self._inner_boundaries = list[LinearRing]()
        if inner_boundaries:
            self._inner_boundaries.extend(inner_boundaries)
        self._extrude = extrude
        self._tessellate = tessellate
        self._altitude_mode = altitude_mode
