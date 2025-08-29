"""LinearRing module."""

from typing import Iterable, Iterator

from lxml import etree  # type: ignore

from pyLiveKML.KML import AltitudeMode
from pyLiveKML.KML._BaseObject import _FieldDef, NoParse, DumpDirect
from pyLiveKML.KML.GeoCoordinates import GeoCoordinates
from pyLiveKML.KML.KMLObjects.Geometry import Geometry


class LinearRing(Geometry):
    """A LinearRing geometry, as per https://developers.google.com/kml/documentation/kmlreference#linearring.

    :class:`~pyLiveKML.KML.KMLObjects.LinearRing` objects describe a geospatial boundary that is defined by a closed
    sequence of points, where points map to :class:`~pyLiveKML.KML.GeoCoordinates` instances.

    :param Iterable[GeoCoordinates] coordinates: An iterable of :class:`~pyLiveKML.KML.GeoCoordinates` objects, or
        points, that define the boundary of the :class:`~pyLiveKML.KML.KMLObjects.LinearRing`. There should be at
        least three points.
    :param AltitudeMode|None altitude_mode: The (optional) :class:`~pyLiveKML.KML.KML.AltitudeMode` that will
        be applied by GEP to all the points that make up the boundary of the
        :class:`~pyLiveKML.KML.KMLObjects.LinearRing`.
    :param bool|None extrude: An (optional) flag to indicate whether the points that make up the
        boundary of the :class:`~pyLiveKML.KML.KMLObjects.LinearRing` should be shown in GEP connected to the
        ground with vertical lines.
    :param bool|None tessellate: An (optional) flag to indicate whether the
        :class:`~pyLiveKML.KML.KMLObjects.LinearRing` should follow the terrain.
    :param float|None gx_altitude_offset: An (optional) altitude offset, in metres, to be applied to every
        point that makes up the boundary of the :class:`~pyLiveKML.KML.KMLObjects.LinearRing`.
    """

    _kml_type = "LinearRing"
    _kml_fields = Geometry._kml_fields + (
        _FieldDef("altitude_mode", NoParse, "altitudeMode", DumpDirect),
        _FieldDef("extrude", NoParse, "extrude", DumpDirect),
        _FieldDef("tessellate", NoParse, "tessellate", DumpDirect),
        _FieldDef("gx_altitude_offset", NoParse, "gx:altitudeOffset", DumpDirect),
    )

    def __init__(
        self,
        coordinates: Iterable[GeoCoordinates],
        altitude_mode: AltitudeMode | None = None,
        extrude: bool | None = None,
        tessellate: bool | None = None,
        gx_altitude_offset: float | None = None,
    ):
        """LinearRing instance constructor."""
        Geometry.__init__(self)
        self.gx_altitude_offset = gx_altitude_offset
        self.extrude = extrude
        self.tessellate = tessellate
        self.altitude_mode = altitude_mode
        self._coordinates = list[GeoCoordinates]()
        self.coordinates = coordinates

    @property
    def coordinates(self) -> Iterator[GeoCoordinates]:
        """The LLA coordinates of the vertices of the instance.

        A generator to retrieve the :class:`~pyLiveKML.KML.GeoCoordinates` objects that define the boundary of the
        :class:`~pyLiveKML.KML.KMLObjects.LinearRing` object.

        :returns: A generator of :class:`~pyLiveKML.KML.GeoCoordinates` objects.
        """
        yield from self._coordinates

    @coordinates.setter
    def coordinates(self, value: Iterable[GeoCoordinates]) -> None:
        self._coordinates.clear()
        self._coordinates.extend(value)
        if len(self._coordinates) < 3:
            raise ValueError("There must be at least three points in the boundary.")
        self.field_changed()

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""

        def _build() -> Iterable[str]:
            yield from (str(c) for c in self._coordinates)
            yield str(self._coordinates[0])

        super().build_kml(root, with_children)
        if self._coordinates:
            etree.SubElement(root, "coordinates").text = " ".join(_build())
