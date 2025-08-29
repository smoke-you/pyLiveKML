"""Update module."""

from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML.KML._BaseObject import _BaseObject
from pyLiveKML.KML.KML import with_ns, _FieldDef, NoDump, NoParse


class Update(_BaseObject):
    """Update tag class."""

    _kml_type = "Update"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("target_href", NoParse, "targetHref", NoDump),
    )

    def __init__(
        self,
        target_href: str,
        changes: etree.Element | Iterable[etree.Element] | None = None,
        creates: etree.Element | Iterable[etree.Element] | None = None,
        deletes: etree.Element | Iterable[etree.Element] | None = None,
    ):
        """Update instance constructor."""
        super().__init__()
        self.target_href = target_href
        self.changes = list[etree.Element]()
        self.creates = list[etree.Element]()
        self.deletes = list[etree.Element]()
        if changes is not None:
            if isinstance(changes, etree.Element):
                self.changes.append(changes)
            else:
                self.changes.extend(changes)
        if creates is not None:
            if isinstance(creates, etree.Element):
                self.creates.append(creates)
            else:
                self.creates.extend(creates)
        if deletes is not None:
            if isinstance(deletes, etree.Element):
                self.deletes.append(deletes)
            else:
                self.deletes.extend(deletes)

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        if self.changes:
            etree.SubElement(root, with_ns("Change")).extend(self.changes)
        if self.creates:
            etree.SubElement(root, with_ns("Create")).extend(self.creates)
        if self.deletes:
            etree.SubElement(root, with_ns("Delete")).extend(self.deletes)
                

    