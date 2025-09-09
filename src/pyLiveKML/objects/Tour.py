"""Tour module."""

from typing import Iterable, Iterator

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import (
    _BaseObject,
    _ChildDef,
    _DeletableMixin,
    _DependentDef,
    _FieldDef,
    _ListObject,
    Object,
)
from pyLiveKML.objects.TourPrimitive import TourPrimitive


class Playlist(_DeletableMixin, _ListObject[TourPrimitive], _BaseObject):
    """A KML `<Playlist>` tag constructor.

    Contains any number of `TourPrimitive` objects.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#contains_6

    Parameters
    ----------
    items : TourPrimitive | Iterable[TourPrimitive] | None, default = None
        The `TourPrimitive` items in the playlist.

    Attributes
    ----------
    Nil

    """

    _kml_tag = "gx:Playlist"
    _kml_children = _BaseObject._kml_children + (_ChildDef("items"),)
    _yield_self = True

    def __init__(
        self, items: TourPrimitive | Iterable[TourPrimitive] | None = None
    ) -> None:
        """Playlist instance constructor."""
        _DeletableMixin.__init__(self)
        _ListObject[TourPrimitive].__init__(self)
        _BaseObject.__init__(self)
        self.items = items

    @property
    def items(self) -> Iterator[TourPrimitive]:
        """Retrieve a generator over the `TourPrimitive`s in this `Tour`.

        If the property setter is called, replaces the current list of contained
        `TourPrimitive`s with those provided.

        Parameters
        ----------
        value : TourPrimitive | Iterable[TourPrimitive] | None
            The new `TourPrimitive` elements for the `Tour`.

        :returns: A generator over the `TourPrimitive`s in the `Tour`.
        :rtype: Iterator[TourPrimitive]

        """
        yield from self

    @items.setter
    def items(self, value: TourPrimitive | Iterable[TourPrimitive] | None) -> None:
        self.clear()
        if value is not None:
            if isinstance(value, TourPrimitive):
                self.append(value)
            else:
                self.extend(value)


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
    _kml_dependents = Object._kml_dependents + (_DependentDef("playlist"),)

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
