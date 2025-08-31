"""AbstractView module."""

from abc import ABC
from typing import Iterator, Iterable

from lxml import etree  # type: ignore

from pyLiveKML.KML.ViewerOption import ViewerOption
from pyLiveKML.KML.utils import with_ns
from pyLiveKML.KML.Object import Object, ObjectChild, _ChildDef
from pyLiveKML.KMLObjects.TimePrimitive import TimePrimitive


class AbstractView(Object, ABC):
    """A KML 'AbstractView', per https://developers.google.com/kml/documentation/kmlreference#abstractview."""

    _direct_children = Object._direct_children + (_ChildDef("time_primitive"),)

    def __init__(
        self,
        viewer_options: Iterable[ViewerOption] | ViewerOption | None = None,
        time_primitive: TimePrimitive | None = None,
    ) -> None:
        """AbstractView instance constructor."""
        Object.__init__(self)
        ABC.__init__(self)
        self._viewer_options = list[ViewerOption]()
        if viewer_options is not None:
            if isinstance(viewer_options, ViewerOption):
                self._viewer_options.append(viewer_options)
            else:
                self._viewer_options.extend(viewer_options)
        self.time_primitive = time_primitive

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        if self._viewer_options:
            opts = etree.SubElement(root, with_ns("gx:ViewerOptions"))
            for v in self._viewer_options:
                v.build_kml(opts)
