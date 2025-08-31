"""MultiTrack module."""

from typing import Iterator, Iterable

from lxml import etree  # type: ignore

from pyLiveKML.KML import AltitudeModeEnum
from pyLiveKML.KML._BaseObject import _FieldDef
from pyLiveKML.KMLObjects.Geometry import Geometry
from pyLiveKML.KMLObjects.Object import _ListObject
from pyLiveKML.KMLObjects.Track import Track


class MultiTrack(list[Track], _ListObject, Geometry):
    """A KML 'gx:MultiTrack', per https://developers.google.com/kml/documentation/kmlreference#gxmultitrack."""

    _kml_tag = "gx:MultiTrack"
    _kml_fields = Geometry._kml_fields + (
        _FieldDef("altitude_mode", "gx:altitudeMode"),
        _FieldDef("interpolate", "gx:interpolate"),
    )

    def __init__(
        self,
        altitude_mode: AltitudeModeEnum | None = None,
        interpolate: bool = False,
        tracks: Track | Iterable[Track] | None = None,
    ) -> None:
        """Track instance constructor."""
        Geometry.__init__(self)
        self.altitude_mode = altitude_mode
        self.interpolate = interpolate
        if tracks is not None:
            if isinstance(tracks, Track):
                self.append(tracks)
            else:
                self.extend(tracks)
