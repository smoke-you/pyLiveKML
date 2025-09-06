"""LookAt module."""

from typing import Sequence

from lxml import etree  # type: ignore

from pyLiveKML.types import AltitudeModeEnum, ViewerOption
from pyLiveKML.objects.Object import (
    _FieldDef,
    Angle180,
    Angle360,
    Angle90,
    AnglePos90,
    NoParse,
)
from pyLiveKML.objects.AbstractView import AbstractView
from pyLiveKML.objects.TimePrimitive import TimePrimitive


class LookAt(AbstractView):
    """A KML `<LookAt>` tag constructor.

    Defines a virtual camera that is associated with any element derived from `Feature`.
    The `LookAt` element positions the "camera" in relation to the object that is being
    viewed. In Google Earth, the view "flies to" this `LookAt` viewpoint when the user
    double-clicks an item in the "Places" panel or double-clicks an icon in the 3D
    viewer.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#lookat

    Parameters
    ----------
    viewer_options : ViewerOption | Iterable[ViewerOption] | None, default = None
        Enable or disable one or more Google Earth view modes.
    time_primitive : TimePrimitive | None, default = None
        Timestamp or timespan assigned to the object.
    lla : tuple[float, float, float], default = (0, 0, 0)
        The longitude, latitude and altitude (in that order, in decimal degrees) of the
        camera position.
    angles : tuple[float, float], default (0, 0)
        The heading, tilt and roll (in that order, in decimal degrees) of the `LookAt`
        facing.
    range : float
        Distance in meters from the point specified by `longitude`, `latitude` and
        `altitude` to the `LookAt` position.
    altitude_mode : AltitudeModeEnum | None, default = None

    Attributes
    ----------
    viewer_options : list[ViewerOption]
        Enable or disable one or more Google Earth view modes.
    time_primitive : TimePrimitive | None
        Timestamp or timespan assigned to the object.
    longitude : float
        The longitude of the `LookAt` position, in decimal degrees.
    latitude : float
        The latitude of the `LookAt` position, in decimal degrees.
    altitude : float
        The altitude of the `LookAt` position, in metres, with respect to `altitude_mode`.
    heading : float
        The heading of the `LookAt` facing, in decimal degrees.
    tilt : float
        The tilt of the `LookAt` facing, in decimal degrees.
    range : float
        Distance in meters from the point specified by `longitude`, `latitude` and
        `altitude` to the `LookAt` position.
    altitude_mode : AltitudeModeEnum | None

    """

    _kml_tag = "LookAt"
    _kml_fields = AbstractView._kml_fields + (
        _FieldDef("longitude", parser=Angle180),
        _FieldDef("latitude", parser=Angle90),
        _FieldDef("altitude"),
        _FieldDef("heading", parser=Angle360),
        _FieldDef("tilt", parser=AnglePos90),
        _FieldDef("range", parser=NoParse),
        _FieldDef("altitude_mode", "gx:altitudeMode"),
    )

    def __init__(
        self,
        viewer_options: Sequence[ViewerOption] | ViewerOption | None = None,
        time_primitive: TimePrimitive | None = None,
        lla: tuple[float, float, float] = (0, 0, 0),
        angles: tuple[float, float] = (0, 0),
        range: float = 0,
        altitude_mode: AltitudeModeEnum | None = None,
    ):
        """LookAt instance constructor."""
        AbstractView.__init__(self, viewer_options, time_primitive)
        self.longitude, self.latitude, self.altitude = lla
        self.heading, self.tilt = angles
        self.range = range
        self.altitude_mode = (
            AltitudeModeEnum.CLAMP_TO_GROUND if altitude_mode is None else altitude_mode
        )
