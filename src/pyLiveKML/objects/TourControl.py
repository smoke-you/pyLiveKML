"""TourControl module."""

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import _FieldDef
from pyLiveKML.objects.TourPrimitive import TourPrimitive
from pyLiveKML.types import PlayModeEnum


class TourControl(TourPrimitive):
    """A KML `<gx:TourControl>` tag constructor.

    Allows a `Tour` to be paused, until the user takes action to continue the `Tour`.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#extended-by_8

    Parameters
    ----------
    play_mode : PlayModeEnum, default = PlayModeEnum.PAUSE

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "gx:TourControl"
    _kml_fields = TourPrimitive._kml_fields + (_FieldDef("play_mode", "gx:playMode"),)

    def __init__(
        self,
        play_mode: PlayModeEnum = PlayModeEnum.PAUSE,
    ) -> None:
        """GxTourControl instance constructor."""
        TourPrimitive.__init__(self)
        self.play_mode = play_mode
