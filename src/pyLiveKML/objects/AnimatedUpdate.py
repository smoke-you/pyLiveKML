"""AnimatedUpdate module."""

from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import _FieldDef
from pyLiveKML.objects.Update import Update, UpdateSequent
from pyLiveKML.objects.Object import _ChildDef, ObjectChild
from pyLiveKML.objects.TourPrimitive import TourPrimitive


class AnimatedUpdate(TourPrimitive):
    """A KML `<gx:AnimatedUpdate>` tag constructor.

    `<AnimatedUpdate>` controls changes during a tour to KML features, using an
    `<Update>`. Changes to KML features will not modify the DOM - that is, any changes
    will be reverted when the tour is over, and will not be saved in the KML at any time.

    `<AnimatedUpdate>` should also contain a `duration` value to specify the length of
    time in seconds over which the update takes place. Integer, float, and color fields
    are smoothly animated from original to new value across the duration; boolean,
    string, and other values that don't lend to interpolation are updated at the end of
    the duration.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#gxanimatedupdate.

    Parameters
    ----------
    duration : float, default = 0
        Specifies the length of time, in seconds, over which the update takes place.
    delayed_start : float, default = 0
        Specifies the number of seconds to wait (after the inline start position) before
        starting the update.
    target_href : str, default = ""
        The target href for the enclosed :class:`pyLiveKML.objects.Update` instance.
    sequence : UpdateSequent | Iterable[UpdateSequent] | None, default = None
        The sequence of create, change and delete operations to be constructed by the
        enclosed :class:`pyLiveKML.objects.Update` instance.

    Attributes
    ----------
    duration : float, default = 0
        Specifies the length of time, in seconds, over which the update takes place.
    delayed_start : float, default = 0
        Specifies the number of seconds to wait (after the inline start position) before
        starting the update.
    update : Update
        The :class:`pyLiveKML.objects.Update` instance that will generate the animation
        instructions.

    """

    _kml_tag = "gx:AnimatedUpdate"
    _kml_fields = TourPrimitive._kml_fields + (
        _FieldDef("duration", "gx:duration"),
        _FieldDef("delayed_start", "gx:delayedStart"),
    )
    _kml_children = TourPrimitive._kml_children + (_ChildDef("update"),)

    def __init__(
        self,
        duration: float = 0,
        delayed_start: float = 0,
        target_href: str = "",
        sequence: UpdateSequent | Iterable[UpdateSequent] | None = None,
    ) -> None:
        """GxAnimatedUpdate instance constructor."""
        TourPrimitive.__init__(self)
        self.delayed_start = delayed_start
        self.duration = duration
        self.update = Update(target_href, sequence=sequence)
