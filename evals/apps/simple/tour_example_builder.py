"""Simple data builder module."""

from lxml import etree  # type: ignore

from pyLiveKML import (
    Alias,
    AltitudeModeEnum,
    BalloonStyle,
    Camera,
    DataItem,
    Document,
    ExtendedData,
    Folder,
    GroundOverlay,
    Icon,
    IconStyle,
    ImagePyramid,
    ItemIcon,
    ItemIconModeEnum,
    LabelStyle,
    LatLonAltBox,
    LatLonBox,
    LatLonQuad,
    LinearRing,
    LineString,
    LineStyle,
    Link,
    ListStyle,
    LevelOfDetail,
    LookAt,
    Model,
    MultiGeometry,
    OverlayShapeEnum,
    OverlayXY,
    PhotoOverlay,
    Placemark,
    Point,
    Polygon,
    PolyStyle,
    Region,
    RotationXY,
    Schema,
    SchemaDataItem,
    ScreenOverlay,
    ScreenXY,
    SimpleField,
    Size,
    Style,
    StyleMap,
    Tour,
    Track,
    UnitsEnum,
    ViewerOption,
    ViewerOptionEnum,
    ViewVolume,
)


def build_doc(root_path: str) -> Document:
    """Construct a simple KML document.

    Main purpose is to prepend the server root path to icon links.
    """
    # root Document, contains the various Folders for the Placemarks
    # Global Styles are stored here
    build_data = Document(
        "root",
        is_open=True,
        description="Contains an example of a Tour.",
        snippet="",
        author_name="smoke-you",
        author_link="https://github.com/smoke-you/pyLiveKML",
    )

    # build_data.extend(
    # )

    return build_data
