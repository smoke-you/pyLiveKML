"""TourPrimitive module."""

from abc import ABC

from pyLiveKML.objects.Object import Object


class TourPrimitive(Object, ABC):
    """A KML `<TourPrimitive>` tag constructor.

    This is an abstract element and cannot be used directly in a KML file.

    Objects inheriting from `TourPrimitive` provide instructions to KML browsers during
    tours, including points to fly to and the duration of those flights, pauses, updates
    to KML features, and sound files to play.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#tourprimitive

    Parameters
    ----------
    Nil

    Attributes
    ----------
    Nil

    """

    def __init__(self) -> None:
        """TourPrimitive instance constructor."""
        Object.__init__(self)
        ABC.__init__(self)
