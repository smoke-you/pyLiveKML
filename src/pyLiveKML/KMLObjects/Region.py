"""Region module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML import AltitudeModeEnum
from pyLiveKML.KML._BaseObject import _BaseObject, _FieldDef
from pyLiveKML.KMLObjects.Object import Object, _ChildDef


class LatLonAltBox(_BaseObject):
    """A bounding box that describes an area of interest defined by geographic coordinates and altitudes."""

    _kml_tag = "LatLonAltBox"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("north"),
        _FieldDef("south"),
        _FieldDef("east"),
        _FieldDef("west"),
        _FieldDef("min_altitude", "minAltitude"),
        _FieldDef("max_altitude", "maxAltitude"),
        _FieldDef("altitude_mode", "gx:altitudeMode"),
    )

    def __init__(
        self,
        region: "Region",
        north: float,
        south: float,
        east: float,
        west: float,
        min_altitude: float = 0,
        max_altitude: float = 0,
        altitude_mode: AltitudeModeEnum = AltitudeModeEnum.CLAMP_TO_GROUND,
    ):
        """LatLonAltBox instance constructor."""
        super().__init__()
        self.region = region
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.min_altitude = min_altitude
        self.max_altitude = max_altitude
        self.altitude_mode = altitude_mode


class Lod(_BaseObject):
    """Lod is an abbreviation for Level of Detail.

    <Lod> describes the size of the projected region on the screen that is required in
    order for the region to be considered "active." Also specifies the size of the
    pixel ramp used for fading in (from transparent to opaque) and fading out (from
    opaque to transparent).
    """

    _kml_tag = "Lod"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("min_lod_pixels", "minLodPixels"),
        _FieldDef("max_lod_pixels", "maxLodPixels"),
        _FieldDef("min_fade_extent", "minFadeExtent"),
        _FieldDef("max_fade_extent", "maxFadeExtent"),
    )

    def __init__(
        self,
        region: "Region",
        min_lod_pixels: float = 256,
        max_lod_pixels: float = -1,
        min_fade_extent: float = 0,
        max_fade_extent: float = 0,
    ):
        """Lod instance constructor."""
        super().__init__()
        self.region = region
        self.min_lod_pixels = min_lod_pixels
        self.max_lod_pixels = max_lod_pixels
        self.min_fade_extent = min_fade_extent
        self.max_fade_extent = max_fade_extent


class Region(Object):
    """A KML 'Region', per https://developers.google.com/kml/documentation/kmlreference."""

    _kml_tag = "Region"
    _direct_children = Object._direct_children + (
        _ChildDef("box"),
        _ChildDef("lod"),
    )

    def __init__(
        self,
        north: float,
        south: float,
        east: float,
        west: float,
        min_altitude: float = 0,
        max_altitude: float = 0,
        altitude_mode: AltitudeModeEnum = AltitudeModeEnum.CLAMP_TO_GROUND,
        min_lod_pixels: float = 256,
        max_lod_pixels: float = -1,
        min_fade_extent: float = 0,
        max_fade_extent: float = 0,
    ) -> None:
        """Region instance constructor."""
        Object.__init__(self)
        self.box = LatLonAltBox(
            self, north, south, east, west, min_altitude, max_altitude, altitude_mode
        )
        self.lod = Lod(
            self, min_lod_pixels, max_lod_pixels, min_fade_extent, max_fade_extent
        )
