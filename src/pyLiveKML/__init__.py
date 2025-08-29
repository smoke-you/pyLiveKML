"""pyLiveKML init module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML import (
    GxAltitudeModeEnum,
    ColorModeEnum,
    DisplayModeEnum,
    FlyToModeEnum,
    GxPlayModeEnum,
    GxViewerOptionEnum,
    ItemIconModeEnum,
    ListItemTypeEnum,
    RefreshModeEnum,
    StyleStateEnum,
    UnitsEnum,
    ViewRefreshModeEnum,
)
from pyLiveKML.KML.errors import errors
from pyLiveKML.KML.GeoColor import GeoColor
from pyLiveKML.KML.GeoCoordinates import GeoCoordinates
from pyLiveKML.KML.KMLObjects.BalloonStyle import BalloonStyle
from pyLiveKML.KML.KMLObjects.Camera import Camera
from pyLiveKML.KML.KMLObjects.Document import Document
from pyLiveKML.KML.KMLObjects.FlyTo import GxFlyTo
from pyLiveKML.KML.KMLObjects.Folder import Folder
from pyLiveKML.KML.KMLObjects.GroundOverlay import GroundOverlay
from pyLiveKML.KML.KMLObjects.Icon import Icon
from pyLiveKML.KML.KMLObjects.IconStyle import IconStyle
from pyLiveKML.KML.KMLObjects.LabelStyle import LabelStyle
from pyLiveKML.KML.KMLObjects.LineString import LineString
from pyLiveKML.KML.KMLObjects.LineStyle import LineStyle
from pyLiveKML.KML.KMLObjects.LinearRing import LinearRing
from pyLiveKML.KML.KMLObjects.Link import Link
from pyLiveKML.KML.KMLObjects.ListStyle import ItemIcon, ListStyle
from pyLiveKML.KML.KMLObjects.LookAt import LookAt
from pyLiveKML.KML.KMLObjects.Model import Alias, Model
from pyLiveKML.KML.KMLObjects.MultiGeometry import MultiGeometry
from pyLiveKML.KML.KMLObjects.NetworkLink import NetworkLink
from pyLiveKML.KML.KMLObjects.PhotoOverlay import PhotoOverlay
from pyLiveKML.KML.KMLObjects.Point import Point
from pyLiveKML.KML.KMLObjects.PolyStyle import PolyStyle
from pyLiveKML.KML.KMLObjects.Polygon import Polygon
from pyLiveKML.KML.KMLObjects.Region import Region
from pyLiveKML.KML.KMLObjects.Schema import Schema, SimpleField
from pyLiveKML.KML.KMLObjects.ScreenOverlay import ScreenOverlay
from pyLiveKML.KML.KMLObjects.SoundCue import GxSoundCue
from pyLiveKML.KML.KMLObjects.Style import Style
from pyLiveKML.KML.KMLObjects.StyleMap import StyleMap
from pyLiveKML.KML.KMLObjects.TimeSpan import TimeSpan, GxTimeSpan
from pyLiveKML.KML.KMLObjects.TimeStamp import TimeStamp, GxTimeStamp
from pyLiveKML.KML.KMLObjects.Tour import GxTour
from pyLiveKML.KML.KMLObjects.TourControl import GxTourControl
from pyLiveKML.KML.KMLObjects.Track import (
    GxTrack,
    TrackAngles,
    TrackCoord,
    TrackElement,
    TrackExtendedData,
)
from pyLiveKML.KML.KMLObjects.Wait import GxWait
from pyLiveKML.KML.NetworkLinkControl import NetworkLinkControl
from pyLiveKML.KML.Vec2 import HotSpot, OverlayXY, ScreenXY, RotationXY, Size
from pyLiveKML.KML.ViewerOption import GxViewerOption

# global imports wrapper
# allows importing any of the instantiable KML objects and helpers from the `pyLiveKML` module
__all__ = [
    "Alias",
    "GxAltitudeModeEnum",
    "BalloonStyle",
    "Camera",
    "ColorModeEnum",
    "DisplayModeEnum",
    "Document",
    "FlyToModeEnum",
    "Folder",
    "GeoColor",
    "GeoCoordinates",
    "GroundOverlay",
    "GxFlyTo",
    "GxPlayModeEnum",
    "GxSoundCue",
    "GxTimeSpan",
    "GxTimeStamp",
    "GxTour",
    "GxTourControl",
    "GxTrack",
    "GxViewerOption",
    "GxViewerOptionEnum",
    "GxWait",
    "HotSpot",
    "Icon",
    "IconStyle",
    "ItemIcon",
    "ItemIconModeEnum",
    "KML_DOCTYPE",
    "KML_HEADERS",
    "KML_UPDATE_CONTAINER_LIMIT_DEFAULT",
    "LabelStyle",
    "LineString",
    "LineStyle",
    "LinearRing",
    "Link",
    "ListItemTypeEnum",
    "ListStyle",
    "LookAt",
    "Model",
    "MultiGeometry",
    "NetworkLink",
    "NetworkLinkControl",
    "OverlayXY",
    "PhotoOverlay",
    "Point",
    "PolyStyle",
    "Polygon",
    "RefreshModeEnum",
    "Region",
    "RotationXY",
    "Schema",
    "ScreenOverlay",
    "ScreenXY",
    "SimpleField",
    "Size",
    "Style",
    "StyleMap",
    "StyleStateEnum",
    "TimeSpan",
    "TimeStamp",
    "TrackAngles",
    "TrackCoord",
    "TrackElement",
    "TrackExtendedData",
    "UnitsEnum",
    "ViewRefreshModeEnum",
    "errors",
    "kml_root_tag",
]


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


