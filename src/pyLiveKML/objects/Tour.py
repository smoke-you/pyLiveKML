"""Tour module."""

from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import _BaseObject, _DependentDef, _FieldDef, _ListObject, Object
from pyLiveKML.objects.TourPrimitive import TourPrimitive


class Playlist(_ListObject[TourPrimitive], _BaseObject):
    """A KML `<Playlist>` tag constructor.

    Contains any number of `TourPrimitive` objects.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#contains_6

    Parameters
    ----------
    items : TourPrimitive | Iterable[TourPrimitive] | None, default = None

    Attributes
    ----------
    Nil

    """

    _kml_tag = "gx:Playlist"

    def __init__(
        self, items: TourPrimitive | Iterable[TourPrimitive] | None = None
    ) -> None:
        """Playlist instance constructor."""
        _BaseObject.__init__(self)
        _ListObject[TourPrimitive].__init__(self)
        if items is not None:
            if isinstance(items, TourPrimitive):
                self.append(items)
            else:
                self.extend(items)


class Tour(Object):
    """A KML `<gx:Tour>` tag constructor.
    
    A `Tour` contains a single `PlayList`, which in turn contains an ordered list of 
    `TourPrimitive` elements that define a tour in any KML browser.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#gxtour
    * https://developers.google.com/kml/documentation/touring

    Parameters
    ----------    
    name: str | None, default = None
    description: str | None, default = None
    playlist: TourPrimitive | list[TourPrimitive] | None, default = None
    
    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "gx:Tour"
    _kml_fields = Object._kml_fields + (
        _FieldDef("name"),
        _FieldDef("description"),
    )
    _kml_dependents = Object._kml_dependents + (
        _DependentDef("playlist"),
    )

    def __init__(
        self,
        name: str | None = None,
        description: str | None = None,
        playlist: TourPrimitive | list[TourPrimitive] | None = None,
    ) -> None:
        """Tour instance constructor."""
        Object.__init__(self)
        self.name = name
        self.description = description
        self.playlist = Playlist(playlist)
