# pyLiveKML: A python library that streams geospatial data using the KML protocol.
# Copyright (C) 2025 smoke-you

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

"""Simple data builder module."""

from lxml import etree  # type: ignore

from pyLiveKML import (
    Document,
    HotSpot,
    IconStyle,
    LineStyle,
    Placemark,
    Schema,
    SimpleField,
    Style,
    StyleMap,
    Track,
    TrackElement,
)


def build_doc(root_path: str) -> Document:
    """Construct a simple KML document.

    Main purpose is to prepend the server root path to icon links.
    """
    track_style = StyleMap(
        Style(
            LineStyle(3, 0xFF00FF00),
            IconStyle(
                "http://maps.google.com/mapfiles/kml/shapes/motorcycling.png",
                hot_spot=HotSpot(1, 1),
            ),
        ),
        Style(
            LineStyle(5, 0xFF0000FF),
            IconStyle(
                "http://maps.google.com/mapfiles/kml/shapes/motorcycling.png",
                hot_spot=HotSpot(1, 1),
            ),
        ),
    )
    track_schema = Schema(
        "mc_schema",
        (
            SimpleField("float", "pollution", "Pollution (ppm)"),
            SimpleField("float", "noise", "Noise Level (dB)"),
        ),
    )

    # root Document, contains the various Folders for the Placemarks
    # Global Styles are stored here
    build_data = Document(
        "root",
        is_open=True,
        description="Contains an example of a Track.",
        snippet="A track of a motorcycle.",
        author_name="smoke-you",
        author_link="https://github.com/smoke-you/pyLiveKML",
        styles=(track_style,),
        schemas=(track_schema,),
    )

    track = Placemark(
        name="Track example",
        snippet="",
        style_url=f"#{track_style.id}",
        geometry=Track(
            elements=(
                TrackElement(
                    "2025-06-01T22:00:00Z",
                    (151.192985, -33.904928),
                    38,
                    {f"#{track_schema.name}": {"pollution": "0", "noise": "0"}},
                ),
                TrackElement(
                    "2025-06-01T22:00:10Z",
                    (151.193544, -33.904323),
                    308,
                    {f"#{track_schema.name}": {"pollution": "30", "noise": "90"}},
                ),
                TrackElement(
                    "2025-06-01T22:00:20Z",
                    (151.192772, -33.903803),
                    38,
                    {f"#{track_schema.name}": {"pollution": "450", "noise": "105"}},
                ),
                TrackElement(
                    "2025-06-01T22:00:30Z",
                    (151.194706, -33.901737),
                    308,
                    {f"#{track_schema.name}": {"pollution": "30", "noise": "90"}},
                ),
                TrackElement(
                    "2025-06-01T22:00:40Z",
                    (151.193987, -33.901215),
                    218,
                    {f"#{track_schema.name}": {"pollution": "450", "noise": "105"}},
                ),
                TrackElement(
                    "2025-06-01T22:00:50Z",
                    (151.192102, -33.903376),
                    308,
                    {f"#{track_schema.name}": {"pollution": "30", "noise": "90"}},
                ),
                TrackElement(
                    "2025-06-01T22:01:00Z",
                    (151.191370, -33.902907),
                    218,
                    {f"#{track_schema.name}": {"pollution": "20", "noise": "88"}},
                ),
                TrackElement(
                    "2025-06-01T22:01:05Z",
                    (151.191073, -33.903255),
                    0,
                    {f"#{track_schema.name}": {"pollution": "0", "noise": "0"}},
                ),
            )
        ),
    )

    build_data.extend((track,))

    return build_data
