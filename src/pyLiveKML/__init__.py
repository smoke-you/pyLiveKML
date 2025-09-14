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
    OverlayShapeEnum,
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
from pyLiveKML.objects.AnimatedUpdate import AnimatedUpdate
from pyLiveKML.objects.BalloonStyle import BalloonStyle
from pyLiveKML.objects.Camera import Camera
from pyLiveKML.objects.Document import Document
from pyLiveKML.objects.ExtendedData import DataItem, ExtendedData, SchemaDataItem
from pyLiveKML.objects.FlyTo import FlyTo
from pyLiveKML.objects.Folder import Folder
from pyLiveKML.objects.GroundOverlay import GroundOverlay, LatLonBox, LatLonQuad
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
from pyLiveKML.objects.TimeSpan import TimeSpan
from pyLiveKML.objects.TimeStamp import TimeStamp
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
    "AnimatedUpdate",
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
    "LatLonBox",
    "LatLonQuad",
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
    "OverlayShapeEnum",
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
