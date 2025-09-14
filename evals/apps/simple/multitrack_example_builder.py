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
    IconStyle,
    LabelStyle,
    LineStyle,
    LookAt,
    MultiTrack,
    Placemark,
    Style,
    StyleMap,
    TimeSpan,
    Track,
    TrackElement,
)


def build_doc(root_path: str) -> Document:
    """Construct a simple KML document.

    Main purpose is to prepend the server root path to icon links.
    """
    mtrack_style = StyleMap(
        Style(
            LabelStyle(1, 0xFFFF8000),
            LineStyle(1, 0xFFFF8000),
            IconStyle("http://maps.google.com/mapfiles/kml/shapes/swimming.png"),
        ),
        Style(
            LabelStyle(2, 0xFF00FF00),
            LineStyle(5, 0xFF00FF00),
            IconStyle("http://maps.google.com/mapfiles/kml/shapes/swimming.png"),
        ),
    )

    # root Document, contains the various Folders for the Placemarks
    # Global Styles are stored here
    build_data = Document(
        "root",
        is_open=True,
        description="Contains an example of a MultiTrack.",
        snippet="A multi-step track of a swimmer.",
        author_name="smoke-you",
        author_link="https://github.com/smoke-you/pyLiveKML",
        styles=mtrack_style,
    )

    mtrack = Placemark(
        name="MultiTrack example",
        snippet="",
        description="Swimming around a bay clockwise: starting at a marina; stopping at a pier; stopping again at buoy, then finishing at a pier.",
        style_url=f"#{mtrack_style.id}",
        abstract_view=LookAt((151.201046, -33.870679), 52, 57, 900),
        time_primitive=TimeSpan("2025-07-02T14:00:00Z", "2025-07-02T14:57:00Z"),
        geometry=MultiTrack(
            tracks=(
                Track(
                    elements=(
                        TrackElement(
                            "2025-07-02T14:00:00Z",
                            (151.201722, -33.871055),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:01:00Z",
                            (151.201282, -33.871035),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:02:00Z",
                            (151.201193, -33.871390),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:03:00Z",
                            (151.201143, -33.871725),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:04:00Z",
                            (151.201105, -33.872049),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:05:00Z",
                            (151.201093, -33.872468),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:06:00Z",
                            (151.201395, -33.872708),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:07:00Z",
                            (151.201383, -33.873022),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:08:00Z",
                            (151.201042, -33.873106),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:09:00Z",
                            (151.200677, -33.873147),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:10:00Z",
                            (151.200375, -33.873053),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:11:00Z",
                            (151.200198, -33.872792),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:12:00Z",
                            (151.200072, -33.872509),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:13:00Z",
                            (151.199946, -33.872143),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:14:00Z",
                            (151.199921, -33.871819),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:15:00Z",
                            (151.199959, -33.871401),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:16:00Z",
                            (151.199871, -33.871076),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:17:00Z",
                            (151.199493, -33.870899),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:18:00Z",
                            (151.199329, -33.870606),
                            0,
                        ),
                    )
                ),
                Track(
                    elements=(
                        TrackElement(
                            "2025-07-02T14:27:00Z",
                            (151.199329, -33.870606),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:28:00Z",
                            (151.199588, -33.870393),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:29:00Z",
                            (151.199801, -33.870141),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:30:00Z",
                            (151.200123, -33.870141),
                            0,
                        ),
                    )
                ),
                Track(
                    elements=(
                        TrackElement(
                            "2025-07-02T14:49:00Z",
                            (151.200123, -33.870141),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:50:00Z",
                            (151.200149, -33.869879),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:51:00Z",
                            (151.200123, -33.869607),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:52:00Z",
                            (151.200227, -33.869384),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:53:00Z",
                            (151.200336, -33.869137),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:54:00Z",
                            (151.200370, -33.868824),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:55:00Z",
                            (151.200303, -33.868535),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:56:00Z",
                            (151.200089, -33.868358),
                            0,
                        ),
                        TrackElement(
                            "2025-07-02T14:57:00Z",
                            (151.199796, -33.868253),
                            0,
                        ),
                    )
                ),
            )
        ),
    )

    build_data.extend((mtrack,))

    return build_data
