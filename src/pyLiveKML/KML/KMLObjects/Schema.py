"""Schema module."""

from typing import Any, Iterator, Iterable, Sequence, NamedTuple

from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import (
    AltitudeMode,
    Angle90,
    Angle180,
    AnglePos180,
    Angle360,
    _FieldDef,
    NoParse,
    DumpDirect,
    NoDump,
)
from pyLiveKML.KML._BaseObject import _BaseObject
from pyLiveKML.KML.KMLObjects.Model import Model
from pyLiveKML.KML.KMLObjects.Object import Object, ObjectChild
from pyLiveKML.KML.KMLObjects.TimeStamp import TimeStamp


class SimpleField(_BaseObject):
    _kml_type = "SimpleField"

    def __init__(
        self,
        type: str,
        name: str,
        display_names: str | Iterable[str] | None,
    ) -> None:
        self.type = type
        self.name = name
        self.display_names = list[str]()
        if display_names:
            if isinstance(display_names, str):
                self.display_names.append(display_names)
            else:
                self.display_names.extend(display_names)

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        for dn in self.display_names:
            etree.SubElement(root, "displayName").text = dn

    def construct_kml(self) -> etree.Element:
        # attribs = { "type": self.type, "name": self.name }
        root = etree.Element(self.kml_type, type=self.type, name=self.name)
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
        """Model instance constructor."""
        Object.__init__(self)
        self.name = name
        self.fields = list[SimpleField]()
        if isinstance(fields, SimpleField):
            self.fields.append(fields)
        else:
            self.fields.extend(fields)

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        for f in self.fields:
            root.append(f.construct_kml())

    def construct_kml(self) -> etree.Element:
        # attribs = { "name": self.name, "id": str(self.id) }
        root = etree.Element(self.kml_type, name=self.name, id=str(self.id))
        self.build_kml(root)
        return root
