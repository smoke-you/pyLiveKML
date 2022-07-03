import enum

from lxml import etree


KML_UPDATE_CONTAINER_LIMIT_DEFAULT: int = 100
"""The default maximum number of :class:`~pyLiveKML.KML.KMLObjects.Feature` objects that will be included in each 
synchronization update emitted by a :class:`~pyLiveKML.KML.NetworkLinkControl` object.
"""


kml_header: str = '<?xml version="1.0" encoding="UTF-8"?>'
"""The XML tag that opens any XML document, including any KML document.
"""


def kml_tag() -> etree.Element:
    """Construct the opening <kml> tag, with namespaces, for a KML document.

    :return: The <kml> tag, with namespaces, that encloses the contents of a KML document.
    :rtype: etree.Element
    """
    nsmap = {
        'gx': 'http://www.google.com/kml/ext/2.2',
        'kml': 'http://www.opengis.net/kml/2.2',
        'atom': 'http://www.w3.org/2005/Atom',
    }
    attrib = {'xmlns': 'http://www.opengis.net/kml/2.2'}
    return etree.Element('kml', nsmap=nsmap, attrib=attrib)


class AltitudeMode(enum.Enum):
    """Enumeration of options for KML <altitudeMode> tags, generally used in e.g. objects that derive from
    :class:`~pyLiveKML.KML.KMLObjects.Geometry`. Refer to the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """
    CLAMP_TO_GROUND = 'clampToGround'
    RELATIVE_TO_GROUND = 'relativeToGround'
    ABSOLUTE = 'absolute'


class ColorMode(enum.Enum):
    """Enumeration of options for KML <colorMode> tags, specifically for objects that derive from
    :class:`~pyLiveKML.KML.KMLObjects.ColorStyle`. Refer to the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """
    NORMAL = 'normal',
    RANDOM = 'random'


class DisplayMode(enum.Enum):
    """Enumeration of options for KML <displayMode> tags, specifically for
    :class:`~pyLiveKML.KML.KMLObjects.BalloonStyle` objects. Refer to the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """
    DEFAULT = 'default'
    HIDE = 'hide'


class ItemIconMode(enum.Flag):
    """Enumeration of options for KML <ItemIcon><state> tags, specifically for
    :class:`~pyLiveKML.KML.KMLObjects.ListStyle` objects. Refer to the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """
    OPEN = 'open'
    CLOSED = 'closed'
    ERROR = 'error'
    OPEN_ERROR = 'open error'
    CLOSED_ERROR = 'closed error'
    OPEN_FETCHING0 = 'open fetching0'
    OPEN_FETCHING1 = 'open fetching1'
    OPEN_FETCHING2 = 'open fetching2'
    CLOSED_FETCHING0 = 'closed fetching0'
    CLOSED_FETCHING1 = 'closed fetching1'
    CLOSED_FETCHING2 = 'closed fetching2'


class ListItemType(enum.Enum):
    """Enumeration of options for KML <listItemType> tags, specifically for
    :class:`~pyLiveKML.KML.KMLObjects.ListStyle` objects. Refer to the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """
    CHECK = 'check'
    CHECK_OFF_ONLY = 'checkOffOnly'
    CHECK_HIDE_CHILDREN = 'checkHideChildren'
    RADIO_FOLDER = 'radioFolder'


class RefreshMode(enum.Enum):
    """Enumeration of options for KML <refreshMode> tags, specifically for
    :class:`~pyLiveKML.KML.KMLObjects.Link` objects. Refer to the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """
    ON_CHANGE = 'onChange'
    ON_INTERVAL = 'onInterval'
    ON_EXPIRE = 'onExpire'


class StyleState(enum.Enum):
    """Enumeration of options for KML <Pair><key> tags, specifically for
    :class:`~pyLiveKML.KML.KMLObjects.StyleMap` objects. Refer to the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """
    NORMAL = 'normal'
    HIGHLIGHT = 'highlight'


class UnitsEnum(enum.Enum):
    """Enumeration of options for KML <unitsEnum> tags, specifically for :class:`~pyLiveKML.KML.KMLObjects.Vec2`
    instances in e.g. :class:`~pyLiveKML.KML.KMLObjects.IconStyle` objects. Refer to the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """
    FRACTION = 'fraction'
    PIXELS = 'pixels'
    INSET_PIXELS = 'insetPixels'


class ViewRefreshMode(enum.Enum):
    """Enumeration of options for KML <viewRefreshMode> tags, specifically for
    :class:`~pyLiveKML.KML.KMLObjects.Link` objects. Refer to the KML documentation at
    https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """
    NEVER = 'never'
    ON_STOP = 'onStop'
    ON_REQUEST = 'onRequest'
    ON_REGION = 'onRegion'


class Vec2Type(enum.Enum):
    """Enumeration of possible sub-types for KML :class:`~pyLiveKML.KML.KMLObjects.Vec2` objects.  Refer to the KML
    documentation at https://developers.google.com/kml/documentation/kmlreference#kml-fields.
    """
    HOTSPOT = 'hotSpot'


class State(enum.Enum):
    """Enumeration of possible states that objects derived from KML :class:`~pyLiveKML.KML.KMLObjects.Object` may hold.
    The 'State' enumeration is specific to the :mod:`pyLiveKML` package, i.e. it is *not* part of the KML specification.
    """
    IDLE = 0
    CREATING = 1
    CREATED = 2
    CHANGING = 3
    DELETE_CREATED = 4
    DELETE_CHANGED = 5
