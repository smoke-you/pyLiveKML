"""SubStyle module."""

from abc import ABC

from pyLiveKML.objects.Object import _FieldDef, Object


class SubStyle(Object, ABC):
    """A KML `<SubStyle>` tag constructor.

    This is an abstract element and cannot be used directly in a KML file.

    Notes
    -----
    There is no description of the `SubStyle` class in the Google KML documentation,
    although it is include in the inheritance tree at the top of the page.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference.

    Parameters
    ----------
    Nil

    Attributes
    ----------
    Nil

    """

    _kml_fields: tuple[_FieldDef, ...] = tuple()

    def __init__(self) -> None:
        """SubStyle instance constructor."""
        Object.__init__(self)
        ABC.__init__(self)
