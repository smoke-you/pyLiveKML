# pyLiveKML: A python library that streams geospatial data using the KML protocol.
# Copyright (C) 2022 smoke-you

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""KML module."""

import enum


class AltitudeModeEnum(enum.Enum):
    """Enumeration of options for KML `<gx:altitudeMode>` tags.

    Generally used in e.g. objects that derive from :class:`pyLiveKML.objects.Geometry`.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#kml-fields

    Notes
    -----
    * For simplicity, all `<altitudeMode>` tags in pyLiveKML have been replaced with
    `<gx:altitudeMode>` tags to ease implementation of the seafloor-based modes.

    """

    CLAMP_TO_SEAFLOOR = "clampToSeaFloor"
    RELATIVE_TO_SEAFLOOR = "relativeToSeaFloor"
    CLAMP_TO_GROUND = "clampToGround"
    RELATIVE_TO_GROUND = "relativeToGround"
    ABSOLUTE = "absolute"


class ColorModeEnum(enum.Enum):
    """Enumeration of options for KML `<colorMode>` tags.

    Specifically for objects that derive from :class:`pyLiveKML.objects.ColorStyle`.

    A value of `RANDOM` applies a random linear scale to the base `<color>` as follows.

    * To achieve a truly random selection of colors, specify a base `<color>` of solid
    white (0xffffffff).
    * If you specify a single color component (for example, a value of 0xff0000ff for
    solid red), random color values for that one component (red) will be selected. In
    this case, the values would range from 0x00 (black) to 0xff (full red).
    * If you specify values for two or for all three color components, a random linear
    scale is applied to each color component, with results ranging from black to the
    maximum values specified for each component.
    * The opacity of a color comes from the alpha component of `<color>` and is never
    randomized.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#kml-fields.

    """

    NORMAL = "normal"
    RANDOM = "random"


class DisplayModeEnum(str, enum.Enum):
    """Enumeration of options for KML `<displayMode>` tags.

    Specifically for :class:`pyLiveKML.objects.BalloonStyle` objects.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#kml-fields.

    """

    DEFAULT = "default"
    HIDE = "hide"


class FlyToModeEnum(enum.Enum):
    """Enumeration of options for KML `<gx:FlyTo>` tags.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#gxflyto.

    """

    BOUNCE = "bounce"
    SMOOTH = "smooth"


class PlayModeEnum(enum.Enum):
    """Enumeration of options for KML `<gx:playMode>` tags.

    Used only by :class:`pyLiveKML.objects.TourControl`.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#gxtourcontrol.

    """

    PAUSE = "pause"


class ViewerOptionEnum(enum.Enum):
    """Enumeration of options for KML `<gx:option>` tags.

    Used only by subclasses of :class:`pyLiveKML.objects.AbstractView`.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#abstractview.

    """

    STREETVIEW = "streetview"
    HISTORICAL_IMAGERY = "historicalimagery"
    SUNLIGHT = "sunlight"
    GROUND_NAVIGATION = "groundnavigation"


class ItemIconModeEnum(str, enum.Enum):
    """Enumeration of options for KML `<ItemIcon><state>` tags.

    Specifically for :class:`pyLiveKML.objects.ListStyle` objects.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#kml-fields.

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
    """Enumeration of options for KML `<listItemType>` tags.

    Specifically for :class:`pyLiveKML.objects.ListStyle` objects.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#kml-fields.

    """

    CHECK = "check"
    CHECK_OFF_ONLY = "checkOffOnly"
    CHECK_HIDE_CHILDREN = "checkHideChildren"
    RADIO_FOLDER = "radioFolder"


class RefreshModeEnum(str, enum.Enum):
    """Enumeration of options for KML `<refreshMode>` tags.

    Specifically for :class:`pyLiveKML.objects.Link` objects.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#kml-fields.

    """

    ON_CHANGE = "onChange"
    ON_INTERVAL = "onInterval"
    ON_EXPIRE = "onExpire"


class StyleStateEnum(str, enum.Enum):
    """Enumeration of options for KML `<Pair><key>` tags.

    Specifically for :class:`pyLiveKML.objects.StyleMap` objects.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#kml-fields.

    """

    NORMAL = "normal"
    HIGHLIGHT = "highlight"


class UnitsEnum(str, enum.Enum):
    """Enumeration of options for KML `<unitsEnum>` tags.

    Specifically for subclasses of :class:`pyLiveKML.objects.Vec2` instances.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#kml-fields.

    """

    FRACTION = "fraction"
    PIXELS = "pixels"
    INSET_PIXELS = "insetPixels"


class ViewRefreshModeEnum(enum.Enum):
    """Enumeration of options for KML `<viewRefreshMode>` tags.

    Specifically for :class:`pyLiveKML.objects.Link` objects.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#kml-fields.

    """

    NEVER = "never"
    ON_STOP = "onStop"
    ON_REQUEST = "onRequest"
    ON_REGION = "onRegion"


class OverlayShapeEnum(enum.Enum):
    """Enumeration of view shape options for KML `<Overlay>` subclass tags.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#photooverlay.

    """

    RECTANGLE = "rectangle"
    CYLINDER = "cylinder"
    SPHERE = "sphere"


class GridOriginEnum(enum.Enum):
    """Enumeration of grid origin options for KML `<Overlay>` subclass tags.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#photooverlay.

    """

    LOWER_LEFT = "lowerLeft"
    UPPER_LEFT = "upperLeft"
