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



point_style = Style(
    icon_style=IconStyle("http://maps.google.com/mapfiles/kml/paddle/red-diamond.png")
)
line_style = Style(
    line_style=LineStyle(3, 0xff20ff00)
)

# root Document, contains the various Folders for the Placemarks
# Global Styles are defined here
build_data = Document(
    "root", 
    is_open=True, 
    description="Contains folders hosting a variety of Placemarks.",
    snippet="",
    author_name="smoke-you", 
    author_link="https://github.com/smoke-you/pyLiveKML",
    styles=[
        point_style,
        line_style,
    ]
)
# points Folder
points_folder = Folder(
    "Points",
    is_open=True,
    description="Contains several Placemarks containing Point geometries.",
    snippet="",
    features = (
        # point located at ground level
        # styled by global style
        Placemark(
            Point((151.188431, -33.873545), AltitudeModeEnum.CLAMP_TO_GROUND), 
            "Ground", 
            style_url=f"#{str(point_style.id)}"
        ),
        # point located in the air
        # styled by an inline style, including a double-size yellow label
        Placemark(
            Point((151.188431, -33.873545, 1000), AltitudeModeEnum.ABSOLUTE), 
            "Air @ 1000m",
            inline_style=Style(
                icon_style=IconStyle(
                    "http://maps.google.com/mapfiles/kml/paddle/grn-blank.png", 
                    scale=2,
                ),
                label_style=LabelStyle(scale=2, color=0xc0808000),
            )
        )
    )
)
build_data.append(points_folder)

linestr_folder = Folder(
    "LineStrings",
    is_open=True,
    description="Contains several Placemarks containing LineString geometries.",
    snippet="",
    features = (
        Placemark(
            LineString((
                (151.188431, -33.873545),
                (151.198431, -33.873545),
                (151.198431, -33.863545),
            )),
            style_url=f"#{str(line_style.id)}"
        )
    )
)
build_data.append(linestr_folder)

# with open("tests/output/test_placemarks.kml", "w+") as kf:
#     kf.write(
#         etree.tostring(
#             root, 
#             doctype=KML_DOCTYPE, 
#             encoding="utf-8", 
#             pretty_print=True
#             ).decode("utf-8")
#         )
