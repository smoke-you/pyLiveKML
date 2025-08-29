"""KML module."""

import enum
from abc import ABC, abstractmethod

from typing import Any, Type

from lxml import etree  # type: ignore

from pyLiveKML.KML.GeoColor import GeoColor

KML_UPDATE_CONTAINER_LIMIT_DEFAULT: int = 100
"""The default value for the container update limit.

The default maximum number of :class:`~pyLiveKML.KML.KMLObjects.Feature` objects that 
will be included in each synchronization update emitted by a 
:class:`~pyLiveKML.KML.NetworkLinkControl` object.
"""


KML_DOCTYPE: str = '<?xml version="1.0" encoding="UTF-8"?>'
"""The XML tag that opens any XML document, including any KML document."""

KML_HEADERS = {"Content-Type": "application/vnd.google-earth.kml+xml"}
"""The headers that should be included when a KML file is tranmitted via HTTP."""

__root_namespace_map = {
    "gx": "http://www.google.com/kml/ext/2.2",
    "kml": "http://www.opengis.net/kml/2.2",
    "atom": "http://www.w3.org/2005/Atom",
}
"""The namespace map that is to applied to all Google Earth KML files."""

__root_attributes = {"xmlns": "http://www.opengis.net/kml/2.2"}
"""The attributes that should be applied to all Google Earth KML files."""


def kml_root_tag() -> etree.Element:
    """Construct the opening <kml> tag, with namespaces, for a KML document.

    :return: The <kml> tag, with namespaces, that encloses the contents of a KML document.
    :rtype: etree.Element
    """
    return etree.Element("kml", nsmap=__root_namespace_map, attrib=__root_attributes)


def with_ns(tag: str) -> str:
    """Output a Clark-notation XML string from a colon-notation XML string.

    If there is no colon in the text, just return the text. Otherwise, split the text
    into two parts at the first colon. Look up the first part as a key in
    `_root_namespace_map` and return the corresponding value, wrapped in {}, with the
    second part of the original text appended.

    For example, "gx:Track" would return "{http://www.google.com/kml/ext/2.2}Track".
    lxml publishes this as a <gx:Track> tag. Ridiculous double-entry nonsense, but it
    works.
    """
    parts = tag.split(":")
    return (
        tag
        if len(parts) < 2
        else f"{{{__root_namespace_map[parts[0]]}}}{':'.join(parts[1:])}"
    )


class AltitudeMode(enum.Enum):
    """Enumeration of options for KML <altitudeMode> tags.

    Generally used in e.g. objects that derive from
    :class:`~pyLiveKML.KML.KMLObjects.Geometry`. Refer to the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """

    CLAMP_TO_GROUND = "clampToGround"
    RELATIVE_TO_GROUND = "relativeToGround"
    ABSOLUTE = "absolute"


class ColorModeEnum(enum.Enum):
    """Enumeration of options for KML <colorMode> tags.

    Specifically for objects that derive from
    :class:`~pyLiveKML.KML.KMLObjects.ColorStyle`. Refer to the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """

    NORMAL = "normal"
    RANDOM = "random"


class DisplayModeEnum(str, enum.Enum):
    """Enumeration of options for KML <displayMode> tags.

    Specifically for :class:`~pyLiveKML.KML.KMLObjects.BalloonStyle` objects. Refer to
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


class GxPlayModeEnum(enum.Enum):
    """Enumeration of options for KML <gx:playMode> tags.

    Used only by `gx:TourControl`. Refer to the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#gxtourcontrol.
    """

    PAUSE = "pause"


class GxViewerOptionEnum(enum.Enum):
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

    Specifically for :class:`~pyLiveKML.KML.KMLObjects.ListStyle` objects. Refer to the
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

    Specifically for :class:`~pyLiveKML.KML.KMLObjects.ListStyle` objects. Refer to the
    KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """

    CHECK = "check"
    CHECK_OFF_ONLY = "checkOffOnly"
    CHECK_HIDE_CHILDREN = "checkHideChildren"
    RADIO_FOLDER = "radioFolder"


class RefreshModeEnum(str, enum.Enum):
    """Enumeration of options for KML <refreshMode> tags.

    Specifically for :class:`~pyLiveKML.KML.KMLObjects.Link` objects. Refer to the
    KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """

    ON_CHANGE = "onChange"
    ON_INTERVAL = "onInterval"
    ON_EXPIRE = "onExpire"


class StyleStateEnum(str, enum.Enum):
    """Enumeration of options for KML <Pair><key> tags.

    Specifically for :class:`~pyLiveKML.KML.KMLObjects.StyleMap` objects. Refer to the
    KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """

    NORMAL = "normal"
    HIGHLIGHT = "highlight"


class UnitsEnum(str, enum.Enum):
    """Enumeration of options for KML <unitsEnum> tags.

    Specifically for :class:`~pyLiveKML.KML.KMLObjects.Vec2` instances in e.g.
    :class:`~pyLiveKML.KML.KMLObjects.IconStyle` objects. Refer to the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """

    FRACTION = "fraction"
    PIXELS = "pixels"
    INSET_PIXELS = "insetPixels"


class ViewRefreshModeEnum(enum.Enum):
    """Enumeration of options for KML <viewRefreshMode> tags.

    Specifically for :class:`~pyLiveKML.KML.KMLObjects.Link` objects. Refer to the
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


class ObjectState(enum.Enum):
    """Enumeration of possible states that objects derived from KML :class:`~pyLiveKML.KML.KMLObjects.Object` may hold.

    The 'State' enumeration is specific to the :mod:`pyLiveKML` package, i.e. it is *not* part of the KML specification.
    """

    IDLE = 0
    CREATING = 1
    CREATED = 2
    CHANGING = 3
    DELETE_CREATED = 4
    DELETE_CHANGED = 5
