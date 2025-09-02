"""SubStyle module."""

from abc import ABC

from pyLiveKML.KML.Object import _FieldDef
from pyLiveKML.KML.Object import Object


class SubStyle(Object, ABC):
    """A KML 'SubStyle', per https://developers.google.com/kml/documentation/kmlreference.

    Note that there is no description of the :class:`~pyLiveKML.KMLObjects.SubStyle`
    class in the Google KML documentation, although it is included in the inheritance
    tree at the top of the page.  The :class:`~pyLiveKML.KMLObjects.SubStyle` class
    is the abstract base class for the specific sub-styles that are optionally included
    as children :class:`~pyLiveKML.KMLObjects.Style` objects.
    """

    _kml_fields: tuple[_FieldDef, ...] = tuple()
    _suppress_id = True

    def __init__(self) -> None:
        """SubStyle instance constructor."""
        Object.__init__(self)
        ABC.__init__(self)
