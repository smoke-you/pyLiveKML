"""LookAt module."""

from typing import Sequence

from lxml import etree  # type: ignore

from pyLiveKML.KML import GxAltitudeModeEnum
from pyLiveKML.KML._BaseObject import (
    Angle90,
    AnglePos90,
    Angle180,
    Angle360,
    _FieldDef,
    NoParse,
)
from pyLiveKML.KML.KMLObjects.AbstractView import AbstractView
from pyLiveKML.KML.KMLObjects.TimePrimitive import TimePrimitive
from pyLiveKML.KML.ViewerOption import GxViewerOption


class LookAt(AbstractView):
    """A KML 'LookAt', per https://developers.google.com/kml/documentation/kmlreference#lookat."""

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
        viewer_options: Sequence[GxViewerOption] | GxViewerOption | None = None,
        time_primitive: TimePrimitive | None = None,
        longitude: float = 0,
        latitude: float = 0,
        altitude: float = 0,
        heading: float = 0,
        tilt: float = 0,
        range: float = 0,
        altitude_mode: GxAltitudeModeEnum | None = None,
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
            GxAltitudeModeEnum.CLAMP_TO_GROUND if altitude_mode is None else altitude_mode
        )
