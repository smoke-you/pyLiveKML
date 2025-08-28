"""Point module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML.GeoCoordinates import GeoCoordinates
from pyLiveKML.KML.KML import AltitudeMode, _FieldDef, NoParse, DumpDirect
from pyLiveKML.KML.KMLObjects.Geometry import Geometry


class Point(Geometry):
    """A Point geometry, as per https://developers.google.com/kml/documentation/kmlreference#point.

    :class:`~pyLiveKML.KML.KMLObjects.Point` objects define a simple geographic location, described a longitude,
    latitude and optional altitude.

    :param GeoCoordinates coordinates: A :class:`~pyLiveKML.KML.GeoCoordinates` object that defines the longitude,
        latitude and optional altitude of the :class:`~pyLiveKML.KML.KMLObjects.Point`.
    :param bool|None extrude: An (optional) flag to indicate whether the :class:`~pyLiveKML.KML.KMLObjects.Point`
        should be shown in GEP connected to the ground with a vertical line.
    :param bool|None altitude_mode: The (optional) :class:`~pyLiveKML.KML.KML.AltitudeMode` that will be applied
        to the :class:`~pyLiveKML.KML.KMLObjects.Point` by GEP.
    """

    _kml_type = "Point"
    _kml_fields = Geometry._kml_fields + (
        _FieldDef("extrude", NoParse, "extrude", DumpDirect),
        _FieldDef("altitude_mode", NoParse, "altitudeMode", DumpDirect),
        _FieldDef("coordinates", NoParse, "coordinates", DumpDirect),
    )

    def __init__(
        self,
        coordinates: GeoCoordinates,
        extrude: bool | None = None,
        altitude_mode: AltitudeMode | None = None,
    ):
        """Point instance constructor."""
        Geometry.__init__(self)
        self.coordinates = coordinates
        self.extrude = extrude
        self.altitude_mode = altitude_mode
