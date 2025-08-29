"""Camera module."""

from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML.KML import AltitudeModeEnum
from pyLiveKML.KML._BaseObject import (
    _FieldDef,
    Angle90,
    Angle180,
    AnglePos180,
    Angle360,
)
from pyLiveKML.KML.KMLObjects.AbstractView import AbstractView
from pyLiveKML.KML.KMLObjects.TimePrimitive import TimePrimitive
from pyLiveKML.KML.ViewerOption import GxViewerOption


class Camera(AbstractView):
    """A KML 'Camera', per https://developers.google.com/kml/documentation/kmlreference#camera."""

    _kml_tag = "Camera"
    _kml_fields = AbstractView._kml_fields + (
        _FieldDef("longitude", parser=Angle180),
        _FieldDef("latitude", parser=Angle90),
        _FieldDef("altitude"),
        _FieldDef("heading", parser=Angle360),
        _FieldDef("tilt", parser=AnglePos180),
        _FieldDef("roll", parser=Angle180),
        _FieldDef("altitude_mode", "altitudeMode"),
    )

    def __init__(
        self,
        viewer_options: Iterable[GxViewerOption] | GxViewerOption | None = None,
        time_primitive: TimePrimitive | None = None,
        longitude: float = 0,
        latitude: float = 0,
        altitude: float = 0,
        heading: float = 0,
        tilt: float = 0,
        roll: float = 0,
        altitude_mode: AltitudeModeEnum | None = None,
    ):
        """LookAt instance constructor."""
        AbstractView.__init__(self, viewer_options, time_primitive)
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = altitude
        self.heading = heading
        self.tilt = tilt
        self.roll = roll
        self.altitude_mode = (
            AltitudeModeEnum.CLAMP_TO_GROUND if altitude_mode is None else altitude_mode
        )
