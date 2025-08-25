"""AbstractView module."""

from abc import ABC
from typing import Iterator, Sequence

from lxml import etree  # type: ignore

from pyLiveKML.KML.KMLObjects.Object import Object, ObjectChild
from pyLiveKML.KML.KMLObjects.TimePrimitive import TimePrimitive
from pyLiveKML.KML.KML import GxViewerOption


class AbstractView(Object, ABC):
    """A KML 'Abstract', per https://developers.google.com/kml/documentation/kmlreference#abstractview."""

    def __init__(
        self,
        viewer_options: Sequence[GxViewerOption] | GxViewerOption | None = None,
        time_primitive: TimePrimitive | None = None,
    ) -> None:
        """AbstractView instance constructor."""
        Object.__init__(self)
        ABC.__init__(self)
        self._viewer_options = list[GxViewerOption]()
        if viewer_options is not None:
            if isinstance(viewer_options, GxViewerOption):
                self._viewer_options.append(viewer_options)
            else:
                self._viewer_options.extend(viewer_options)
        self._time_primitive = time_primitive

    @property
    def time_primitive(self) -> TimePrimitive | None:
        """The TimePrimitive associated with this Feature."""
        return self._time_primitive

    @time_primitive.setter
    def time_primitive(self, value: TimePrimitive | None) -> None:
        if self._time_primitive != value:
            self._time_primitive = value
            self.field_changed()

    @property
    def viewer_options(self) -> list[GxViewerOption]:
        """The viewer options associated with this Feature."""
        return self._viewer_options

    @property
    def children(self) -> Iterator[ObjectChild]:
        """The children of this instance."""
        if self.time_primitive is not None:
            yield ObjectChild(parent=self, child=self.time_primitive)

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        if self._viewer_options:
            opts = etree.SubElement(root, "gx:ViewerOptions")
            for v in self._viewer_options:
                etree.SubElement(
                    opts,
                    "gx:option",
                    attribs={"name": v.name.value, "enabled": str(int(v.enabled))},
                )
        if with_children:
            if self.time_primitive is not None:
                root.append(self.time_primitive.construct_kml())
