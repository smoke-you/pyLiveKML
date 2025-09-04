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
        viewer_options: Sequence[ViewerOption] | ViewerOption | None = None,
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
