"""Update module."""

from abc import ABC
from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML.KML.Object import _BaseObject, _FieldDef, ObjectChild
from pyLiveKML.KML.utils import with_ns


class _UpdateList(_BaseObject, list[ObjectChild], ABC):

    def __init__(self, items: ObjectChild | Iterable[ObjectChild] | None = None) -> None:
        _BaseObject.__init__(self)
        list[ObjectChild].__init__(self)
        ABC.__init__(self)
        if items is not None:
            if isinstance(items, ObjectChild):
                self.append(items)
            else:
                self.extend(items)


class CreateList(_UpdateList):

    _kml_tag = "Create"

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        for c in (c for c in self if not c.parent._suppress_id):
            c.child.create_kml(root, c.parent)
        self.clear()


class ChangeList(_UpdateList):

    _kml_tag = "Change"

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        for c in (c for c in self if not c.child._suppress_id):
            c.child.change_kml(root)
        self.clear()


class DeleteList(_UpdateList):

    _kml_tag = "Delete"

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        for c in (c for c in self if not c.child._suppress_id):
            c.child.delete_kml(root)
        self.clear()


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
    _kml_fields = _BaseObject._kml_fields + (_FieldDef("target_href", "targetHref"),)

    def __init__(
        self,
        target_href: str,
        creates: ObjectChild | Iterable[ObjectChild] | None = None,
        changes: ObjectChild | Iterable[ObjectChild] | None = None,
        deletes: ObjectChild | Iterable[ObjectChild] | None = None,
    ):
        """Update instance constructor."""
        super().__init__()
        self.target_href = target_href
        self.creates = CreateList(creates)
        self.changes = ChangeList(changes)
        self.deletes = DeleteList(deletes)

    def clear(self) -> None:
        self.creates.clear()
        self.changes.clear()
        self.deletes.clear()

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        if self.creates:
            root.append(self.creates.construct_kml())
        if self.changes:
            root.append(self.changes.construct_kml())
        if self.deletes:
            root.append(self.deletes.construct_kml())
