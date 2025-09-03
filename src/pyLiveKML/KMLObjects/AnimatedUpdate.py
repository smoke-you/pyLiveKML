"""AnimatedUpdate module."""

from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML.KML.Object import _FieldDef
from pyLiveKML.KML.Update import Update
from pyLiveKML.KML.Object import _ChildDef
from pyLiveKML.KMLObjects.TourPrimitive import TourPrimitive


class AnimatedUpdate(TourPrimitive):
    """A KML 'gx:AnimatedUpdate', per https://developers.google.com/kml/documentation/kmlreference#gxanimatedupdate."""

    _kml_tag = "gx:AnimatedUpdate"
    _kml_fields = TourPrimitive._kml_fields + (
        _FieldDef("delayed_start", "gx:delayedStart"),
        _FieldDef("duration", "gx:duration"),
    )
    _kml_children = TourPrimitive._kml_children + (_ChildDef("update"),)

    def __init__(
        self,
        delayed_start: float = 0,
        duration: float = 0,
        target_href: str = "",
        changes: etree.Element | Iterable[etree.Element] | None = None,
        creates: etree.Element | Iterable[etree.Element] | None = None,
        deletes: etree.Element | Iterable[etree.Element] | None = None,
    ) -> None:
        """GxAnimatedUpdate instance constructor."""
        TourPrimitive.__init__(self)
        self.delayed_start = delayed_start
        self.duration = duration
        self.update = Update(target_href, changes, creates, deletes)
