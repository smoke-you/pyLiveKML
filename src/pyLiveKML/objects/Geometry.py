"""Geometry module."""

from abc import ABC

from pyLiveKML.objects.Object import Object


class Geometry(Object, ABC):
    """A KML `<Geometry>` tag constructor.

    This is an abstract element and cannot be used directly in a KML file. It provides a
    placeholder object for all derived `<Geometry>` objects.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#geometry.

    Parameters
    ----------
    Nil

    Attributes
    ----------
    Nil

    """

    def __init__(self) -> None:
        """Geometry instance constructor."""
        Object.__init__(self)
        ABC.__init__(self)
