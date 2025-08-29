"""Schema module."""

from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML.KML._BaseObject import _BaseObject
from pyLiveKML.KML.KMLObjects.Object import Object


class SimpleField(_BaseObject):
    """SimpleField class.

    `Schema` instances contain a collection of `SimpleField` instances.
    """

    _kml_type = "SimpleField"

    def __init__(
        self,
        type: str,
        name: str,
        display_names: str | Iterable[str] | None,
    ) -> None:
        """SimpleField instance constructor."""
        self.type = type
        self.name = name
        self.display_names = list[str]()
        if display_names:
            if isinstance(display_names, str):
                self.display_names.append(display_names)
            else:
                self.display_names.extend(display_names)

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        for dn in self.display_names:
            etree.SubElement(root, "displayName").text = dn

    def construct_kml(self) -> etree.Element:
        """Construct this instances' KML representation."""
        root = etree.Element(
            self.kml_type, attrib={"type": self.type, "name": self.name}
        )
        self.build_kml(root)
        return root


class Schema(Object):
    """A KML 'Schema', per https://developers.google.com/kml/documentation/kmlreference#schema."""

    _kml_type = "Schema"

    def __init__(
        self,
        name: str,
        fields: SimpleField | Iterable[SimpleField],
    ) -> None:
        """Construct Schema instances."""
        Object.__init__(self)
        self.name = name
        self.fields = list[SimpleField]()
        if isinstance(fields, SimpleField):
            self.fields.append(fields)
        else:
            self.fields.extend(fields)

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        for f in self.fields:
            root.append(f.construct_kml())

    def construct_kml(self) -> etree.Element:
        """Construct this instances' KML representation."""
        root = etree.Element(
            self.kml_type, attrib={"name": self.name, "id": str(self.id)}
        )
        self.build_kml(root)
        return root
