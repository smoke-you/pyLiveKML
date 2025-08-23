"""LineString module."""

from typing import Iterable, Iterator

from lxml import etree  # type: ignore

from pyLiveKML.KML.GeoCoordinates import GeoCoordinates
from pyLiveKML.KML.KML import AltitudeMode
from pyLiveKML.KML.KMLObjects.Geometry import Geometry


class LineString(Geometry):
    """A LineString geometry, as per https://developers.google.com/kml/documentation/kmlreference#linestring.

    :class:`~pyLiveKML.KML.KMLObjects.LineString` objects define an open sequence of points, or
    :class:`~pyLiveKML.KML.GeoCoordinates` such as might make up a track.

    :param Iterable[GeoCoordinates] coordinates: An iterable of :class:`~pyLiveKML.KML.GeoCoordinates` objects, or
        points, that define the :class:`~pyLiveKML.KML.KMLObjects.LineString`. There should be at least two points.
    :param AltitudeMode|None altitude_mode: The (optional) :class:`~pyLiveKML.KML.KML.AltitudeMode` that will be
        applied by GEP to all the points that make up the :class:`~pyLiveKML.KML.KMLObjects.LineString`.
    :param bool|None extrude: An (optional) flag to indicate whether the points that make up the
        :class:`~pyLiveKML.KML.KMLObjects.LineString` should be shown in GEP connected to the ground with vertical
        lines.
    :param bool|None tessellate: An (optional) flag to indicate whether the
        :class:`~pyLiveKML.KML.KMLObjects.LineString` should follow the terrain.
    :param float|None gx_altitude_offset: An (optional) altitude offset (in metres) to be applied to every point
        that makes up the :class:`~pyLiveKML.KML.KMLObjects.LineString`.
    :param int|None gx_draw_order: An (optional) indication of the order in which overlapping
        :class:`~pyLiveKML.KML.KMLObjects.LineString` objects should be drawn.
    """

    _kml_type = "LineString"

    def __init__(
        self,
        coordinates: Iterable[GeoCoordinates],
        altitude_mode: AltitudeMode | None = None,
        extrude: bool | None = None,
        tessellate: bool | None = None,
        gx_altitude_offset: float | None = None,
        gx_draw_order: int | None = None,
    ):
        """LineString instance constructor."""
        Geometry.__init__(self)
        self._gx_altitude_offset: float | None = gx_altitude_offset
        self._extrude: bool | None = extrude
        self._tessellate: bool | None = tessellate
        self._altitude_mode: AltitudeMode | None = altitude_mode
        self._gx_draw_order: int | None = gx_draw_order
        self._coordinates: list[GeoCoordinates] = list[GeoCoordinates]()
        self._coordinates.extend(coordinates)

    @property
    def gx_altitude_offset(self) -> float | None:
        """The altitude offset of the instance in the UI.

        An offset, in metres, that is applied to the altitude of all the points
        (:class:`~pyLiveKML.KML.GeoCoordinates`) that define this
        :class:`~pyLiveKML.KML.KMLObjects.LineString` instance.
        """
        return self._gx_altitude_offset

    @gx_altitude_offset.setter
    def gx_altitude_offset(self, value: float | None) -> None:
        if self._gx_altitude_offset != value:
            self._gx_altitude_offset = value
            self.field_changed()

    @property
    def extrude(self) -> bool | None:
        """Flag indicating whether the vertices of the instance should be drawn connected to ground in the UI.

        True if a vertical line (using the current :class:`~pyLiveKML.KML.KMLObjects.LineStyle`) connects each of
        the :class:`~pyLiveKML.KML.KMLObjects.LineString` objects' points to the ground in GEP, False otherwise.  None
        implies False.
        """
        return self._extrude

    @extrude.setter
    def extrude(self, value: bool | None) -> None:
        if self._extrude != value:
            self._extrude = value
            self.field_changed()

    @property
    def tessellate(self) -> bool | None:
        """Flag indicating whether the vertices of the instance should be displayed tessellated in the UI.

        True if the boundary line of the :class:`~pyLiveKML.KML.KMLObjects.LineString` follows the terrain in GEP,
        otherwise False.

        :note: The :attr:`altitude_mode` property must be set to CLAMP_TO_GROUND to enable tessellation.
        """
        return self._tessellate

    @tessellate.setter
    def tessellate(self, value: bool | None) -> None:
        if self._tessellate != value:
            self._tessellate = value
            self.field_changed()

    @property
    def altitude_mode(self) -> AltitudeMode | None:
        """The altitude mode of the instance in the UI.

        An :class:`~pyLiveKML.KML.KML.AltitudeMode` instance that defines how GEP displays the
        :class:`~pyLiveKML.KML.GeoCoordinates` objects that make up the  :class:`~pyLiveKML.KML.KMLObjects.LineString`
        and treats their altitudes.
        """
        return self._altitude_mode

    @altitude_mode.setter
    def altitude_mode(self, value: AltitudeMode | None) -> None:
        if self._altitude_mode != value:
            self._altitude_mode = value
            self.field_changed()

    @property
    def gx_draw_order(self) -> int | None:
        """The order in which to draw overlapping LineString instances.

        An integer that specifies the draw order when multiple :class:`~pyLiveKML.KML.KMLObjects.LineString` objects
        are drawn over the top of one another in GEP. Lower values are drawn first.
        """
        return self._gx_draw_order

    @gx_draw_order.setter
    def gx_draw_order(self, value: int | None) -> None:
        if self._gx_draw_order != value:
            self._gx_draw_order = value
            self.field_changed()

    @property
    def coordinates(self) -> Iterator[GeoCoordinates]:
        """The LLA coordinates of the vertices of the instance.

        A generator to retrieve the :class:`~pyLiveKML.KML.GeoCoordinates` objects that define this
        :class:`~pyLiveKML.KML.KMLObjects.LineString` object.

        :returns: A generator of :class:`~pyLiveKML.KML.GeoCoordinates` objects.
        """
        yield from self._coordinates

    @coordinates.setter
    def coordinates(self, value: Iterable[GeoCoordinates]) -> None:
        self._coordinates.clear()
        self._coordinates.extend(value)
        self.field_changed()

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        if self._gx_altitude_offset is not None:
            etree.SubElement(root, "gx:altitudeOffset").text = (
                f"{self._gx_altitude_offset:0.1f}"
            )
        if self._extrude is not None:
            etree.SubElement(root, "extrude").text = str(int(self._extrude))
        if self._tessellate is not None:
            etree.SubElement(root, "tessellate").text = str(int(self._tessellate))
        if self._altitude_mode is not None:
            etree.SubElement(root, "altitudeMode").text = self._altitude_mode.value
        if self._gx_draw_order is not None:
            etree.SubElement(root, "gx:drawOrder").text = str(self._gx_draw_order)
        if self._coordinates:
            etree.SubElement(root, "coordinates").text = " ".join(
                c.__str__() for c in self._coordinates
            )
