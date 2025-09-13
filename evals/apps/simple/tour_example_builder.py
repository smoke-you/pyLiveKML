"""Simple data builder module."""

from lxml import etree  # type: ignore

from pyLiveKML import (
    AnimatedUpdate,
    FlyTo,
    FlyToModeEnum,
    PlayModeEnum,
    SoundCue,
    Tour,
    TourControl,
    UpdateSequent,
    UpdateType,
    Wait,
    Document,
    IconStyle,
    LookAt,
    Placemark,
    Point,
    Style,
    Tour,
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
    anim_update_style = IconStyle(scale=3)
    anim_update_style._id = anim_base_style._id
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
