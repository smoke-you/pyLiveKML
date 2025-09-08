"""TimePrimitive module."""

from abc import ABC

from pyLiveKML.objects.Object import Object


class TimePrimitive(Object, ABC):
    """A KML `<TimePrimitive>` tag constructor.

    This is an abstract class and cannot be used directly in a KML file. Extended by the
    `TimeSpan` and `TimeStamp` (and `GxTimeSpan` and `GxTimeStamp`) classes.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference

    Parameters
    ----------
    Nil

    Attributes
    ----------
    Nil

    """

    def __init__(self) -> None:
        """TimePrimitive instance constructor."""
        Object.__init__(self)
        ABC.__init__(self)
