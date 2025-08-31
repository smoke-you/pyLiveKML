"""pyLiveKML init module."""

from pyLiveKML.KML.utils import (
    kml_root_tag,
    KML_DOCTYPE,
    KML_HEADERS,
    KML_UPDATE_CONTAINER_LIMIT_DEFAULT,
)
from pyLiveKML.KML import (
    AltitudeModeEnum,
    AltitudeModeEnum as AltitudeModeEnum,
    ColorModeEnum,
    DisplayModeEnum,
    FlyToModeEnum,
    PlayModeEnum,
    ViewerOptionEnum,
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
from pyLiveKML.KML.NetworkLinkControl import NetworkLinkControl
from pyLiveKML.KML.Vec2 import HotSpot, OverlayXY, ScreenXY, RotationXY, Size
from pyLiveKML.KML.ViewerOption import ViewerOption
from pyLiveKML.KMLObjects.BalloonStyle import BalloonStyle
from pyLiveKML.KMLObjects.Camera import Camera
from pyLiveKML.KMLObjects.Document import Document
from pyLiveKML.KMLObjects.FlyTo import FlyTo
from pyLiveKML.KMLObjects.Folder import Folder
from pyLiveKML.KMLObjects.GroundOverlay import GroundOverlay
from pyLiveKML.KMLObjects.Icon import Icon
from pyLiveKML.KMLObjects.IconStyle import IconStyle
from pyLiveKML.KMLObjects.LabelStyle import LabelStyle
from pyLiveKML.KMLObjects.LineString import LineString
from pyLiveKML.KMLObjects.LineStyle import LineStyle
from pyLiveKML.KMLObjects.LinearRing import LinearRing
from pyLiveKML.KMLObjects.Link import Link
from pyLiveKML.KMLObjects.ListStyle import ItemIcon, ListStyle
from pyLiveKML.KMLObjects.LookAt import LookAt
from pyLiveKML.KMLObjects.Model import Alias, Model
from pyLiveKML.KMLObjects.MultiGeometry import MultiGeometry
from pyLiveKML.KMLObjects.MultiTrack import MultiTrack
from pyLiveKML.KMLObjects.NetworkLink import NetworkLink
from pyLiveKML.KMLObjects.PhotoOverlay import PhotoOverlay
from pyLiveKML.KMLObjects.Placemark import Placemark
from pyLiveKML.KMLObjects.Point import Point
from pyLiveKML.KMLObjects.PolyStyle import PolyStyle
from pyLiveKML.KMLObjects.Polygon import Polygon
from pyLiveKML.KMLObjects.Region import Region
from pyLiveKML.KMLObjects.Schema import Schema, SimpleField
from pyLiveKML.KMLObjects.ScreenOverlay import ScreenOverlay
from pyLiveKML.KMLObjects.SoundCue import SoundCue
from pyLiveKML.KMLObjects.Style import Style
from pyLiveKML.KMLObjects.StyleMap import StyleMap
from pyLiveKML.KMLObjects.TimeSpan import TimeSpan, TimeSpan
from pyLiveKML.KMLObjects.TimeStamp import TimeStamp, GxTimeStamp
from pyLiveKML.KMLObjects.Tour import Tour, Playlist
from pyLiveKML.KMLObjects.TourControl import TourControl
from pyLiveKML.KMLObjects.Track import (
    Track,
    TrackAngles,
    TrackCoord,
    TrackElement,
)
from pyLiveKML.KMLObjects.Wait import Wait

# global imports wrapper
# allows importing any of the instantiable KML objects and helpers from the `pyLiveKML` module
__all__ = [
    "Alias",
    "AltitudeModeEnum",
    "AltitudeModeEnum",
    "BalloonStyle",
    "Camera",
    "ColorModeEnum",
    "DisplayModeEnum",
    "Document",
    "FlyTo",
    "FlyToModeEnum",
    "Folder",
    "GeoColor",
    "GeoCoordinates",
    "GroundOverlay",
    "GxTimeStamp",
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
    "MultiTrack",
    "NetworkLink",
    "NetworkLinkControl",
    "OverlayXY",
    "PhotoOverlay",
    "Placemark",
    "Playlist",
    "PlayModeEnum",
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
    "SoundCue",
    "Style",
    "StyleMap",
    "StyleStateEnum",
    "TimeSpan",
    "TimeSpan",
    "TimeStamp",
    "Tour",
    "TourControl",
    "Track",
    "TrackAngles",
    "TrackCoord",
    "TrackElement",
    "UnitsEnum",
    "ViewRefreshModeEnum",
    "ViewerOption",
    "ViewerOptionEnum",
    "Wait",
    "errors",
    "kml_root_tag",
]
