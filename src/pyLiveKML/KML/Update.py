"""Update module."""

from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML.KML import with_ns
from pyLiveKML.KML._BaseObject import _BaseObject, _FieldDef, DumpDirect, NoParse


class Update(_BaseObject):
    """Update tag class.

    Refer https://developers.google.com/kml/documentation/kmlreference#update.

    Specifies an addition, change, or deletion to KML data that has already been loaded
    using the specified URL. The <targetHref> specifies the .kml or .kmz file whose data
    (within Google Earth) is to be modified. <Update> is always contained in a
    <NetworkLinkControl> (N.B. or a <gx:AnimatedUpdate>). Furthermore, the file
    containing the <NetworkLinkControl> must have been loaded by a <NetworkLink>. See the
    "Topics in KML" page on Updates for a detailed example of how <Update> works.

    :param str target_href: Specifies the .kml or .kmz file whose data (within Google
        Earth) is to be modified
    :param etree.Element|Iterable[etree.Element]|None creates: An optional KML
        element, or iterable of KML elements, to be inserted under a child <Create> tag.
    :param etree.Element|Iterable[etree.Element]|None changes: An optional KML
        element, or iterable of KML elements, to be inserted under a child <Change> tag.
    :param etree.Element|Iterable[etree.Element]|None changes: An optional KML
        element, or iterable of KML elements, to be inserted under a child <Delete> tag.
    """

    _kml_tag = "Update"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("target_href", NoParse, "targetHref", DumpDirect),
    )

    def __init__(
        self,
        target_href: str,
        creates: etree.Element | Iterable[etree.Element] | None = None,
        changes: etree.Element | Iterable[etree.Element] | None = None,
        deletes: etree.Element | Iterable[etree.Element] | None = None,
    ):
        """Update instance constructor."""
        super().__init__()
        self.target_href = target_href
        self.creates = list[etree.Element]()
        self.changes = list[etree.Element]()
        self.deletes = list[etree.Element]()
        if creates is not None:
            if isinstance(creates, etree.Element):
                self.creates.append(creates)
            else:
                self.creates.extend(creates)
        if changes is not None:
            if isinstance(changes, etree.Element):
                self.changes.append(changes)
            else:
                self.changes.extend(changes)
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
