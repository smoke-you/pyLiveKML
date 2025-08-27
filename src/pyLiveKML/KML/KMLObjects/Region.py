"""Region module."""

from typing import Iterator

from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import (
    AltitudeMode,
    Angle90,
    Angle180,
    ArgParser,
    NoParse,
    DumpDirect,
)
from pyLiveKML.KML.KMLObjects.Object import Object, ObjectChild


class LatLonAltBox(Object):
    """A bounding box that describes an area of interest defined by geographic coordinates and altitudes."""

    _kml_type = "LatLonAltBox"
    _kml_fields = (
        ArgParser("north", NoParse, "north", DumpDirect),
        ArgParser("south", NoParse, "south", DumpDirect),
        ArgParser("east", NoParse, "east", DumpDirect),
        ArgParser("west", NoParse, "west", DumpDirect),
        ArgParser("min_altitude", NoParse, "minAltitude", DumpDirect),
        ArgParser("max_altitude", NoParse, "maxAltitude", DumpDirect),
        ArgParser("altitude_mode", NoParse, "altitudeMode", DumpDirect),
    )
    _suppress_id = True

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
        Object.__init__(self)
        self.region = region
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.min_altitude = min_altitude
        self.max_altitude = max_altitude
        self.altitude_mode = altitude_mode


class Lod(Object):
    """Lod is an abbreviation for Level of Detail.

    <Lod> describes the size of the projected region on the screen that is required in
    order for the region to be considered "active." Also specifies the size of the
    pixel ramp used for fading in (from transparent to opaque) and fading out (from
    opaque to transparent).
    """

    _kml_type = "Lod"
    _kml_fields = (
        ArgParser("min_lod_pixels", NoParse, "minLodPixels", DumpDirect),
        ArgParser("max_lod_pixels", NoParse, "maxLodPixels", DumpDirect),
        ArgParser("min_fade_extent", NoParse, "minFadeExtent", DumpDirect),
        ArgParser("max_fade_extent", NoParse, "maxFadeExtent", DumpDirect),
    )
    _suppress_id = True

    def __init__(
        self,
        region: "Region",
        min_lod_pixels: float = 256,
        max_lod_pixels: float = -1,
        min_fade_extent: float = 0,
        max_fade_extent: float = 0,
    ):
        """Lod instance constructor."""
        self.region = region
        self.min_lod_pixels = min_lod_pixels
        self.max_lod_pixels = max_lod_pixels
        self.min_fade_extent = min_fade_extent
        self.max_fade_extent = max_fade_extent


class Region(Object):
    """A KML 'Region', per https://developers.google.com/kml/documentation/kmlreference."""

    _kml_type = "Region"

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

    @property
    def children(self) -> Iterator[ObjectChild]:
        """The children of the instance."""
        yield ObjectChild(self, self.box)
        yield ObjectChild(self, self.lod)

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        root.append(self.box.construct_kml())
        root.append(self.lod.construct_kml())
