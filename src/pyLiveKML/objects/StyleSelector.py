"""StyleSelector module."""

from abc import ABC

from pyLiveKML.objects.Object import Object


class StyleSelector(Object, ABC):
    """A KML `<StyleSelector>` tag constructor.

    This is an abstract element and cannot be used directly in a KML file. It is the base
    type for `Style` and `StyleMap`. An object derived from `StyleSelector` is uniquely
    identified by its id and its url.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#styleselector.

    Parameters
    ----------
    Nil

    Attributes
    ----------
    Nil

    """

    def __init__(self) -> None:
        """StyleSelector instance constructor."""
        Object.__init__(self)
        ABC.__init__(self)
