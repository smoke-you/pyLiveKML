"""KML module."""

import enum


class AltitudeModeEnum(enum.Enum):
    """Enumeration of options for KML <gx:altitudeMode> tags.

    Generally used in e.g. objects that derive from
    :class:`~pyLiveKML.KMLObjects.Geometry`. Refer to the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.

    :note: For simplicity, all `altitudeMode` tags in pyLiveKML have been replaced with
        `gx:altitudeMode` tags to simplify implementation of the seafloor-based modes.
    """

    CLAMP_TO_SEAFLOOR = "clampToSeaFloor"
    RELATIVE_TO_SEAFLOOR = "relativeToSeaFloor"
    CLAMP_TO_GROUND = "clampToGround"
    RELATIVE_TO_GROUND = "relativeToGround"
    ABSOLUTE = "absolute"


class ColorModeEnum(enum.Enum):
    """Enumeration of options for KML <colorMode> tags.

    Specifically for objects that derive from
    :class:`~pyLiveKML.KMLObjects.ColorStyle`. Refer to the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """

    NORMAL = "normal"
    RANDOM = "random"


class DisplayModeEnum(str, enum.Enum):
    """Enumeration of options for KML <displayMode> tags.

    Specifically for :class:`~pyLiveKML.KMLObjects.BalloonStyle` objects. Refer to
    the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """

    DEFAULT = "default"
    HIDE = "hide"


class FlyToModeEnum(enum.Enum):
    """Enumeration of options for KML <gx:FlyTo> tags.

    Refer to the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#gxflyto.
    """

    BOUNCE = "bounce"
    SMOOTH = "smooth"


class PlayModeEnum(enum.Enum):
    """Enumeration of options for KML <gx:playMode> tags.

    Used only by `gx:TourControl`. Refer to the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#gxtourcontrol.
    """

    PAUSE = "pause"


class ViewerOptionEnum(enum.Enum):
    """Enumeration of options for KML <gx:option> tags.

    Used only by `AbstractView` subclasses. Refer to the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#abstractview.
    """

    STREETVIEW = "streetview"
    HISTORICAL_IMAGERY = "historicalimagery"
    SUNLIGHT = "sunlight"
    GROUND_NAVIGATION = "groundnavigation"


class ItemIconModeEnum(str, enum.Enum):
    """Enumeration of options for KML <ItemIcon><state> tags.

    Specifically for :class:`~pyLiveKML.KMLObjects.ListStyle` objects. Refer to the
    KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """

    OPEN = "open"
    CLOSED = "closed"
    ERROR = "error"
    OPEN_ERROR = "open error"
    CLOSED_ERROR = "closed error"
    OPEN_FETCHING0 = "open fetching0"
    OPEN_FETCHING1 = "open fetching1"
    OPEN_FETCHING2 = "open fetching2"
    CLOSED_FETCHING0 = "closed fetching0"
    CLOSED_FETCHING1 = "closed fetching1"
    CLOSED_FETCHING2 = "closed fetching2"


class ListItemTypeEnum(str, enum.Enum):
    """Enumeration of options for KML <listItemType> tags.

    Specifically for :class:`~pyLiveKML.KMLObjects.ListStyle` objects. Refer to the
    KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """

    CHECK = "check"
    CHECK_OFF_ONLY = "checkOffOnly"
    CHECK_HIDE_CHILDREN = "checkHideChildren"
    RADIO_FOLDER = "radioFolder"


class RefreshModeEnum(str, enum.Enum):
    """Enumeration of options for KML <refreshMode> tags.

    Specifically for :class:`~pyLiveKML.KMLObjects.Link` objects. Refer to the
    KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """

    ON_CHANGE = "onChange"
    ON_INTERVAL = "onInterval"
    ON_EXPIRE = "onExpire"


class StyleStateEnum(str, enum.Enum):
    """Enumeration of options for KML <Pair><key> tags.

    Specifically for :class:`~pyLiveKML.KMLObjects.StyleMap` objects. Refer to the
    KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """

    NORMAL = "normal"
    HIGHLIGHT = "highlight"


class UnitsEnum(str, enum.Enum):
    """Enumeration of options for KML <unitsEnum> tags.

    Specifically for :class:`~pyLiveKML.KMLObjects.Vec2` instances in e.g.
    :class:`~pyLiveKML.KMLObjects.IconStyle` objects. Refer to the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """

    FRACTION = "fraction"
    PIXELS = "pixels"
    INSET_PIXELS = "insetPixels"


class ViewRefreshModeEnum(enum.Enum):
    """Enumeration of options for KML <viewRefreshMode> tags.

    Specifically for :class:`~pyLiveKML.KMLObjects.Link` objects. Refer to the
    KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """

    NEVER = "never"
    ON_STOP = "onStop"
    ON_REQUEST = "onRequest"
    ON_REGION = "onRegion"


class OverlayShapeEnum(enum.Enum):
    """Enumeration of view shape options for KML <Overlay> subclass tags.

    Refer to the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#photooverlay.
    """

    RECTANGLE = "rectangle"
    CYLINDER = "cylinder"
    SPHERE = "sphere"


class GridOriginEnum(enum.Enum):
    """Enumeration of grid origin options for KML <Overlay> subclass tags.

    Refer to the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#photooverlay.
    """

    LOWER_LEFT = "lowerLeft"
    UPPER_LEFT = "upperLeft"
