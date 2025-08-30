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
    PolyStyle,
    StyleMap,
)


# global styles
root_style = Style(
    balloon_style=BalloonStyle(
        text="Some text goes here", text_color=0xFF0000FF, bg_color=0x40400000
    )
)
ground_point_style = Style(
    icon_style=IconStyle("http://maps.google.com/mapfiles/kml/paddle/red-diamond.png")
)
ground_linestr_style = Style(line_style=LineStyle(3, 0xFF20FF00))
air_linestr_style = Style(line_style=LineStyle(5, 0xFF00FF20))
ground_linring_style = Style(line_style=LineStyle(10, 0xFFFF0000))
air_linring_style = Style(line_style=LineStyle(5, 0xFF0000FF))
no_cutout_poly_style = Style(
    line_style=LineStyle(1, 0xFF0000FF),  # red 1px border
    poly_style=PolyStyle(0x6000FF00, fill=True, outline=True),  # 38% green fill
)
with_cutout_poly_style_normal = Style(
    line_style=LineStyle(5, 0xFF00FF00),  # green 5px border
    poly_style=PolyStyle(0x60FF0000, fill=True, outline=True),  # 38% blue fill
)
with_cutout_poly_style_highlight = Style(
    line_style=LineStyle(5, 0xFF00FF00),  # green 5px border
    poly_style=PolyStyle(0x600000FF, fill=True, outline=True),  # 38% red fill
)
with_cutout_poly_style = StyleMap(
    f"#{with_cutout_poly_style_normal.id}", f"#{with_cutout_poly_style_highlight.id}"
)

# multigeo_style_normal = Style(
#     icon_style=IconStyle("http://maps.google.com/mapfiles/kml/paddle/red-diamond.png"),
#     line_style=LineStyle(1, 0xFF0080FF),
#     poly_style=PolyStyle(0x6000FF00, fill=True, outline=True),
#     label_style=LabelStyle(0),
# )
# multigeo_style_highlight = Style(
#     icon_style=IconStyle("http://maps.google.com/mapfiles/kml/paddle/wht-stars.png", 2),
#     line_style=LineStyle(2, 0xFFFF8000),
#     poly_style=PolyStyle(0xFFFF0000, fill=True, outline=True),
#     label_style=LabelStyle(0),
# )
# multigeo_style = StyleMap(
#     f"#{multigeo_style_normal.id}", f"#{multigeo_style_highlight.id}"
# )

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
        ground_point_style,
        ground_linestr_style,
        air_linestr_style,
        ground_linring_style,
        air_linring_style,
        no_cutout_poly_style,
        with_cutout_poly_style_normal,
        with_cutout_poly_style_highlight,
        with_cutout_poly_style,
        # multigeo_style_normal,
        # multigeo_style_highlight,
        # multigeo_style,
    ],
)

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
            style_url=f"#{ground_point_style.id}",
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
            description="A simple LineString, clamped to ground, and lime-green in colour.",
            snippet="",
            style_url=f"#{ground_linestr_style.id}",
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
            description="A LineString located in the air, tessellated and extruded to ground, and yellowish in color.",
            snippet="",
            style_url=f"#{ground_linestr_style.id}",
        ),
    ],
)

linring_folder = Folder(
    "LineStrings",
    is_open=True,
    description="Contains several Placemarks hosting LinearRing geometries. Note that while Polygons are constructed from LinearRings, LinearRings may be created independent of Polygons.",
    snippet="",
    features=[
        Placemark(
            LinearRing(
                (
                    (151.18343, -33.89354),
                    (151.18343, -33.88354),
                    (151.19343, -33.88354),
                    (151.19343, -33.89354),
                    (151.18343, -33.89354),
                ),
                altitude_mode=AltitudeModeEnum.CLAMP_TO_GROUND,
            ),
            name="LinearRing @ Ground",
            description="A LinearRing, clamped to ground, blue in color.",
            snippet="",
            style_url=f"#{ground_linring_style.id}",
        ),
        Placemark(
            LinearRing(
                (
                    (151.18343, -33.89354, 1000),
                    (151.18343, -33.88354, 1000),
                    (151.19343, -33.88354, 1000),
                    (151.19343, -33.89354, 1000),
                    (151.18343, -33.89354, 1000),
                ),
                altitude_mode=AltitudeModeEnum.ABSOLUTE,
                extrude=True,
                tessellate=True,
            ),
            name="LinearRing @ 1000m",
            description="A LinearRing, at 1000m, red in color, tessellated and extruded to ground.",
            snippet="",
            style_url=f"#{air_linring_style.id}",
        ),
        Placemark(
            LinearRing(
                (
                    (151.18343, -33.89354, 2000),
                    (151.18343, -33.88354, 2000),
                    (151.19343, -33.88354, 2000),
                    (151.19343, -33.89354, 2000),
                    (151.18343, -33.89354, 2000),
                ),
                altitude_mode=AltitudeModeEnum.ABSOLUTE,
            ),
            name="LinearRing @ 2000m",
            description="A LinearRing, at 2000m, purple in color.",
            snippet="",
            inline_style=Style(line_style=LineStyle(color=0xFFFF00FF, width=2.5)),
        ),
    ],
)

poly_folder = Folder(
    "Polygons",
    is_open=True,
    description="Contains several Placemarks hosting Polygon geometries.",
    snippet="",
    features=[
        Placemark(
            Polygon(
                LinearRing(
                    (
                        (151.20343, -33.89354),
                        (151.20343, -33.88354),
                        (151.21343, -33.88354),
                        (151.21343, -33.89354),
                        (151.20343, -33.89354),
                    ),
                    altitude_mode=AltitudeModeEnum.CLAMP_TO_GROUND,
                ),
            ),
            name="Polygon @ Ground",
            description="A Polygon, clamped to ground, lime-green fill, red border.",
            snippet="",
            style_url=f"#{no_cutout_poly_style.id}",
        ),
        Placemark(
            Polygon(
                LinearRing(
                    (
                        (151.22343, -33.89354, 200),
                        (151.22343, -33.88354, 200),
                        (151.23343, -33.88354, 200),
                        (151.23343, -33.89354, 200),
                        (151.22343, -33.89354, 200),
                    ),
                ),
                [
                    LinearRing(
                        (
                            (151.22443, -33.89254, 200),
                            (151.22443, -33.89154, 200),
                            (151.22543, -33.89154, 200),
                            (151.22543, -33.89254, 200),
                            (151.22443, -33.89254, 200),
                        ),
                    ),
                    LinearRing(
                        (
                            (151.22443, -33.88954, 200),
                            (151.22443, -33.88854, 200),
                            (151.22543, -33.88854, 200),
                            (151.22543, -33.88954, 200),
                            (151.22443, -33.88954, 200),
                        ),
                    ),
                ],
                altitude_mode=AltitudeModeEnum.ABSOLUTE,
            ),
            name="Polygon @ 200m",
            description="A Polygon, 200m, blue fill, thick green border, cutouts. Fill changes to red on hover.",
            snippet="",
            style_url=f"#{with_cutout_poly_style.id}",
        ),
    ],
)

multigeo_folder = Folder(
    "Multigeometries",
    is_open=True,
    description="Contains a Placemark hosting MultiGeometry geometries.",
    snippet="",
    features=[
        Placemark(
            MultiGeometry(
                [
                    Point((151.18843, -33.90354, 200), AltitudeModeEnum.ABSOLUTE),
                    Polygon(
                        LinearRing(
                            (
                                (151.18643, -33.90554),
                                (151.18643, -33.90154),
                                (151.19043, -33.90154),
                                (151.19043, -33.90554),
                                (151.18643, -33.90554),
                            ),
                        ),
                        altitude_mode=AltitudeModeEnum.CLAMP_TO_GROUND,
                    ),
                ],
            ),
            name="[Point @ 200m, Poly @ Ground]",
            description="A MultiGeometry hosting a Point @ 200m and a Polygon clamped to ground.\nBoth Point and Polygon respond to mouse hover.",
            snippet="",
            inline_style = StyleMap(
                Style(
                    icon_style=IconStyle("http://maps.google.com/mapfiles/kml/paddle/red-diamond.png"),
                    line_style=LineStyle(1, 0xFF0080FF),
                    poly_style=PolyStyle(0x6000FF00, fill=True, outline=True),
                    label_style=LabelStyle(0),
                ),
                Style(
                    icon_style=IconStyle("http://maps.google.com/mapfiles/kml/paddle/wht-stars.png", 2),
                    line_style=LineStyle(2, 0xFFFF8000),
                    poly_style=PolyStyle(0xFFFF0000, fill=True, outline=True),
                    label_style=LabelStyle(0),
                )
            )
        )
    ],
)

build_data.extend(
    (
        points_folder,
        linestr_folder,
        linring_folder,
        poly_folder,
        multigeo_folder,
    )
)
