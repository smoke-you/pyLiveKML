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
    UnitsEnum,
    ViewerOption,
    ViewerOptionEnum,
    ViewVolume,
)


def build_simple_doc(root_path: str) -> Document:
    """Construct a simple KML document.

    Main purpose is to prepend the server root path to icon links.
    """
    # global styles
    root_style = Style(
        BalloonStyle(
            0x40400000,
            0xFF0000FF,
            "This popup's text is set in the root Document's balloon style, rather than in the Document itself.",
        ),
        ListStyle(
            icons=(
                ItemIcon(
                    icon_state=ItemIconModeEnum.OPEN,
                    href=f"{root_path}static/img/google-mapfiles-kml-pal3-icon47.png",
                ),
                ItemIcon(
                    icon_state=ItemIconModeEnum.CLOSED,
                    href=f"{root_path}static/img/google-mapfiles-kml-pal3-icon41.png",
                ),
            ),
        ),
    )
    ground_point_style = Style(
        IconStyle("https://maps.google.com/mapfiles/kml/paddle/red-diamond.png")
    )
    ground_linestr_style = Style(LineStyle(3, 0xFF20FF00))
    air_linestr_style = Style(
        LineStyle(5, 0xFF00FF20),
        PolyStyle(0x8000FF20, fill=True),
    )
    ground_linring_style = Style(LineStyle(10, 0xFFFF0000))
    air_linring_style = Style(
        LineStyle(5, 0xFF0000FF),
        PolyStyle(0xFF0000FF, fill=True),
    )
    no_cutout_poly_style = Style(
        LineStyle(1, 0xFF0000FF),  # red 1px border
        PolyStyle(0x6000FF00, fill=True, outline=True),  # 38% green fill
    )
    with_cutout_poly_style_normal = Style(
        LineStyle(5, 0xFF00FF00),  # green 5px border
        PolyStyle(0x60FF0000, fill=True, outline=True),  # 38% blue fill
    )
    with_cutout_poly_style_highlight = Style(
        LineStyle(5, 0xFF00FF00),  # green 5px border
        PolyStyle(0x600000FF, fill=True, outline=True),  # 38% red fill
    )
    with_cutout_poly_style = StyleMap(
        f"#{with_cutout_poly_style_normal.id}",
        f"#{with_cutout_poly_style_highlight.id}",
    )
    camera = Camera(
        (151.21343, -33.88354, 10000), altitude_mode=AltitudeModeEnum.ABSOLUTE
    )
    root_schema = Schema(
        "root_schema",
        (
            SimpleField("int", "000", "Field I"),
            SimpleField("float", "001"),
            SimpleField("str", "002", "Field S"),
        ),
    )

    # root Document, contains the various Folders for the Placemarks
    # Global Styles are stored here
    build_data = Document(
        "root",
        is_open=True,
        description="Contains folders hosting a variety of Placemarks.",
        snippet="",
        author_name="smoke-you",
        author_link="https://github.com/smoke-you/pyLiveKML",
        abstract_view=camera,
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
        ],
        schemas=root_schema,
    )


    xd_folder = Folder(
        "Extended Data",
        snippet="click me for extended data",
        extended_data=ExtendedData(
            items=(
                DataItem("field 0", "Field: 0", "abc"),
                DataItem("field 1", "Field: 1", "def"),
                DataItem("field 2", "Field: 2", "ghi"),
                SchemaDataItem(
                    f"#{root_schema.id}",
                    {"000": "123", "001": "34.5", "002": "some string"},
                ),
            ),
        ),
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
                    (151.18843, -33.87354, 1000),
                    AltitudeModeEnum.ABSOLUTE,
                    extrude=True,
                ),
                name="Point @ 1000m",
                description="A Point located in the air, and extruded to ground. Styled with an inline style to give a double-sized icon and a double-sized yellow label.",
                snippet="",
                inline_style=Style(
                    icon_style=IconStyle(
                        "https://maps.google.com/mapfiles/kml/paddle/grn-blank.png",
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
                style_url=f"#{air_linestr_style.id}",
            ),
        ],
    )

    linring_folder = Folder(
        "LinearRings",
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
                    (
                        (151.20343, -33.89354),
                        (151.20343, -33.88354),
                        (151.21343, -33.88354),
                        (151.21343, -33.89354),
                    ),
                    altitude_mode=AltitudeModeEnum.CLAMP_TO_GROUND,
                ),
                name="Polygon @ Ground",
                description="A Polygon, clamped to ground, lime-green fill, red border.",
                snippet="",
                style_url=f"#{no_cutout_poly_style.id}",
            ),
            Placemark(
                Polygon(
                    (
                        (151.22343, -33.89354, 200),
                        (151.22343, -33.88354, 200),
                        (151.23343, -33.88354, 200),
                        (151.23343, -33.89354, 200),
                    ),
                    (
                        (
                            (151.22443, -33.89254, 200),
                            (151.22443, -33.89154, 200),
                            (151.22543, -33.89154, 200),
                            (151.22543, -33.89254, 200),
                        ),
                        (
                            (151.22443, -33.88954, 200),
                            (151.22443, -33.88854, 200),
                            (151.22543, -33.88854, 200),
                            (151.22543, -33.88954, 200),
                        ),
                    ),
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
        abstract_view=LookAt(
            (151.18843, -33.90354, 200),
            11,
            72,
            3700,
            viewer_options=ViewerOption(ViewerOptionEnum.SUNLIGHT, False),
        ),
        features=[
            Placemark(
                MultiGeometry(
                    [
                        Point((151.18843, -33.90354, 200), AltitudeModeEnum.ABSOLUTE),
                        Polygon(
                            (
                                (151.18643, -33.90554),
                                (151.18643, -33.90154),
                                (151.19043, -33.90154),
                                (151.19043, -33.90554),
                            ),
                            altitude_mode=AltitudeModeEnum.CLAMP_TO_GROUND,
                        ),
                    ],
                ),
                name="[Point @ 200m, Poly @ Ground]",
                description="A MultiGeometry hosting a Point @ 200m and a Polygon clamped to ground.\nBoth Point and Polygon respond to mouse hover.",
                snippet="Double-click this folder to change view",
                inline_style=StyleMap(
                    Style(
                        IconStyle(
                            "https://maps.google.com/mapfiles/kml/paddle/red-diamond-lv.png",
                            0.4,
                        ),
                        LineStyle(1, 0xFF0080FF),
                        PolyStyle(0x6000FF00, fill=True, outline=True),
                        LabelStyle(0),
                    ),
                    Style(
                        IconStyle(
                            "https://maps.google.com/mapfiles/kml/paddle/wht-stars.png",
                            2,
                        ),
                        LineStyle(2, 0xFFFF8000),
                        PolyStyle(0xFFFF0000, fill=True, outline=True),
                        LabelStyle(0),
                    ),
                ),
            )
        ],
    )

    # This is commented out because I don't think I can put the CU Macky building .dae
    # model, obtained from
    # https://developers.google.com/static/kml/documentation/MackyBldg.kmz as linked at
    # https://developers.google.com/kml/documentation/models into my github archive.
    # Nonetheless, the <Model> implementation works - the model is displayed in GEP, and
    # all of it's texture files are retrieved using the <ResourceMap> aliases.
    # It should be quite straightforward to replicate.

    # model_folder = Folder(
    #     name="Models",
    #     is_open=True,
    #     description="Contains a Placemark hosting a Model.",
    #     snippet="",
    #     features=[
    #         Placemark(
    #             geometry=Model(
    #                 Link(href=f"{root_path}static/dae/CU Macky.dae"),
    #                 location=(151.20643, -33.90554),
    #                 scales=(20, 20, 20),
    #                 resources=(
    #                     Alias("resources/CU-Macky---Center-StairsnoCulling.jpg", "../files/CU-Macky---Center-StairsnoCulling.jpg"),
    #                     Alias("resources/CU-Macky-4sideturretnoCulling.jpg", "../files/CU-Macky-4sideturretnoCulling.jpg"),
    #                     Alias("resources/CU-Macky-Back-NorthnoCulling.jpg", "../files/CU-Macky-Back-NorthnoCulling.jpg"),
    #                     Alias("resources/CU-Macky-BrickwallnoCulling.jpg", "../files/CU-Macky-BrickwallnoCulling.jpg"),
    #                     Alias("resources/CU-Macky-East-WingnoCulling.jpg", "../files/CU-Macky-East-WingnoCulling.jpg"),
    #                     Alias("resources/CU-Macky-EastdetaildoornoCulling.jpg", "../files/CU-Macky-EastdetaildoornoCulling.jpg"),
    #                     Alias("resources/CU-Macky-EastnoCulling.jpg", "../files/CU-Macky-EastnoCulling.jpg"),
    #                     Alias("resources/CU-Macky-EntrancenoCulling.jpg", "../files/CU-Macky-EntrancenoCulling.jpg"),
    #                     Alias("resources/CU-Macky-Front--TurretnoCulling.jpg", "../files/CU-Macky-Front--TurretnoCulling.jpg"),
    #                     Alias("resources/CU-Macky-FrontbrickwallnoCulling.jpg", "../files/CU-Macky-FrontbrickwallnoCulling.jpg"),
    #                     Alias("resources/CU-Macky-FrontnoCulling.jpg", "../files/CU-Macky-FrontnoCulling.jpg"),
    #                     Alias("resources/CU-Macky-FrontofTowernoCulling.jpg", "../files/CU-Macky-FrontofTowernoCulling.jpg"),
    #                     Alias("resources/CU-Macky-NortheastUnivnoCulling.jpg", "../files/CU-Macky-NortheastUnivnoCulling.jpg"),
    #                     Alias("resources/CU-Macky-NorthnoCulling.jpg", "../files/CU-Macky-NorthnoCulling.jpg"),
    #                     Alias("resources/CU-Macky-RoofnoCulling.jpg", "../files/CU-Macky-RoofnoCulling.jpg"),
    #                     Alias("resources/CU-Macky-Tower-SidenoCulling.jpg", "../files/CU-Macky-Tower-SidenoCulling.jpg"),
    #                     Alias("resources/CU-Macky-TowerBasenoCulling.jpg", "../files/CU-Macky-TowerBasenoCulling.jpg"),
    #                     Alias("resources/CU-Macky-TowernoCulling.jpg", "../files/CU-Macky-TowernoCulling.jpg"),
    #                     Alias("resources/CU-Macky-_Side_BrickwallnoCulling.jpg", "../files/CU-Macky-_Side_BrickwallnoCulling.jpg"),
    #                     Alias("resources/roofnoCulling.jpg", "../files/roofnoCulling.jpg"),
    #                 )
    #             )
    #         )
    #     ]
    # )

    overlay_folder = Folder(
        "Overlays",
        description="Contains an instance of each concrete Overlay subclass",
        snippet="",
        is_open=True,
        # Regions **work**, in that GEP accepts them, but... I can't seem to make them 
        # become active?
        # region=Region(LatLonAltBox(-33.86354, -33.87354, 151.20843, 151.21843)),
        features=[
            GroundOverlay(
                name="Ground overlay (box)",
                description='Overlays a semi-transparent "earth" icon into a square box with 45deg rotation',
                snippet="",
                box=LatLonBox(-33.86354, -33.87354, 151.20843, 151.21843, 45),
                color=0xA0FFFFFF,
                icon=Icon(f"{root_path}/static/img/earth.png"),
            ),
            GroundOverlay(
                name="Ground overlay (quad)",
                description="Overlays a semi-transparent blue-green rhombus",
                snippet="",
                quad=LatLonQuad(
                    (
                        (151.22843, -33.86354),
                        (151.24043, -33.86354),
                        (151.23843, -33.87354),
                        (151.22643, -33.87354),
                    )
                ),
                color=0x80FF4000,
            ),
            ScreenOverlay(
                name="Screen overlay",
                description='Overlays a "pyLiveKML" icon onto the screen in the bottom-left corner.\nColor is purple, semi-transparent.',
                snippet="",
                size=Size(
                    0, 64, UnitsEnum.PIXELS, UnitsEnum.PIXELS
                ),  # 64px high, maintain aspect ratio
                overlay_xy=OverlayXY(0, 0),  # place at bottom left corner of icon
                screen_xy=ScreenXY(
                    0.05, 0.08
                ),  # place at 0.05,0.08 of screen fullscale from origin
                rotation_xy=RotationXY(
                    0.05, 0.08
                ),  # rotation around 0.05,0.08 of screen fullscale from origin
                rotation=30,  # rotate 30deg around rotation_xy
                icon=Icon(f"{root_path}/static/img/pyLiveKML-overlay.png"),
                color=0xA08000FF,
            ),
            PhotoOverlay(
                name="Photo overlay",
                description='Photo overlay of an "earth" icon onto a point, with a LookAt facing it.',
                snippet="",
                point=Point((151.24043, -33.90554)),
                color=0x60FFFFFF,
                icon=Icon(f"{root_path}/static/img/earth.png"),
                abstract_view=LookAt(
                    (151.24043, -33.90554, 0), -90, 70, 10000, AltitudeModeEnum.ABSOLUTE
                ),
                view_volume=ViewVolume(-25, 25, -25, 25, 9000),
                shape=OverlayShapeEnum.RECTANGLE,
                styles=StyleMap(
                    Style(IconStyle(scale=0)),
                    Style(
                        IconStyle(
                            "http://maps.google.com/mapfiles/kml/paddle/ylw-circle.png",
                            2,
                        )
                    ),
                ),
            ),
        ],
    )

    build_data.extend(
        (
            xd_folder,
            points_folder,
            linestr_folder,
            linring_folder,
            poly_folder,
            multigeo_folder,
            # model_folder,
            overlay_folder,
        )
    )

    return build_data
