"""FlyTo module."""

from typing import Iterator

from lxml import etree  # type: ignore

from pyLiveKML.KML import FlyToModeEnum, with_ns
from pyLiveKML.KML._BaseObject import _FieldDef, DumpDirect, NoParse
from pyLiveKML.KML.KMLObjects.AbstractView import AbstractView
from pyLiveKML.KML.KMLObjects.Object import ObjectChild
from pyLiveKML.KML.KMLObjects.TourPrimitive import TourPrimitive


class GxFlyTo(TourPrimitive):
    """A KML 'gx:FlyTo', per https://developers.google.com/kml/documentation/kmlreference#gxflyto."""

    _kml_type = "gx:FlyTo"
    _kml_fields = TourPrimitive._kml_fields + (
        _FieldDef("duration", NoParse, "duration", DumpDirect),
        _FieldDef("fly_to_mode", NoParse, "flyToMode", DumpDirect),
    )
    _direct_children = TourPrimitive._direct_children + ("abstract_view",)

    def __init__(
        self,
        duration: float,
        fly_to_mode: FlyToModeEnum,
        abstract_view: AbstractView,
    ) -> None:
        """Track instance constructor."""
        TourPrimitive.__init__(self)
        self.duration = duration
        self.fly_to_mode = fly_to_mode
        self.abstract_view = abstract_view

    @property
    def children(self) -> Iterator[ObjectChild]:
        """The children of the instance."""
        yield ObjectChild(self, self.abstract_view)
