"""FlyTo module."""

from lxml import etree  # type: ignore

from pyLiveKML.types import FlyToModeEnum
from pyLiveKML.objects.Object import _FieldDef, _ChildDef
from pyLiveKML.objects.AbstractView import AbstractView
from pyLiveKML.objects.TourPrimitive import TourPrimitive


class FlyTo(TourPrimitive):
    """A KML 'gx:FlyTo', per https://developers.google.com/kml/documentation/kmlreference#gxflyto."""

    _kml_tag = "gx:FlyTo"
    _kml_fields = TourPrimitive._kml_fields + (
        _FieldDef("duration"),
        _FieldDef("fly_to_mode", "flyToMode"),
    )
    _kml_children = TourPrimitive._kml_children + (_ChildDef("abstract_view"),)

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
