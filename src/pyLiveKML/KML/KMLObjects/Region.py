"""Region module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import AltitudeMode
from pyLiveKML.KML.KMLObjects.Object import Object


class LatLonAltBox(Object):
    """A bounding box that describes an area of interest defined by geographic coordinates and altitudes."""

    _kml_type = "LatLonAltBox"

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
        self._north: float = 0
        self._south: float = 0
        self._east: float = 0
        self._west: float = 0
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self._min_altitude = min_altitude
        self._max_altitude = max_altitude
        self._altitude_mode = altitude_mode

    @property
    def north(self) -> float:
        """Specifies the latitude of the north edge of the bounding box, in decimal degrees from 0 to ±90."""
        return self._north

    @north.setter
    def north(self, value: float) -> None:
        # value = value % 90.0
        if value != self._north:
            self._north = value
            self.region.field_changed()

    @property
    def south(self) -> float:
        """Specifies the latitude of the south edge of the bounding box, in decimal degrees from 0 to ±90."""
        return self._south

    @south.setter
    def south(self, value: float) -> None:
        # value = value % 90.0
        if value != self._south:
            self._south = value
            self.region.field_changed()

    @property
    def east(self) -> float:
        """Specifies the longitude of the east edge of the bounding box, in decimal degrees from 0 to ±180."""
        return self._east

    @east.setter
    def east(self, value: float) -> None:
        # value = value % 180.0
        if value != self._east:
            self._east = value
            self.region.field_changed()

    @property
    def west(self) -> float:
        """Specifies the longitude of the west edge of the bounding box, in decimal degrees from 0 to ±180."""
        return self._west

    @west.setter
    def west(self, value: float) -> None:
        # value = value % 180.0
        if value != self._west:
            self._west = value
            self.region.field_changed()

    @property
    def min_altitude(self) -> float:
        """Specified in meters (and is affected by the altitude mode specification)."""
        return self._min_altitude

    @min_altitude.setter
    def min_altitude(self, value: float) -> None:
        if value != self._min_altitude:
            self._min_altitude = value
            self.region.field_changed()

    @property
    def max_altitude(self) -> float:
        """Specified in meters (and is affected by the altitude mode specification)."""
        return self._max_altitude

    @max_altitude.setter
    def max_altitude(self, value: float) -> None:
        if value != self._max_altitude:
            self._max_altitude = value
            self.region.field_changed()

    @property
    def altitude_mode(self) -> AltitudeMode:
        """The altitude mode of the region."""
        return self._altitude_mode

    @altitude_mode.setter
    def altitude_mode(self, value: AltitudeMode) -> None:
        if value != self._altitude_mode:
            self._altitude_mode = value
            self.region.field_changed()

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        box = etree.SubElement(root, self._kml_type)
        etree.SubElement(box, "north").text = str(self._north)
        etree.SubElement(box, "south").text = str(self._south)
        etree.SubElement(box, "east").text = str(self._east)
        etree.SubElement(box, "west").text = str(self._west)
        etree.SubElement(box, "altitudeMode").text = self._altitude_mode.value
        etree.SubElement(box, "minAltitude").text = str(self._min_altitude)
        etree.SubElement(box, "maxAltitude").text = str(self._max_altitude)


class Lod(Object):
    """Lod is an abbreviation for Level of Detail.

    <Lod> describes the size of the projected region on the screen that is required in
    order for the region to be considered "active." Also specifies the size of the
    pixel ramp used for fading in (from transparent to opaque) and fading out (from
    opaque to transparent).
    """

    _kml_type = "Lod"

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
        self._min_lod_pixels = min_lod_pixels
        self._max_lod_pixels = max_lod_pixels
        self._min_fade_extent = min_fade_extent
        self._max_fade_extent = max_fade_extent

    @property
    def min_lod_pixels(self) -> float:
        """Defines a square in screen space, with sides of the specified value in pixels."""
        return self._min_lod_pixels

    @min_lod_pixels.setter
    def min_lod_pixels(self, value: float) -> None:
        if value != self._min_lod_pixels:
            self._min_lod_pixels = value
            self.region.field_changed()

    @property
    def max_lod_pixels(self) -> float:
        """Measurement in screen pixels that represents the maximum limit of the visibility range for a given Region."""
        return self._max_lod_pixels

    @max_lod_pixels.setter
    def max_lod_pixels(self, value: float) -> None:
        if value != self._max_lod_pixels:
            self._max_lod_pixels = value
            self.region.field_changed()

    @property
    def min_fade_extent(self) -> float:
        """Distance over which the geometry fades, from fully opaque to fully transparent."""
        return self._min_fade_extent

    @min_fade_extent.setter
    def min_fade_extent(self, value: float) -> None:
        if value != self._min_fade_extent:
            self._min_fade_extent = value
            self.region.field_changed()

    @property
    def max_fade_extent(self) -> float:
        """Distance over which the geometry fades, from fully transparent to fully opaque."""
        return self._max_fade_extent

    @max_fade_extent.setter
    def max_fade_extent(self, value: float) -> None:
        if value != self._max_fade_extent:
            self._max_fade_extent = value
            self.region.field_changed()

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        if all(
            map(
                lambda x: x is None,
                (
                    self._min_lod_pixels,
                    self._max_lod_pixels,
                    self._min_fade_extent,
                    self._max_fade_extent,
                ),
            )
        ):
            return
        lod = etree.SubElement(root, self._kml_type)
        etree.SubElement(lod, "minLodPixels").text = str(self._min_lod_pixels)
        etree.SubElement(lod, "maxLodPixels").text = str(self._max_lod_pixels)
        etree.SubElement(lod, "minFadeExtent").text = str(self._min_fade_extent)
        etree.SubElement(lod, "maxFadeExtent").text = str(self._max_fade_extent)


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

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        reg = etree.SubElement(root, self._kml_type)
        self.box.build_kml(reg, with_children)
        self.lod.build_kml(reg, with_children)
