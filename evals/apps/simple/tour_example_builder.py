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
    AnimatedUpdate,
    Document,
    FlyTo,
    FlyToModeEnum,
    IconStyle,
    LookAt,
    Placemark,
    PlayModeEnum,
    Point,
    SoundCue,
    Style,
    Tour,
    TourControl,
    UpdateSequent,
    UpdateType,
    Wait,
)


def build_doc(root_path: str) -> Document:
    """Construct a simple KML document.

    Main purpose is to prepend the server root path to icon links.
    """
    build_data = Document(
        "root",
        is_open=True,
        description="Contains an example of a Tour.",
        snippet="",
        author_name="smoke-you",
        author_link="https://github.com/smoke-you/pyLiveKML",
        abstract_view=LookAt((151.201046, -33.870679), 52, 57, 900),
    )

    # The Tour is going to animate an update to the `IconStyle` (make the icon large).
    # **One** way to do this is to have the `IconStyle`, and the `Style` that contains
    # it, already exist. Then, create another `IconStyle` and assign it the same `id`.
    # Now, we can change the new `IconStyle` and use it when constructing a `<Change>`
    # for the `AnimatedUpdate` via an `UpdateSequent`.
    anim_base_style = IconStyle()
    anim_update_style = IconStyle(scale=3, _id=anim_base_style._id)
    # anim_update_style._id = anim_base_style._id
    anim_style = Style(anim_base_style)
    anim_update = UpdateSequent(UpdateType.CHANGE, anim_base_style, anim_update_style)

    icon = Placemark(
        geometry=Point((151.201046, -32.870679)),
        inline_style=anim_style,
    )

    tour = Tour(
        "test tour",
        description="Demonstration of Tour tag, including TourControl (start/stop), FlyTo, Wait, AnimatedUpdate and SoundCue.",
        playlist=(
            FlyTo(
                0, FlyToModeEnum.SMOOTH, LookAt((151.201046, -33.870679), 52, 57, 900)
            ),
            TourControl(),
            FlyTo(
                3, FlyToModeEnum.SMOOTH, LookAt((151.201046, -32.870679), 52, 57, 900)
            ),
            TourControl(),
            # SoundCue works, but it's commented out below because I'm not going to
            # supply a sound file in my github archive.
            #
            # SoundCue(f"{root_path}static/media/testing-testing-testing.wav", 0),
            AnimatedUpdate(3, 0, "", (anim_update,)),
            Wait(10),
            FlyTo(
                3, FlyToModeEnum.SMOOTH, LookAt((151.201046, -33.870679), 52, 57, 900)
            ),
        ),
    )

    build_data.extend(
        (
            icon,
            tour,
        )
    )

    return build_data
