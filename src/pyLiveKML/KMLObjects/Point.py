"""Point module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML import AltitudeModeEnum
from pyLiveKML.KML._BaseObject import _FieldDef
from pyLiveKML.KML.GeoCoordinates import GeoCoordinates
from pyLiveKML.KMLObjects.Geometry import Geometry


class Point(Geometry):
    """A Point geometry, as per https://developers.google.com/kml/documentation/kmlreference#point.

    :class:`~pyLiveKML.KMLObjects.Point` objects define a simple geographic location, described a longitude,
    latitude and optional altitude.

    :param GeoCoordinates coordinates: A :class:`~pyLiveKML.KML.GeoCoordinates` object that defines the longitude,
        latitude and optional altitude of the :class:`~pyLiveKML.KMLObjects.Point`.
    :param bool|None extrude: An (optional) flag to indicate whether the :class:`~pyLiveKML.KMLObjects.Point`
        should be shown in GEP connected to the ground with a vertical line.
    :param bool|None altitude_mode: The (optional) :class:`~pyLiveKML.KML.KML.AltitudeMode` that will be applied
        to the :class:`~pyLiveKML.KMLObjects.Point` by GEP.
    """

    _kml_tag = "Point"
    _kml_fields = Geometry._kml_fields + (
        _FieldDef("coordinates"),
        _FieldDef("altitude_mode", "gx:altitudeMode"),
        _FieldDef("extrude"),
    )

    def __init__(
        self,
        coordinates: GeoCoordinates | tuple[float, float, float] | tuple[float, float],
        altitude_mode: AltitudeModeEnum | None = None,
        extrude: bool | None = None,
    ):
        """Point instance constructor."""
        Geometry.__init__(self)
        if isinstance(coordinates, GeoCoordinates):
            self.coordinates = coordinates
        else:
            self.coordinates = GeoCoordinates(*coordinates)
        self.extrude = extrude
        self.altitude_mode = altitude_mode
