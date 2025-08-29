"""Tour module."""

from typing import Iterator

from lxml import etree  # type: ignore

from pyLiveKML.KML import with_ns
from pyLiveKML.KML._BaseObject import (
    _FieldDef,
    DumpDirect,
    NoParse,
)
from pyLiveKML.KML.KMLObjects.Object import Object, ObjectChild
from pyLiveKML.KML.KMLObjects.TourPrimitive import TourPrimitive


class GxTour(Object, list[TourPrimitive]):
    """A KML 'gx:Tour', per https://developers.google.com/kml/documentation/kmlreference#gxtour."""

    _kml_type = "gx:Tour"
    _kml_fields = Object._kml_fields + (
        _FieldDef("name", NoParse, "name", DumpDirect),
        _FieldDef("description", NoParse, "description", DumpDirect),
    )

    def __init__(
        self,
        name: str | None = None,
        description: str | None = None,
        tours: TourPrimitive | list[TourPrimitive] | None = None,
    ) -> None:
        """Track instance constructor."""
        Object.__init__(self)
        list[TourPrimitive].__init__(self)
        self.name = name
        self.description = description
        if tours is not None:
            if isinstance(tours, TourPrimitive):
                self.append(tours)
            else:
                self.extend(tours)

    @property
    def children(self) -> Iterator[ObjectChild]:
        """The children of the instance."""
        for t in self:
            yield ObjectChild(parent=self, child=t)

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        if with_children:
            if len(self) > 0:
                tours = etree.SubElement(root, with_ns("gx:Playlist"))
                for t in self:
                    tours.append(t.construct_kml())
