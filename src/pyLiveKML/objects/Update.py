"""Update module."""

from abc import ABC
from enum import Enum
from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import _BaseObject, _FieldDef, ObjectChild


class UpdateType(Enum):
    """Enumeration of the child tags that may be contained in an `<Update>` tag."""

    CREATE = "Create"
    CHANGE = "Change"
    DELETE = "Delete"


class UpdateSequent(ObjectChild):
    """An element in an Update sequence.

    Parameters
    ----------
    tag : UpdateType
        The `<Update>` sub-tag for the element.
    parent : _BaseObject
        The parent object for any `<Create>` tags. Required for the `id` field.
    child : _BaseObject
        The target object that will be created, changed or deleted.

    Attributes
    ----------
    Same as parameters.

    """

    def __init__(
        self, tag: UpdateType, parent: _BaseObject, child: _BaseObject
    ) -> None:
        """UpdateSequent instance constructor."""
        super().__init__(parent, child)
        self.tag = tag


class _UpdateSequence(_BaseObject, list[UpdateSequent]):
    """A sequence of create, change and delete operations to be executed.

    This sequence will be executed in the order in which it is stored. The primary
    purpose, compared to the :class:`pyLiveKML.objects.Update._UpdateList` subclasses,
    below, is to allow a completely arbitrary sub-tag order for `<Update>` tags. This is
    relevant to :class:`pyLiveKML.objects.AnimatedUpdate`.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#update
    * https://developers.google.com/kml/documentation/kmlreference#example-of-create
    * https://developers.google.com/kml/documentation/kmlreference#example-of-change
    * https://developers.google.com/kml/documentation/kmlreference#example-of-delete

    Parameters
    ----------
    items : UpdateSequent | Iterable[UpdateSequent] | None, default = None
        The initial sequence of `UpdateSequent` items.

    """

    _suppress_id = True

    def __init__(
        self,
        items: UpdateSequent | Iterable[UpdateSequent] | None = None,
    ):
        _BaseObject.__init__(self)
        list[UpdateSequent].__init__(self)
        if items is not None:
            if isinstance(items, UpdateSequent):
                self.append(items)
            else:
                self.extend(items)

    def build_kml(
        self,
        root: etree.Element,
        with_children: bool = True,
        with_dependents: bool = True,
    ) -> None:
        """Construct the KML content and append it to the provided etree.Element.

        Overridden from `_ObjectBase` to ensure specific behaviour.

        Notes
        -----
        * Unlike the other update list types, **does not** clear the list after
        publishing it.

        """
        for s in self:
            if s.tag == UpdateType.CREATE:
                if not s.parent._suppress_id:
                    create_tag = etree.SubElement(root, s.tag.value)
                    s.child.create_kml(create_tag, s.parent)
            elif s.tag == UpdateType.CHANGE:
                if not s.child._suppress_id:
                    change_tag = etree.SubElement(root, s.tag.value)
                    s.child.change_kml(change_tag)
            elif s.tag == UpdateType.DELETE:
                if not s.child._suppress_id:
                    delete_tag = etree.SubElement(root, s.tag.value)
                    s.child.delete_kml(delete_tag)


class _UpdateList(_BaseObject, list[ObjectChild], ABC):
    """Abstract base for `_CreateList`, `_ChangeList` and `_DeleteList`."""

    def __init__(
        self,
        items: ObjectChild | Iterable[ObjectChild] | None = None,
    ) -> None:
        _BaseObject.__init__(self)
        list[ObjectChild].__init__(self)
        ABC.__init__(self)
        if items is not None:
            if isinstance(items, ObjectChild):
                self.append(items)
            else:
                self.extend(items)


class _CreateList(_UpdateList):
    """A KML `<Create>` tag constructor.

    Always a child of an `Update` instance.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#example-of-create

    Parameters
    ----------
    Nil

    Attributes
    ----------
    Nil

    """

    _kml_tag = "Create"

    def build_kml(
        self,
        root: etree.Element,
        with_children: bool = True,
        with_dependents: bool = True,
    ) -> None:
        """Construct the KML content and append it to the provided etree.Element.

        Overridden from `_ObjectBase` to ensure specific behaviour, including clearing
        the list after publishing the KML.
        """
        for c in (c for c in self if not c.parent._suppress_id):
            c.child.create_kml(root, c.parent)
        self.clear()


class _ChangeList(_UpdateList):
    """A KML `<Change>` tag constructor.

    Always a child of an `Update` instance.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#example-of-change

    Parameters
    ----------
    Nil

    Attributes
    ----------
    Nil

    """

    _kml_tag = "Change"

    def build_kml(
        self,
        root: etree.Element,
        with_children: bool = True,
        with_dependents: bool = True,
    ) -> None:
        """Construct the KML content and append it to the provided etree.Element.

        Overridden from `_ObjectBase` to ensure specific behaviour, including clearing
        the list after publishing the KML.
        """
        for c in (c for c in self if not c.child._suppress_id):
            c.child.change_kml(root)
        self.clear()


class _DeleteList(_UpdateList):
    """A KML `<Delete>` tag constructor.

    Always a child of an `Update` instance.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#example-of-delete

    Parameters
    ----------
    Nil

    Attributes
    ----------
    Nil

    """

    _kml_tag = "Delete"

    def build_kml(
        self,
        root: etree.Element,
        with_children: bool = True,
        with_dependents: bool = True,
    ) -> None:
        """Construct the KML content and append it to the provided etree.Element.

        Overridden from `_ObjectBase` to ensure specific behaviour, including clearing
        the list after publishing the KML.
        """
        for c in (c for c in self if not c.child._suppress_id):
            c.child.delete_kml(root)
        self.clear()


class Update(_BaseObject):
    """A KML `<Update>` tag constructor.

    Specifies additions, changes, or deletions to KML data that has already been loaded
    using the specified URL. `target_href` specifies the .kml or .kmz file whose data
    (within Google Earth) is to be modified. `Update` is always* contained in a
    `NetworkLinkControl`. Furthermore, the file containing the `NetworkLinkControl` must
    have been loaded by a `NetworkLink`.

    Notes
    -----
    * `AnimatedUpdate` may also contain an `Update` tag.
    * The `creates`, `changes` and `deletes` attributes each construct and populate a
    single child tag of the appropriate type, **in that order**. That is, **all** creates
    are emitted, then **all** changes, then **all** deletes. This is optimal for
    pyLiveKML synchronization purposes, but can be problematic for e.g. `AnimatedUpdate`.
    The `sequence` attribute allows an arbitrary ordering of child tags, suitable for
    `AnimatedUpdate`, or any other situation in which a specific ordering of child tags
    is required.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#syntax_50

    Parameters
    ----------
    target_href : str
    creates : ObjectChild | Iterable[ObjectChild] | None, default = None
        A collection of ObjectChild instances to be created.
    changes : ObjectChild | Iterable[ObjectChild] | None, default = None
        A collection of ObjectChild instances to be changed.
    deletes : ObjectChild | Iterable[ObjectChild] | None, default = None
        A collection of ObjectChild instances to be deleted.
    sequence : UpdateSequent | Iterable[UpdateSequent] | None, default = None
        An ordered list of update operations.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "Update"
    _kml_fields = _BaseObject._kml_fields + (_FieldDef("target_href", "targetHref"),)

    def __init__(
        self,
        target_href: str,
        creates: ObjectChild | Iterable[ObjectChild] | None = None,
        changes: ObjectChild | Iterable[ObjectChild] | None = None,
        deletes: ObjectChild | Iterable[ObjectChild] | None = None,
        sequence: UpdateSequent | Iterable[UpdateSequent] | None = None,
    ):
        """Update instance constructor."""
        super().__init__()
        self.target_href = target_href
        self.creates = _CreateList(creates)
        self.changes = _ChangeList(changes)
        self.deletes = _DeleteList(deletes)
        self.sequence = _UpdateSequence(sequence)

    def clear(self) -> None:
        """Clear the instance.

        Discards the current contents of the `creates`, `changes`, `deletes` and
        `sequence` lists.
        """
        self.creates.clear()
        self.changes.clear()
        self.deletes.clear()
        self.sequence.clear()

    def __len__(self) -> int:
        """Take the current length of the instance.

        The returned value is the sum of the lengths of the `creates`, `changes` and
        `deletes` lists; it **does not** include the length of the `sequence` list.
        """
        return len(self.creates) + len(self.changes) + len(self.deletes)

    def build_kml(
        self,
        root: etree.Element,
        with_children: bool = True,
        with_dependents: bool = True,
    ) -> None:
        """Construct the KML content and append it to the provided etree.Element.

        Overriden from `_BaseObject` to enforce some specific publishing behaviour.
        """
        super().build_kml(root, with_children, with_dependents)
        if self.creates:
            root.append(self.creates.construct_kml(with_children, with_dependents))
        if self.changes:
            root.append(self.changes.construct_kml(with_children, with_dependents))
        if self.deletes:
            root.append(self.deletes.construct_kml(with_children, with_dependents))
        if self.sequence:
            self.sequence.build_kml(root, with_children, with_dependents)
