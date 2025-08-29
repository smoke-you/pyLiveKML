"""LookAt module."""

from typing import Sequence

from lxml import etree  # type: ignore

from pyLiveKML.KML import AltitudeModeEnum
from pyLiveKML.KML._BaseObject import (
    Angle90,
    AnglePos90,
    Angle180,
    Angle360,
    _FieldDef,
    NoParse,
    DumpDirect,
)
from pyLiveKML.KML.KMLObjects.AbstractView import AbstractView
from pyLiveKML.KML.KMLObjects.TimePrimitive import TimePrimitive
from pyLiveKML.KML.ViewerOption import GxViewerOption


class LookAt(AbstractView):
    """A KML 'LookAt', per https://developers.google.com/kml/documentation/kmlreference#lookat."""

    _kml_tag = "LookAt"
    _kml_fields = AbstractView._kml_fields + (
        _FieldDef("longitude", Angle180, "longitude", DumpDirect),
        _FieldDef("latitude", Angle90, "latitude", DumpDirect),
        _FieldDef("altitude", NoParse, "altitude", DumpDirect),
        _FieldDef("heading", Angle360, "heading", DumpDirect),
        _FieldDef("tilt", AnglePos90, "tilt", DumpDirect),
        _FieldDef("range", NoParse, "range", DumpDirect),
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
        range: float = 0,
        altitude_mode: AltitudeModeEnum | None = None,
    ):
        """LookAt instance constructor."""
        AbstractView.__init__(self, viewer_options, time_primitive)
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = altitude
        self.heading = heading
        self.tilt = tilt
        self.range = range
        self.altitude_mode = (
            AltitudeModeEnum.CLAMP_TO_GROUND if altitude_mode is None else altitude_mode
        )
