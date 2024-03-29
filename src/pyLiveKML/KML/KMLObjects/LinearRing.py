from typing import Optional, Iterable, Iterator

from lxml import etree

from ..GeoCoordinates import GeoCoordinates
from ..KML import AltitudeMode
from .Geometry import Geometry


class LinearRing(Geometry):
    """A LinearRing geometry, as per https://developers.google.com/kml/documentation/kmlreference#linearring.
    :class:`~pyLiveKML.KML.KMLObjects.LinearRing` objects describe a geospatial boundary that is defined by a closed
    sequence of points, where points map to :class:`~pyLiveKML.KML.GeoCoordinates` instances.

    :param Iterable[GeoCoordinates] coordinates: An iterable of :class:`~pyLiveKML.KML.GeoCoordinates` objects, or
        points, that define the boundary of the :class:`~pyLiveKML.KML.KMLObjects.LinearRing`. There should be at
        least three points.
    :param Optional[AltitudeMode] altitude_mode: The (optional) :class:`~pyLiveKML.KML.KML.AltitudeMode` that will
        be applied by GEP to all the points that make up the boundary of the
        :class:`~pyLiveKML.KML.KMLObjects.LinearRing`.
    :param Optional[bool] extrude: An (optional) flag to indicate whether the points that make up the
        boundary of the :class:`~pyLiveKML.KML.KMLObjects.LinearRing` should be shown in GEP connected to the
        ground with vertical lines.
    :param Optional[bool] tessellate: An (optional) flag to indicate whether the
        :class:`~pyLiveKML.KML.KMLObjects.LinearRing` should follow the terrain.
    :param Optional[float] gx_altitude_offset: An (optional) altitude offset, in metres, to be applied to every
        point that makes up the boundary of the :class:`~pyLiveKML.KML.KMLObjects.LinearRing`.
    """

    @property
    def kml_type(self) -> str:
        """Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set the KML tag name to
        'LinearRing'"""
        return 'LinearRing'

    @property
    def gx_altitude_offset(self) -> Optional[float]:
        """An offset, in metres, that is applied to the altitude of all the points
        (:class:`~pyLiveKML.KML.GeoCoordinates`) that define the boundary of this
        :class:`~pyLiveKML.KML.KMLObjects.LinearRing` instance.
        """
        return self._gx_altitude_offset

    @gx_altitude_offset.setter
    def gx_altitude_offset(self, value: Optional[float]):
        if self._gx_altitude_offset != value:
            self._gx_altitude_offset = value
            self.field_changed()

    @property
    def extrude(self) -> Optional[bool]:
        """True if a vertical line (using the current :class:`~pyLiveKML.KML.KMLObjects.LineStyle`) connects each of
        the :class:`~pyLiveKML.KML.KMLObjects.LinearRing` objects' points to the ground in GEP, False otherwise.  None
        implies False.
        """
        return self._extrude

    @extrude.setter
    def extrude(self, value: Optional[bool]):
        if self._extrude != value:
            self._extrude = value
            self.field_changed()

    @property
    def tessellate(self) -> Optional[bool]:
        """True if the boundary line of the :class:`~pyLiveKML.KML.KMLObjects.LinearRing` follows the terrain in GEP,
        otherwise False.

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
        :class:`~pyLiveKML.KML.GeoCoordinates` objects that make up the boundary of the
        :class:`~pyLiveKML.KML.KMLObjects.LinearRing` and treats their altitudes.
        """
        return self._altitude_mode

    @altitude_mode.setter
    def altitude_mode(self, value: Optional[AltitudeMode]):
        if self._altitude_mode != value:
            self._altitude_mode = value
            self.field_changed()

    @property
    def coordinates(self) -> Iterator[GeoCoordinates]:
        """A generator to retrieve the :class:`~pyLiveKML.KML.GeoCoordinates` objects that define the boundary of the
        :class:`~pyLiveKML.KML.KMLObjects.LinearRing` object.

        :returns: A generator of :class:`~pyLiveKML.KML.GeoCoordinates` objects.
        """
        yield from self._coordinates

    @coordinates.setter
    def coordinates(self, value: Iterable[GeoCoordinates]):
        self._coordinates.clear()
        self._coordinates.extend(value)
        if len(self._coordinates) < 3:
            raise ValueError('There must be at least three points in the boundary')
        self.field_changed()

    def build_kml(self, root: etree.Element, with_children=True):
        if self._gx_altitude_offset is not None:
            etree.SubElement(root, 'gx:altitudeOffset').text = f'{self._gx_altitude_offset:0.1f}'
        if self._extrude is not None:
            etree.SubElement(root, 'extrude').text = str(int(self._extrude))
        if self._tessellate is not None:
            etree.SubElement(root, 'tessellate').text = str(int(self._tessellate))
        if self._altitude_mode is not None:
            etree.SubElement(root, 'altitudeMode').text = self._altitude_mode.value
        if self._coordinates:
            def build() -> str:
                for c in self._coordinates:
                    yield c.__str__()
                yield self._coordinates[0].__str__()
            etree.SubElement(root, 'coordinates').text = ' '.join(build())

    def __init__(
            self,
            coordinates: Iterable[GeoCoordinates],
            altitude_mode: Optional[AltitudeMode] = None,
            extrude: Optional[bool] = None,
            tessellate: Optional[bool] = None,
            gx_altitude_offset: Optional[float] = None,
    ):
        Geometry.__init__(self)
        self._gx_altitude_offset = gx_altitude_offset
        self._extrude = extrude
        self._tessellate = tessellate
        self._altitude_mode = altitude_mode
        self._coordinates = list[GeoCoordinates]()
        self._coordinates.extend(coordinates)
