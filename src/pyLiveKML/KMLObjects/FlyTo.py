"""FlyTo module."""

from typing import Iterator

from lxml import etree  # type: ignore

from pyLiveKML.KML import FlyToModeEnum
from pyLiveKML.KML.Object import _FieldDef
from pyLiveKML.KMLObjects.AbstractView import AbstractView
from pyLiveKML.KML.Object import _ChildDef
from pyLiveKML.KMLObjects.TourPrimitive import TourPrimitive


class FlyTo(TourPrimitive):
    """A KML 'gx:FlyTo', per https://developers.google.com/kml/documentation/kmlreference#gxflyto."""

    _kml_tag = "gx:FlyTo"
    _kml_fields = TourPrimitive._kml_fields + (
        _FieldDef("duration"),
        _FieldDef("fly_to_mode", "flyToMode"),
    )
    _direct_children = TourPrimitive._direct_children + (_ChildDef("abstract_view"),)

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
