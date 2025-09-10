"""Region module."""

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import _BaseObject, _DependentDef, _FieldDef, Object
from pyLiveKML.types import AltitudeModeEnum


class LatLonAltBox(_BaseObject):
    """A KML `<LatLonAltBox>` tag constructor.

    A bounding box that describes an area of interest defined by geographic coordinates
    and altitudes.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-region

    Parameters
    ----------
    north : float
        Specifies the latitude of the north edge of the bounding box, in decimal degrees.
    south : float
        Specifies the latitude of the south edge of the bounding box, in decimal degrees.
    east : float
        Specifies the longitude of the east edge of the bounding box, in decimal degrees.
    west : float
        Specifies the longitude of the west edge of the bounding box, in decimal degrees.
    min_altitude : float, default = 0
        Specified in meters (and is affected by the altitude mode specification).
    max_altitude : float, default = 0
        Specified in meters (and is affected by the altitude mode specification).
    altitude_mode : AltitudeModeEnum, default = AltitudeModeEnum.CLAMP_TO_GROUND

    Attributes
    ----------
    Same as parameters.

    """

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
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.min_altitude = min_altitude
        self.max_altitude = max_altitude
        self.altitude_mode = altitude_mode


class LevelOfDetail(_BaseObject):
    """A KML `<Lod>` tag constructor.

    `<Lod>` describes the size of the projected region on the screen that is required in
    order for the region to be considered "active." Also specifies the size of the
    pixel ramp used for fading in (from transparent to opaque) and fading out (from
    opaque to transparent).

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-region
    * https://developers.google.com/kml/documentation/regions
    * https://www.google.com/earth/outreach/tutorials/region.html

    Parameters
    ----------
    min_lod_pixels : float, default = 256
        Defines a square in screen space, with sides of the specified value in pixels.
        For example, 128 defines a square of 128 x 128 pixels. The `region`'s bounding
        box must be larger than this square (and smaller than the `max_lod_pixels`
        square) in order for the `Region` to be active.
    max_lod_pixels : float, default = -1
        Measurement in screen pixels that represents the maximum limit of the visibility
        range for a given Region. A value of -1, the default, indicates "active to
        infinite size."
    min_fade_extent : float, default = 0
        Distance over which the geometry fades, from fully opaque to fully transparent.
        This ramp value, expressed in screen pixels, is applied at the minimum end of the
        LOD (visibility) limits
    max_fade_extent : float, default = 0
        Distance over which the geometry fades, from fully transparent to fully opaque.
        This ramp value, expressed in screen pixels, is applied at the maximum end of the
        LOD (visibility) limits.

    Attributes
    ----------
    Same as parameters.

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
        min_lod_pixels: float = 256,
        max_lod_pixels: float = -1,
        min_fade_extent: float = 0,
        max_fade_extent: float = 0,
    ):
        """Lod instance constructor."""
        super().__init__()
        self.min_lod_pixels = min_lod_pixels
        self.max_lod_pixels = max_lod_pixels
        self.min_fade_extent = min_fade_extent
        self.max_fade_extent = max_fade_extent


class Region(Object):
    """A KML `<Region>` tag constructor.

    A `Region` contains a bounding box (`LatLonAltBox`) that describes an area of
    interest defined by geographic coordinates and altitudes. In addition, a `Region`
    contains an LOD (level of detail) extent (`LevelOfDetail`) that defines a validity
    range of the associated `Region` in terms of projected screen size. A `Region` is
    said to be "active" when the bounding box is within the user's view and the LOD
    requirements are met. Objects associated with a `Region` are drawn only when the
    `Region` is active. When the `view_refresh_mode` is `ON_REGION`, the `Link` or `Icon`
    is loaded only when the `Region` is active. See the "Topics in KML" page on Regions
    for more details. In a `Container` or `NetworkLink` hierarchy, this calculation uses
    the `Region` that is the closest ancestor in the hierarchy.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference
    * https://developers.google.com/kml/documentation/regions

    Parameters
    ----------
    box : LatLonAltBox
        A bounding box that describes an area of interest defined by geographic
        coordinates and altitudes.
    lod : LevelOfDetail
        Describes the size of the projected region on the screen that is required in
        order for the region to be considered "active."

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "Region"
    _kml_depdendents = Object._kml_dependents + (
        _DependentDef("box"),
        _DependentDef("lod"),
    )

    def __init__(
        self,
        box: LatLonAltBox,
        lod: LevelOfDetail,
    ) -> None:
        """Region instance constructor."""
        Object.__init__(self)
        self.box = box
        self.lod = lod
