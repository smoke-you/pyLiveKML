"""Wait module."""

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import _FieldDef
from pyLiveKML.objects.TourPrimitive import TourPrimitive


class Wait(TourPrimitive):
    """A KML `<gx:Wait>` tag constructor.

    The camera remains still, at the last-defined `AbstractView`, for the number of
    seconds specified before playing the next `TourPrimitive`.

    Notes
    -----
    * A `Wait` does not pause the tour timeline - currently-playing sound files and
    animated updates will continue to play while the camera is waiting.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#gxwait

    Parameters
    ----------
    duration : float, default = 0
        The time in seconds to wait.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "gx:Wait"
    _kml_fields = TourPrimitive._kml_fields + (_FieldDef("duration", "gx:duration"),)

    def __init__(
        self,
        duration: float = 0,
    ) -> None:
        """Wait instance constructor."""
        TourPrimitive.__init__(self)
        self.duration = duration
