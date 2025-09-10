"""pyLiveKML init module."""

from pyLiveKML.utils import (
    kml_root_tag,
    KML_DOCTYPE,
    KML_HEADERS,
    KML_UPDATE_CONTAINER_LIMIT_DEFAULT,
)
from pyLiveKML.types import (
    AltitudeModeEnum,
    ColorModeEnum,
    DisplayModeEnum,
    FlyToModeEnum,
    GeoColor,
    GeoCoordinates,
    HotSpot,
    ItemIconModeEnum,
    ListItemTypeEnum,
    OverlayXY,
    PlayModeEnum,
    RefreshModeEnum,
    RotationXY,
    ScreenXY,
    Size,
    StyleStateEnum,
    UnitsEnum,
    ViewRefreshModeEnum,
    ViewerOptionEnum,
)
from pyLiveKML import errors
from pyLiveKML.objects.AbstractView import ViewerOption
from pyLiveKML.objects.BalloonStyle import BalloonStyle
from pyLiveKML.objects.Camera import Camera
from pyLiveKML.objects.Document import Document
from pyLiveKML.objects.ExtendedData import DataItem, ExtendedData, SchemaDataItem
from pyLiveKML.objects.FlyTo import FlyTo
from pyLiveKML.objects.Folder import Folder
from pyLiveKML.objects.GroundOverlay import GroundOverlay
from pyLiveKML.objects.Icon import Icon
from pyLiveKML.objects.IconStyle import IconStyle
from pyLiveKML.objects.LabelStyle import LabelStyle
from pyLiveKML.objects.LineString import LineString
from pyLiveKML.objects.LineStyle import LineStyle
from pyLiveKML.objects.LinearRing import LinearRing
from pyLiveKML.objects.Link import Link
from pyLiveKML.objects.ListStyle import ItemIcon, ListStyle
from pyLiveKML.objects.LookAt import LookAt
from pyLiveKML.objects.Model import Alias, Model
from pyLiveKML.objects.MultiGeometry import MultiGeometry
from pyLiveKML.objects.MultiTrack import MultiTrack
from pyLiveKML.objects.NetworkLink import NetworkLink
from pyLiveKML.objects.NetworkLinkControl import NetworkLinkControl
from pyLiveKML.objects.PhotoOverlay import ImagePyramid, PhotoOverlay, ViewVolume
from pyLiveKML.objects.Placemark import Placemark
from pyLiveKML.objects.Point import Point
from pyLiveKML.objects.PolyStyle import PolyStyle
from pyLiveKML.objects.Polygon import Polygon
from pyLiveKML.objects.Region import LatLonAltBox, LevelOfDetail, Region
from pyLiveKML.objects.Schema import Schema, SimpleField
from pyLiveKML.objects.ScreenOverlay import ScreenOverlay
from pyLiveKML.objects.SoundCue import SoundCue
from pyLiveKML.objects.Style import Style
from pyLiveKML.objects.StyleMap import StyleMap
from pyLiveKML.objects.TimeSpan import TimeSpan, TimeSpan
from pyLiveKML.objects.TimeStamp import TimeStamp, GxTimeStamp
from pyLiveKML.objects.Tour import Tour, Playlist
from pyLiveKML.objects.TourControl import TourControl
from pyLiveKML.objects.Track import Track, TrackAngles, TrackCoord, TrackElement
from pyLiveKML.objects.Update import Update, UpdateSequent, UpdateType
from pyLiveKML.objects.Wait import Wait

# global imports wrapper
# allows importing any of the instantiable KML objects and helpers from the `pyLiveKML` module
__all__ = [
    "Alias",
    "AltitudeModeEnum",
    "AltitudeModeEnum",
    "BalloonStyle",
    "Camera",
    "ColorModeEnum",
    "DataItem",
    "DisplayModeEnum",
    "Document",
    "ExtendedData",
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
    "ImagePyramid",
    "ItemIcon",
    "ItemIconModeEnum",
    "KML_DOCTYPE",
    "KML_HEADERS",
    "KML_UPDATE_CONTAINER_LIMIT_DEFAULT",
    "LabelStyle",
    "LatLonAltBox",
    "LevelOfDetail",
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
    "PlayModeEnum",
    "Playlist",
    "Point",
    "PolyStyle",
    "Polygon",
    "RefreshModeEnum",
    "Region",
    "RotationXY",
    "Schema",
    "SchemaDataItem",
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
    "Update",
    "UpdateSequent",
    "UpdateType",
    "ViewRefreshModeEnum",
    "ViewerOption",
    "ViewerOptionEnum",
    "ViewVolume",
    "Wait",
    "errors",
    "kml_root_tag",
]
