"""LineString module."""

from typing import Iterable, Iterator

from lxml import etree  # type: ignore

from pyLiveKML.KML import GxAltitudeModeEnum
from pyLiveKML.KML._BaseObject import _FieldDef
from pyLiveKML.KML.GeoCoordinates import GeoCoordinates
from pyLiveKML.KMLObjects.Geometry import Geometry


class LineString(Geometry):
    """A LineString geometry, as per https://developers.google.com/kml/documentation/kmlreference#linestring.

    :class:`~pyLiveKML.KMLObjects.LineString` objects define an open sequence of points, or
    :class:`~pyLiveKML.KML.GeoCoordinates` such as might make up a track.

    :param Iterable[GeoCoordinates] coordinates: An iterable of :class:`~pyLiveKML.KML.GeoCoordinates` objects, or
        points, that define the :class:`~pyLiveKML.KMLObjects.LineString`. There should be at least two points.
    :param AltitudeMode|None altitude_mode: The (optional) :class:`~pyLiveKML.KML.KML.AltitudeMode` that will be
        applied by GEP to all the points that make up the :class:`~pyLiveKML.KMLObjects.LineString`.
    :param bool|None extrude: An (optional) flag to indicate whether the points that make up the
        :class:`~pyLiveKML.KMLObjects.LineString` should be shown in GEP connected to the ground with vertical
        lines.
    :param bool|None tessellate: An (optional) flag to indicate whether the
        :class:`~pyLiveKML.KMLObjects.LineString` should follow the terrain.
    :param float|None gx_altitude_offset: An (optional) altitude offset (in metres) to be applied to every point
        that makes up the :class:`~pyLiveKML.KMLObjects.LineString`.
    :param int|None gx_draw_order: An (optional) indication of the order in which overlapping
        :class:`~pyLiveKML.KMLObjects.LineString` objects should be drawn.
    """

    _kml_tag = "LineString"
    _kml_fields = Geometry._kml_fields + (
        _FieldDef("altitude_mode", "gx:altitudeMode"),
        _FieldDef("extrude"),
        _FieldDef("tessellate"),
        _FieldDef("gx_altitude_offset", "gx:altitudeOffset"),
        _FieldDef("gx_draw_order", "gx:drawOrder"),
    )

    def __init__(
        self,
        coordinates: (
            Iterable[GeoCoordinates]
            | Iterable[tuple[float, float, float]]
            | Iterable[tuple[float, float]]
        ),
        altitude_mode: GxAltitudeModeEnum | None = None,
        extrude: bool | None = None,
        tessellate: bool | None = None,
        gx_altitude_offset: float | None = None,
        gx_draw_order: int | None = None,
    ):
        """LineString instance constructor."""
        Geometry.__init__(self)
        self.gx_altitude_offset = gx_altitude_offset
        self.extrude = extrude
        self.tessellate = tessellate
        self.altitude_mode = altitude_mode
        self.gx_draw_order = gx_draw_order
        self._coordinates = list[GeoCoordinates]()
        self.coordinates = coordinates

    @property
    def coordinates(self) -> Iterator[GeoCoordinates]:
        """The LLA coordinates of the vertices of the instance.

        A generator to retrieve the :class:`~pyLiveKML.KML.GeoCoordinates` objects that define this
        :class:`~pyLiveKML.KMLObjects.LineString` object.

        :returns: A generator of :class:`~pyLiveKML.KML.GeoCoordinates` objects.
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
        for c in value:
            if isinstance(c, GeoCoordinates):
                self._coordinates.append(c)
            else:
                self._coordinates.append(GeoCoordinates(*c))
        self.field_changed()

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        if self._coordinates:
            etree.SubElement(root, "coordinates").text = " ".join(
                str(c) for c in self._coordinates
            )
