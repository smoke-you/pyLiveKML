"""Camera module."""

from typing import Iterable, cast

from lxml import etree  # type: ignore

from pyLiveKML.objects.AbstractView import AbstractView
from pyLiveKML.objects.Object import (
    _FieldDef,
    Angle90,
    Angle180,
    AnglePos180,
    Angle360,
)
from pyLiveKML.objects.TimePrimitive import TimePrimitive
from pyLiveKML.types import AltitudeModeEnum, GeoCoordinates, ViewerOption


class Camera(AbstractView):
    """A KML `<Camera>` tag constructor.

    Defines the virtual camera that views the scene. This element defines the position of
    the camera relative to the Earth's surface as well as the viewing direction of the
    camera. The camera position is defined by `<longitude>`, `<latitude>`, `<altitude>`,
    and either `<altitudeMode>` or `<gx:altitudeMode>`. The viewing direction of the
    camera is defined by `<heading>`, `<tilt>`, and `<roll>`. `<Camera>` can be a child
    element of any `Feature` or of `<NetworkLinkControl>`. A parent element cannot
    contain both a `<Camera>` and a `<LookAt>` at the same time.

    `Camera` provides full six-degrees-of-freedom control over the view, so you can
    position the Camera in space and then rotate it around the X, Y, and Z axes. Most
    importantly, you can tilt the camera view so that you're looking above the horizon
    into the sky.

    `Camera` can also contain a :class:`pyLiveKML.objects.TimePrimitive`
    (`GxTimeSpan` or `GxTimeStamp`, noting the "Gx" variant). Time values in `Camera`
    affect historical imagery, sunlight, and the display of time-stamped features.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#camera
    * https://developers.google.com/kml/documentation/time#abstractviews

    Parameters
    ----------
    lla : GeoCoordinates | tuple[float, float, float|None] | tuple[float, float] | None, default = None
        The longitude, latitude and altitude (in that order, in decimal degrees) of the
        `Camera` position. If `None`, `lon` and `lat` must be supplied or an exception
        will be thrown.
    heading : float, default = 0
        The heading (in decimal degrees) of the `Camera` facing.
    tilt : float, default = 0
        The tilt (in decimal degrees) of the `Camera` facing.
    roll : float, default = 0
        The roll (in decimal degrees) of the `Camera` facing.
    altitude_mode : AltitudeModeEnum | None, default = None
    lon : float | None, default = None
        The longitude (in decimal degrees) of the the `Camera` position. If `None`, `lla`
        must be supplied.
    lat : float | None, default = None
        The latitude (in decimal degrees) of the the `Camera` position. If `None`, `lla`
        must be supplied.
    alt : float | None, default = None
        The altitude (in metres, with respect to `altitude_mode`) of the the `Camera`
        position.
    viewer_options : ViewerOption | Iterable[ViewerOption] | None, default = None
        Enable or disable one or more Google Earth view modes.
    time_primitive : TimePrimitive | None, default = None
        Timestamp or timespan assigned to the object.

    Attributes
    ----------
    viewer_options : list[ViewerOption]
        Enable or disable one or more Google Earth view modes.
    time_primitive : TimePrimitive | None
        Timestamp or timespan assigned to the object.
    lon : float
        The longitude of the camera position, in decimal degrees.
    lat : float
        The latitude of the camera position, in decimal degrees.
    alt : float
        The altitude of the camera position, in metres, with respect to `altitude_mode`.
    heading : float
        The heading of the camera facing, in decimal degrees.
    tilt : float
        The tilt of the camera facing, in decimal degrees.
    roll : float
        The roll of the camera facing, in decimal degrees.
    altitude_mode : AltitudeModeEnum | None

    """

    _kml_tag = "Camera"
    _kml_fields = AbstractView._kml_fields + (
        _FieldDef("lon", "longitude", parser=Angle180),
        _FieldDef("lat", "latitude", parser=Angle90),
        _FieldDef("alt", "altitude"),
        _FieldDef("heading", parser=Angle360),
        _FieldDef("tilt", parser=AnglePos180),
        _FieldDef("roll", parser=Angle180),
        _FieldDef("altitude_mode", "gx:altitudeMode"),
    )

    def __init__(
        self,
        lla: (
            GeoCoordinates
            | tuple[float, float, float | None]
            | tuple[float, float]
            | None
        ) = None,
        heading: float = 0,
        tilt: float = 0,
        roll: float = 0,
        altitude_mode: AltitudeModeEnum | None = None,
        lon: float | None = None,
        lat: float | None = None,
        alt: float | None = None,
        viewer_options: Iterable[ViewerOption] | ViewerOption | None = None,
        time_primitive: TimePrimitive | None = None,
    ):
        """Camera instance constructor."""
        AbstractView.__init__(self, viewer_options, time_primitive)
        self.lon: float
        self.lat: float
        self.alt: float
        if lla is None and (lon is None or lat is None):
            raise ValueError(
                "You must supply either `lla` or `lon` and `lat` (and optionally `alt`)."
            )
        if lla is None:
            self.lon = cast(float, lon)
            self.lat = cast(float, lat)
            self.alt = cast(float, alt)
        else:
            self.lla = lla
        self.heading, self.tilt, self.roll = heading, tilt, roll
        self.altitude_mode = altitude_mode

    @property
    def lla(self) -> tuple[float, float, float]:
        """Get or set the longitude, latitude and altitude as a tuple.

        Parameters
        ----------
        value : GeoCoordinates | tuple[float, float, float|None] | tuple[float, float])
            The longitude, latitude and altitude as a tuple with optional altitude, or as
            `GeoCoordinates`.

        Returns
        -------
        tuple[float, float, float]
            The longitude, latitude and altitude as a tuple of floats.

        """
        return (self.lon, self.lat, self.alt)

    @lla.setter
    def lla(
        self,
        value: GeoCoordinates | tuple[float, float, float | None] | tuple[float, float],
    ) -> None:
        if isinstance(value, GeoCoordinates):
            v = value.values
            self.lon, self.lat = v[:2]
            self.alt = 0 if v[2] is None else v[2]
        elif len(value) >= 3:
            v = value[:3]
            self.lon, self.lat = v[:2]
            self.alt = 0 if v[2] is None else v[2]
        else:
            self.lon, self.lat = value
            self.alt = 0
