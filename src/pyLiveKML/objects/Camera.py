"""Camera module."""

from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML.types import AltitudeModeEnum, ViewerOption
from pyLiveKML.objects.Object import (
    _FieldDef,
    Angle90,
    Angle180,
    AnglePos180,
    Angle360,
)
from pyLiveKML.objects.AbstractView import AbstractView
from pyLiveKML.objects.TimePrimitive import TimePrimitive


class Camera(AbstractView):
    """A KML `<Camera>` tag constructor.

    Defines the virtual camera that views the scene. This element defines the position of
    the camera relative to the Earth's surface as well as the viewing direction of the
    camera. The camera position is defined by `<longitude>`, `<latitude>`, `<altitude>`,
    and either `<altitudeMode>` or `<gx:altitudeMode>`. The viewing direction of the
    camera is defined by `<heading>`, `<tilt>`, and `<roll>`. `<Camera>` can be a child
    element of any `Feature` or of `<NetworkLinkControl>`. A parent element cannot
    contain both a `<Camera>` and a `<LookAt>` at the same time.

    `<Camera>` provides full six-degrees-of-freedom control over the view, so you can
    position the Camera in space and then rotate it around the X, Y, and Z axes. Most
    importantly, you can tilt the camera view so that you're looking above the horizon
    into the sky.

    `<Camera>` can also contain a :class:`pyLiveKML.objects.TimePrimitive`
    (`<gx:TimeSpan>` or `<gx:TimeStamp>`). Time values in Camera affect historical
    imagery, sunlight, and the display of time-stamped features. For more information,
    read Time with AbstractViews in the Time and Animation chapter of the Developer's Guide.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#camera

    Parameters
    ----------
    viewer_options : ViewerOption | Iterable[ViewerOption] | None, default = None
        Enable or disable one or more Google Earth view modes.
    time_primitive : TimePrimitive | None, default = None
        Timestamp or timespan assigned to the object.
    lla : tuple[float, float, float], default = (0, 0, 0)
        The longitude, latitude and altitude (in that order, in decimal degrees) of the
        camera position.
    angles : tuple[float, float, float], default (0, 0, 0)
        The heading, tilt and roll (in that order, in decimal degrees) of the camera
        facing.
    altitude_mode : AltitudeModeEnum | None, default = None

    Attributes
    ----------
    viewer_options : list[ViewerOption]
        Enable or disable one or more Google Earth view modes.
    time_primitive : TimePrimitive | None
        Timestamp or timespan assigned to the object.
    longitude : float
        The longitude of the camera position, in decimal degrees.
    latitude : float
        The latitude of the camera position, in decimal degrees.
    altitude : float
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
        _FieldDef("longitude", parser=Angle180),
        _FieldDef("latitude", parser=Angle90),
        _FieldDef("altitude"),
        _FieldDef("heading", parser=Angle360),
        _FieldDef("tilt", parser=AnglePos180),
        _FieldDef("roll", parser=Angle180),
        _FieldDef("altitude_mode", "gx:altitudeMode"),
    )

    def __init__(
        self,
        viewer_options: Iterable[ViewerOption] | ViewerOption | None = None,
        time_primitive: TimePrimitive | None = None,
        lla: tuple[float, float, float] = (0, 0, 0),
        angles: tuple[float, float, float] = (0, 0, 0),
        altitude_mode: AltitudeModeEnum | None = None,
    ):
        """Camera instance constructor."""
        AbstractView.__init__(self, viewer_options, time_primitive)
        self.longitude, self.latitude, self.altitude = lla
        self.heading, self.tilt, self.roll = angles
        self.altitude_mode = altitude_mode
