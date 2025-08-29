"""MultiGeometry module."""

from typing import Iterator, Sequence

from lxml import etree  # type: ignore

from pyLiveKML.KMLObjects.Geometry import Geometry
from pyLiveKML.KMLObjects.Object import ObjectChild


class MultiGeometry(Geometry, list[Geometry]):
    """A KML 'MultiGeometry', per https://developers.google.com/kml/documentation/kmlreference#multigeometry."""

    _kml_tag = "MultiGeometry"

    def __init__(self, contents: Geometry | Sequence[Geometry] | None = None):
        """Folder instance constructor."""
        Geometry.__init__(self)
        if contents is not None:
            if isinstance(contents, Geometry):
                self.append(contents)
            else:
                self.extend(contents)

    @property
    def children(self) -> Iterator[ObjectChild]:
        """The children of the instance."""
        for g in self:
            yield ObjectChild(parent=self, child=g)

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        if with_children:
            for g in self:
                root.append(g.construct_kml())
