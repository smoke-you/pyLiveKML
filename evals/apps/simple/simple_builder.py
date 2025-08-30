"""Simple data builder module."""

from lxml import etree  # type: ignore

from pyLiveKML import (
    kml_root_tag,
    KML_DOCTYPE,
    AltitudeModeEnum,
    Document,
    Folder,
    Placemark,
    Point,
    LineString,
    LinearRing,
    Polygon,
    MultiGeometry,
    GxTrack,
    GxMultiTrack,
    Style,
    BalloonStyle,
    IconStyle,
    LabelStyle,
    LineStyle,
)


# global styles
root_style = Style(
    balloon_style=BalloonStyle(
        text="Some text goes here", text_color=0xFF0000FF, bg_color=0x40400000
    )
)
point_style = Style(
    icon_style=IconStyle("http://maps.google.com/mapfiles/kml/paddle/red-diamond.png")
)
line_style = Style(line_style=LineStyle(3, 0xFF20FF00))

# root Document, contains the various Folders for the Placemarks
# Global Styles are stored here
build_data = Document(
    "root",
    is_open=True,
    description="Contains folders hosting a variety of Placemarks.",
    snippet="",
    author_name="smoke-you",
    author_link="https://github.com/smoke-you/pyLiveKML",
    style_url=f"#{root_style.id}",
    styles=[
        root_style,
        point_style,
        line_style,
    ],
)
# points Folder
points_folder = Folder(
    "Points",
    is_open=True,
    description="Contains several Placemarks hosting Point geometries.",
    snippet="",
    features=[
        Placemark(
            Point((151.18843, -33.87354), AltitudeModeEnum.CLAMP_TO_GROUND),
            name="Point @ Ground",
            description="A simple Point, clamped to ground, and styled with a global style.",
            snippet="",
            style_url=f"#{point_style.id}",
        ),
        Placemark(
            Point(
                (151.18843, -33.87354, 1000), AltitudeModeEnum.ABSOLUTE, extrude=True
            ),
            name="Point @ 1000m",
            description="A Point located in the air, and extruded to ground. Styled with an inline style to give a double-sized icon and a double-sized yellow label.",
            snippet="",
            inline_style=Style(
                icon_style=IconStyle(
                    "http://maps.google.com/mapfiles/kml/paddle/grn-blank.png",
                    scale=2,
                ),
                label_style=LabelStyle(scale=2, color=0xC0008080),
            ),
        ),
    ],
)

linestr_folder = Folder(
    "LineStrings",
    is_open=True,
    description="Contains several Placemarks hosting LineString geometries.",
    snippet="",
    features=[
        Placemark(
            LineString(
                (
                    (151.18843, -33.87354),
                    (151.19843, -33.87354),
                    (151.19843, -33.86354),
                )
            ),
            name="LineString @ Ground",
            description="A simple LineString, clamped to ground.",
            snippet="",
            style_url=f"#{line_style.id}",
        ),
        Placemark(
            LineString(
                (
                    (151.18843, -33.87354, 500),
                    (151.17843, -33.87354, 500),
                    (151.17843, -33.86354, 500),
                ),
                altitude_mode=AltitudeModeEnum.ABSOLUTE,
                extrude=True,
                tessellate=True,
            ),
            name="LineString @ 500m",
            description="A LineString located in the air, tessellated and extruded to ground.",
            snippet="",
            style_url=f"#{line_style.id}",
        ),
    ],
)

build_data.extend((points_folder, linestr_folder))
