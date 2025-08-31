"""Tour module."""

from typing import Iterator, Iterable

from lxml import etree  # type: ignore

from pyLiveKML.KML.Object import _BaseObject, _FieldDef
from pyLiveKML.KML.utils import with_ns
from pyLiveKML.KML.Object import Object, _ListObject
from pyLiveKML.KMLObjects.TourPrimitive import TourPrimitive


class Playlist(_ListObject[TourPrimitive], _BaseObject):
    """Playlist child object, per https://developers.google.com/kml/documentation/kmlreference#gxtour."""

    _kml_tag = "gx:PlayList"

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
    """A KML 'gx:Tour', per https://developers.google.com/kml/documentation/kmlreference#gxtour."""

    _kml_tag = "gx:Tour"
    _kml_fields = Object._kml_fields + (
        _FieldDef("name"),
        _FieldDef("description"),
    )

    def __init__(
        self,
        name: str | None = None,
        description: str | None = None,
        playlist: TourPrimitive | list[TourPrimitive] | None = None,
    ) -> None:
        """Track instance constructor."""
        Object.__init__(self)
        self.name = name
        self.description = description
        self.playlist = Playlist(playlist)
