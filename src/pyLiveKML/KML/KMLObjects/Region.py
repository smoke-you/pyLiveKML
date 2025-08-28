"""Region module."""

from typing import Iterator

from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import (
    AltitudeMode,
    Angle90,
    Angle180,
    _FieldDef,
    NoParse,
    DumpDirect,
)
from pyLiveKML.KML.KMLObjects.Object import Object, ObjectChild
from pyLiveKML.KML._BaseObject import _BaseObject


class LatLonAltBox(_BaseObject):
    """A bounding box that describes an area of interest defined by geographic coordinates and altitudes."""

    _kml_type = "LatLonAltBox"
    _kml_fields = (
        _FieldDef("north", NoParse, "north", DumpDirect),
        _FieldDef("south", NoParse, "south", DumpDirect),
        _FieldDef("east", NoParse, "east", DumpDirect),
        _FieldDef("west", NoParse, "west", DumpDirect),
        _FieldDef("min_altitude", NoParse, "minAltitude", DumpDirect),
        _FieldDef("max_altitude", NoParse, "maxAltitude", DumpDirect),
        _FieldDef("altitude_mode", NoParse, "altitudeMode", DumpDirect),
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
        altitude_mode: AltitudeMode = AltitudeMode.CLAMP_TO_GROUND,
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

    _kml_type = "Lod"
    _kml_fields = (
        _FieldDef("min_lod_pixels", NoParse, "minLodPixels", DumpDirect),
        _FieldDef("max_lod_pixels", NoParse, "maxLodPixels", DumpDirect),
        _FieldDef("min_fade_extent", NoParse, "minFadeExtent", DumpDirect),
        _FieldDef("max_fade_extent", NoParse, "maxFadeExtent", DumpDirect),
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

    _kml_type = "Region"
    _direct_children = (
        "box",
        "lod",
    )

    def __init__(
        self,
        north: float,
        south: float,
        east: float,
        west: float,
        min_altitude: float = 0,
        max_altitude: float = 0,
        altitude_mode: AltitudeMode = AltitudeMode.CLAMP_TO_GROUND,
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
