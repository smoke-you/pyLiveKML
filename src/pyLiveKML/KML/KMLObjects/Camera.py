"""Camera module."""

from typing import Sequence

from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import (
    Angle90,
    Angle180,
    AnglePos180,
    Angle360,
    AltitudeMode,
    _FieldDef,
    NoParse,
    DumpDirect,
)
from pyLiveKML.KML.KMLObjects.AbstractView import AbstractView
from pyLiveKML.KML.KMLObjects.TimePrimitive import TimePrimitive
from pyLiveKML.KML.ViewerOption import GxViewerOption


class Camera(AbstractView):
    """A KML 'Camera', per https://developers.google.com/kml/documentation/kmlreference#camera."""

    _kml_type = "Camera"
    _kml_fields = AbstractView._kml_fields + (
        _FieldDef("longitude", Angle180, "longitude", DumpDirect),
        _FieldDef("latitude", Angle90, "latitude", DumpDirect),
        _FieldDef("altitude", NoParse, "altitude", DumpDirect),
        _FieldDef("heading", Angle360, "heading", DumpDirect),
        _FieldDef("tilt", AnglePos180, "tilt", DumpDirect),
        _FieldDef("roll", Angle180, "roll", DumpDirect),
        _FieldDef("altitude_mode", NoParse, "altitudeMode", DumpDirect),
    )

    def __init__(
        self,
        viewer_options: Sequence[GxViewerOption] | GxViewerOption | None = None,
        time_primitive: TimePrimitive | None = None,
        longitude: float = 0,
        latitude: float = 0,
        altitude: float = 0,
        heading: float = 0,
        tilt: float = 0,
        roll: float = 0,
        altitude_mode: AltitudeMode | None = None,
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
            AltitudeMode.CLAMP_TO_GROUND if altitude_mode is None else altitude_mode
        )
