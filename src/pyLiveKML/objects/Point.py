"""Point module."""

from lxml import etree  # type: ignore

from pyLiveKML.types import AltitudeModeEnum, GeoCoordinates
from pyLiveKML.objects.Object import _FieldDef
from pyLiveKML.objects.Geometry import Geometry


class Point(Geometry):
    """A KML `<Point>` tag constructor.

    A geographic location defined by longitude, latitude, and (optional) altitude. When a
    `Point` is contained by a `Placemark`, the point itself determines the position of
    the `Placemark`'s name and icon. When a `Point` is extruded, it is connected to the
    ground with a line. This "tether" uses the current `LineStyle`.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#point

    Parameters
    ----------
    coordinates : GeoCoordinates | tuple[float, float, float] | tuple[float, float]
        A single tuple consisting of floating point values for longitude, latitude, and
        altitude (in that order). Longitude and latitude values are in decimal degrees
        and are constrained to their circular or half-circular limit respectively.
    altitude_mode : AltitudeModeEnum | None, default = None
        Specifies how altitude components in `coordinates` are interpreted.
    extrude : bool | None, default = None
        Specifies whether to connect the `Point` to the ground with a line. To extrude a
        `Point`, the value for `altitude_mode` must be one of `RELATIVE_TO_GROUND`,
        `RELATIVE_TO_SEAFLOOR` or `ABSOLUTE`. The point is extruded toward the center of
        the Earth's geoid.

    Attributes
    ----------
    Same as parameters.

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
