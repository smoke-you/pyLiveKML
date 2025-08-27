"""Object module."""

from abc import ABC
from collections.abc import Iterable
from typing import Any, Iterator, NamedTuple, Optional
from uuid import uuid4, UUID
from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import ObjectState, ArgParser, NoDump
from pyLiveKML.KML._BaseObject import _BaseObject


class Object(_BaseObject, ABC):
    """A KML 'Object', per https://developers.google.com/kml/documentation/kmlreference#object.

    Note that the :class:`~pyLiveKML.KML.KMLObjects.Object` class is explicitly abstract,
    and is the base class from which most other KML elements (anything with an :attr:`id`
    property) derive.
    """

    _direct_children: tuple[str, ...] = tuple()
    _suppress_id: bool = False

    def __init__(self) -> None:
        """Object instance constructor."""
        super().__init__()
        self._id: UUID = uuid4()
        self._selected: bool = False
        self._container: Optional[Object] = None
        self._state: ObjectState = ObjectState.IDLE

    @property
    def id(self) -> UUID:
        """The unique identifier of this :class:`~pyLiveKML.KML.KMLObjects.Object`."""
        return self._id

    @property
    def state(self) -> ObjectState:
        """The current GEP synchronization state of this :class:`~pyLiveKML.KML.KMLObjects.Object`."""
        return self._state

    @property
    def selected(self) -> bool:
        """Flag to indicate whether the instance has been selected for display.

        True if this :class:`~pyLiveKML.KML.KMLObjects.Object` has been created in the
        UI and is not scheduled for deletion, otherwise False.
        """
        return (
            ObjectState.CREATING,
            ObjectState.CREATED,
            ObjectState.CHANGING,
        ).__contains__(self._state)

    @selected.setter
    def selected(self, value: bool) -> None:
        self.select(value)

    @property
    def children(self) -> Iterator["ObjectChild"]:
        """The children of the instance.

        A generator to retrieve the children of this :class:`~pyLiveKML.KML.KMLObjects.Object` as
        :class:`~pyLiveKML.KML.KMLObjects.Object.ObjectChild` instances.

        :returns: A generator of :class:`~pyLiveKML.KML.KMLObjects.Object.ObjectChild` named tuples that describes
            each child :class:`~pyLiveKML.KML.KMLObjects.Object` as a (parent, child)
        """
        # The return; yield pattern is used to trick linters into accepting that this is a generator that yields
        # nothing, as opposed to yielding None
        return
        yield

    @property
    def direct_children(self) -> Iterator["Object"]:
        """Retrieve a generator over the direct children of the object.

        That is, retrieve any `Object` instances that are embedded in this `Object`.
        """
        for dc in self._direct_children:
            dcobj = getattr(self, dc, None)
            if dcobj:
                if isinstance(dcobj, Iterable):
                    yield from dcobj
                else:
                    yield dcobj

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element.

        Generate the KML representation of the internal fields of this
        :class:`~pyLiveKML.KML.KMLObjects.Object`, and append it to the provided root
        etree.Element.

        :param etree.Element root: The root XML element that will be appended to.
        :param bool with_children: True if the children of this instance should be
            included in the build.
        """
        super().build_kml(root, with_children)
        if with_children:
            for dc in self.direct_children:
                attribs = None
                if not getattr(dc, "_suppress_id", True):
                    attribs = {"id": str(dc.id)}
                dc.build_kml(etree.SubElement(root, dc._kml_type, attrib=attribs), True)

    def construct_kml(self) -> etree.Element:
        """Construct this :class:`~pyLiveKML.KML.KMLObjects.Object`'s KML representation.

        :returns: The KML representation of the object as an etree.Element.
        """
        if self._suppress_id:
            attribs = None
        else:
            attribs = {"id": str(self.id)}
        root = etree.Element(_tag=self.kml_type, attrib=attribs)
        self.build_kml(root)
        return root

    def update_kml(self, parent: "Object", update: etree.Element) -> None:
        """Update this :class:`~pyLiveKML.KML.KMLObjects.Object`'s KML representation.

        Retrieve a complete child <Create>, <Change> or <Delete> KML tag as a child of an <Update> tag.
        The type of child tag retrieved is dependent on the current state of this
        :class:`~pyLiveKML.KML.KMLObjects.Object`.

        :param Object parent: The immediate parent :class:`~pyLiveKML.KML.KMLObjects.Object` of this
            :class:`~pyLiveKML.KML.KMLObjects.Object`. The parent is required only for <Create> tags.
        :param etree.Element update: The etree.Element of the <Update> tag that will be appended to.
        """
        if self._state == ObjectState.CREATING:
            self.create_kml(parent, update)
        elif self._state == ObjectState.CHANGING:
            self.change_kml(update)
        elif (
            self._state == ObjectState.DELETE_CREATED
            or self._state == ObjectState.DELETE_CHANGED
        ):
            self.delete_kml(update)
        self.update_generated()

    def create_kml(self, parent: "Object", update: etree.Element) -> etree.Element:
        """Construct a complete <Create> element tree as a child of an <Update> tag.

        :param Object parent: The immediate parent :class:`~pyLiveKML.KML.KMLObjects.Object` of this
            :class:`~pyLiveKML.KML.KMLObjects.Object`. The parent must be specified for GEP synchronization.
        :param etree.Element update: The etree.Element of the <Update> tag that will be appended to.
        """
        create = etree.Element("Create")
        parent_element = etree.SubElement(
            create, _tag=parent.kml_type, attrib={"targetId": str(parent.id)}
        )
        item = self.construct_kml()
        parent_element.append(item)
        update.append(create)
        return item

    def change_kml(self, update: etree.Element) -> None:
        """Construct a complete <Change> element tree as a child of an <Update> tag.

        :param etree.Element update: The etree.Element of the <Update> tag that will be appended to.
        """
        change = etree.Element("Change")
        item = etree.SubElement(
            change, _tag=self.kml_type, attrib={"targetId": str(self.id)}
        )
        self.build_kml(item, with_children=False)
        update.append(change)

    def delete_kml(self, update: etree.Element) -> None:
        """Construct a complete <Delete> element tree as a child of an <Update> tag.

        :param etree.Element update: The etree.Element of the <Update> tag that will be appended to.
        """
        delete = etree.Element("Delete")
        etree.SubElement(delete, _tag=self.kml_type, attrib={"targetId": str(self.id)})
        update.append(delete)

    def force_idle(self) -> None:
        """Force this :class:`~pyLiveKML.KML.KMLObjects.Object` and **all of its children** to the IDLE state.

        This is typically done after the object has been deselected, which will cause
        it to be deleted from GEP at the next synchronization update. When the
        :class:`~pyLiveKML.KML.KMLObjects.Object` is deleted by GEP, all of its
        children, and any :class:`~pyLiveKML.KML.KMLObjects.Feature` objects that it
        encloses, will also be automatically deleted. There is no need to emit <Delete>
        tags for these deletions, and in fact doing so will likely cause GEP to have
        conniptions.
        """
        self._state = ObjectState.IDLE
        for c in self.children:
            c.child.force_idle()

    def field_changed(self) -> None:
        """Flag that a field or property of this :class:`~pyLiveKML.KML.KMLObjects.Object` has changed.

        If this flag is set, it indicates that re-synchronization with GEP may be required.
        """
        if self._state == ObjectState.CREATED:  # or self._state == State.IDLE:
            self._state = ObjectState.CHANGING
        elif self._state == ObjectState.DELETE_CREATED:
            self._state = ObjectState.DELETE_CHANGED
        elif self._state == ObjectState.IDLE:
            pass

    def update_generated(self) -> None:
        """Modify the state of the :class:`~pyLiveKML.KML.KMLObjects.Object` to reflect that a synchronization update has been emitted."""
        if self._state == ObjectState.CREATING:
            self._state = ObjectState.CREATED
            # if the object is being created, so are all of its descendants, in a single tag; set them created too
            for c in self.children:
                c.child.update_generated()
        elif self._state == ObjectState.CHANGING:
            # if the object is changing, don't mess with its descendants - they are updated elsewhere if necessary
            self._state = ObjectState.CREATED
        elif (
            self._state == ObjectState.DELETE_CREATED
            or self._state == ObjectState.DELETE_CHANGED
        ):
            self._state = ObjectState.IDLE

    def select(self, value: bool, cascade: bool = False) -> None:
        """Select or deselect this :class:`~pyLiveKML.KML.KMLObjects.Object` for display in GEP.

        :param bool value: True for selection, False for deselection
        :param bool cascade: True if the selection is to be cascaded to all child Objects.
        """
        if self._state == ObjectState.CREATING:
            self._state = ObjectState.IDLE if not value else self._state
        elif self._state == ObjectState.CREATED:
            self._state = ObjectState.DELETE_CREATED if not value else self._state
        elif self._state == ObjectState.CHANGING:
            self._state = ObjectState.DELETE_CHANGED if not value else self._state
        elif self._state == ObjectState.DELETE_CREATED:
            self._state = ObjectState.CREATING if value else self._state
        elif self._state == ObjectState.DELETE_CHANGED:
            self._state = ObjectState.CHANGING if value else self._state
        else:  # implies default state is IDLE
            self._state = ObjectState.CREATING if value else self._state
        # cascade Select downwards for Children
        if value:
            for c in self.children:
                c.child.select(True)
        else:
            for c in self.children:
                c.child.force_idle()

    def __str__(self) -> str:
        """Return a string representation."""
        return f"{self.kml_type}"

    def __repr__(self) -> str:
        """Return a debug representation."""
        return self.__str__()


ObjectChild = NamedTuple("ObjectChild", [("parent", Object), ("child", Object)])
"""Named tuple that describes a parent:child relationship between two :class:`~pyLiveKML.KML.KMLObjects.Object` instances.
"""
