"""Object module."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Generic, Iterable, Iterator, NamedTuple, Type, TypeVar, cast
from uuid import uuid4, UUID

from lxml import etree  # type: ignore

from pyLiveKML.KML.GeoColor import GeoColor
from pyLiveKML.KML.utils import with_ns


class _KMLDump(ABC):

    @classmethod
    @abstractmethod
    def dump(cls, value: Any) -> Any:
        raise NotImplementedError


class NoDump(_KMLDump):
    """Dump nothing."""

    @classmethod
    def dump(cls, value: Any) -> Any:
        """Dump and format a KML object field."""
        return ""


class DumpDirect(_KMLDump):
    """Dump to string."""

    @classmethod
    def dump(cls, value: Any) -> Any:
        """Dump and format a KML object field."""
        if value is None:
            return None
        if isinstance(value, Enum):
            return str(value.value)
        if isinstance(value, bool):
            return str(int(value))
        return str(value)


class _KMLParser(ABC):

    @classmethod
    @abstractmethod
    def parse(cls, value: Any) -> Any:
        raise NotImplementedError


class NoParse(_KMLParser):
    """A value that will not be changed."""

    @classmethod
    def parse(cls, value: Any) -> Any:
        """Transform the argument."""
        return value


class Angle90(_KMLParser):
    """A value ≥−90 and ≤90.

    See https://developers.google.com/kml/documentation/kmlreference#kml-fields
    """

    @classmethod
    def parse(cls, value: Any) -> Any:
        """Transform the argument."""
        value = float(value)
        return 90 if value > 90 else -90 if value < -90 else value


class AnglePos90(_KMLParser):
    """A value ≥0 and ≤90.

    See https://developers.google.com/kml/documentation/kmlreference#kml-fields
    """

    @classmethod
    def parse(cls, value: Any) -> Any:
        """Transform the argument."""
        value = float(value)
        return 90 if value > 90 else 0 if value < 0 else value


class Angle180(_KMLParser):
    """A value ≥−180 and ≤180.

    See https://developers.google.com/kml/documentation/kmlreference#kml-fields
    """

    @classmethod
    def parse(cls, value: Any) -> Any:
        """Transform the argument."""
        value = float(value)
        while value > 180:
            value = value - 360
        while value < -180:
            value = value + 360
        return value


class AnglePos180(_KMLParser):
    """A value ≥0 and ≤180.

    See https://developers.google.com/kml/documentation/kmlreference#kml-fields
    """

    @classmethod
    def parse(cls, value: Any) -> Any:
        """Transform the argument."""
        value = float(value)
        return 180 if value > 180 else 0 if value < 0 else value


class Angle360(_KMLParser):
    """A value ≥−360 and ≤360.

    See https://developers.google.com/kml/documentation/kmlreference#kml-fields
    """

    @classmethod
    def parse(cls, value: Any) -> Any:
        """Transform the argument."""
        value = float(value)
        return (
            value % 360 if value > 360 else -(-value % 360) if value < -360 else value
        )


class ColorParse(_KMLParser):
    """A color, typically as a 32-bit ABGR value."""

    @classmethod
    def parse(cls, value: Any) -> Any:
        """Transform the argument."""
        if isinstance(value, int):
            return GeoColor(value)
        return value


class _FieldDef:
    """Describes how a field of a KML object is to be published.

    KML object class definitions specify a tuple of _FieldDef instances as the `_kml_fields`
    class variable.

    :param str name: The name of the field, from the perspective of the Python object.
    :param Type[_KMLParser] parser: The parser class that will be used to transform any value
        assigned to the field. This allows e.g. floats to be constrained to an appropriate
        range.
    :param str tag: The text that will be assigned to the KML tag for the field when it
        is published. May include a prefixed and colon-separated namespace, e.g. "gx:option"
        is valid.
    :param Type[_KMLDump] dumper: The dumper class that will be used to convert and publish
        the field's value to KML.
    """

    def __init__(
        self,
        name: str,
        tag: str | None = None,
        parser: Type[_KMLParser] = NoParse,
        dumper: Type[_KMLDump] = DumpDirect,
    ):
        """_FieldDef instance constructor."""
        self.name = name
        self.typename = tag if tag is not None else name
        self.parser = parser
        self.dumper = dumper


class _ChildDef:

    def __init__(
        self,
        name: str,
        tag: str | None = None,
        use_tag: bool = True,
    ) -> None:
        self.name = name
        self.tag = name if tag is None else tag
        self.use_tag = use_tag


class ObjectState(Enum):
    """Enumeration of possible states that objects derived from KML :class:`~pyLiveKML.KMLObjects.Object` may hold.

    The 'State' enumeration is specific to the :mod:`pyLiveKML` package, i.e. it is *not* part of the KML specification.
    """

    IDLE = 0
    CREATING = 1
    CREATED = 2
    CHANGING = 3
    DELETE_CREATED = 4
    DELETE_CHANGED = 5


class _BaseObject(ABC):

    _kml_tag: str = ""
    _kml_fields: tuple[_FieldDef, ...] = tuple()
    _direct_children: tuple[_ChildDef, ...] = tuple()
    _suppress_id: bool = True

    def __init__(self) -> None:
        """Object instance constructor."""
        super().__init__()
        self._id = uuid4()
        self._selected: bool = False
        self._container: _BaseObject | None = None
        self._state: ObjectState = ObjectState.IDLE

    def __setattr__(self, name: str, value: Any) -> None:
        """Object setattr method."""
        match = next(filter(lambda x: x.name == name, self._kml_fields), None)
        changed = False
        if match is not None:
            value = match.parser.parse(value)
            if value != getattr(self, name, None):
                changed = True
        super().__setattr__(name, value)
        if changed:
            self.field_changed()

    def __eq__(self, value: object) -> bool:
        """Object eq method."""
        return isinstance(value, self.__class__) and all(
            map(
                lambda x: getattr(self, x.name) == getattr(value, x.name),
                self._kml_fields,
            )
        )

    @property
    def id(self) -> UUID:
        """The unique identifier of this :class:`~pyLiveKML.KMLObjects.Object`."""
        return self._id

    @property
    def state(self) -> ObjectState:
        """The current GEP synchronization state of this :class:`~pyLiveKML.KMLObjects.Object`."""
        return self._state

    @property
    def active(self) -> bool:
        """Flag to indicate whether the instance has been selected for display.

        True if this :class:`~pyLiveKML.KMLObjects.Object` has been created in the
        UI and is not scheduled for deletion, otherwise False.
        """
        return (
            ObjectState.CREATING,
            ObjectState.CREATED,
            ObjectState.CHANGING,
        ).__contains__(self._state)

    @active.setter
    def active(self, value: bool) -> None:
        self.activate(value)

    @property
    def children(self) -> Iterator["ObjectChild"]:
        """The children of the instance.

        A generator to retrieve the children of this :class:`~pyLiveKML.KMLObjects.Object` as
        :class:`~pyLiveKML.KMLObjects.Object.ObjectChild` instances.

        :returns: A generator of :class:`~pyLiveKML.KMLObjects.Object.ObjectChild` named tuples that describes
            each child :class:`~pyLiveKML.KMLObjects.Object` as a (parent, child)
        """
        # The return; yield pattern is used to trick linters into accepting that this is a generator that yields
        # nothing, as opposed to yielding None
        for c in self._direct_children:
            c_obj = getattr(self, c.name, None)
            if c_obj:
                if isinstance(c_obj, Iterable):
                    for cc in c_obj:
                        yield ObjectChild(self, cc)
                else:
                    yield ObjectChild(self, c_obj)

    @property
    def direct_children(self) -> Iterator["_BaseObject"]:
        """Retrieve a generator over the direct children of the object.

        That is, retrieve any `Object` instances that are embedded in this `Object`.
        """
        for dc in self._direct_children:
            dcobj = getattr(self, dc.name, None)
            if dcobj:
                if isinstance(dcobj, _BaseObject):
                    if isinstance(dcobj, _ListObject):
                        yield cast(_BaseObject, dcobj)
                    elif isinstance(dcobj, Iterable):
                        yield from dcobj
                    else:
                        yield dcobj
                elif isinstance(dcobj, Iterable):
                    for elem in dcobj:
                        if isinstance(elem, _BaseObject):
                            yield elem
        if isinstance(self, _ListObject):
            for c in cast(list[_BaseObject], self):
                yield c

    @property
    def kml_tag(self) -> str:
        """The class' KML type string.

        Property that specifies the name of the XML tag that forms the root of
        the KML representation of this :class:`~pyLiveKML.KMLObjects.Object`.
        """
        return self._kml_tag

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element.

        Generate the KML representation of the internal fields of this
        :class:`~pyLiveKML.KMLObjects.Object`, and append it to the provided root
        etree.Element.

        :param etree.Element root: The root XML element that will be appended to.
        :param bool with_children: True if the children of this instance should be
            included in the build.
        """
        for f in (f for f in self._kml_fields if f.dumper != NoDump):
            value = f.dumper.dump(getattr(self, f.name))
            if value:
                etree.SubElement(root, with_ns(f.typename)).text = value
        if with_children:
            for dc in self.direct_children:
                branch = dc.construct_kml()
                root.append(branch)


    def construct_kml(self) -> etree.Element:
        """Construct this :class:`~pyLiveKML.KMLObjects.Object`'s KML representation.

        :returns: The KML representation of the object as an etree.Element.
        """
        attribs = None if self._suppress_id else {"id": str(self.id)}
        root = etree.Element(_tag=with_ns(self.kml_tag), attrib=attribs)
        self.build_kml(root)
        return root

    def update_kml(self, parent: "_BaseObject", update: etree.Element) -> None:
        """Update this :class:`~pyLiveKML.KMLObjects.Object`'s KML representation.

        Retrieve a complete child <Create>, <Change> or <Delete> KML tag as a child of an <Update> tag.
        The type of child tag retrieved is dependent on the current state of this
        :class:`~pyLiveKML.KMLObjects.Object`.

        :param Object parent: The immediate parent :class:`~pyLiveKML.KMLObjects.Object` of this
            :class:`~pyLiveKML.KMLObjects.Object`. The parent is required only for <Create> tags.
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

    def create_kml(self, root: etree.Element, parent: "_BaseObject") -> etree.Element:
        """Construct a complete <Create> element tree as a child of an <Update> tag.

        :param Object parent: The immediate parent :class:`~pyLiveKML.KMLObjects.Object` of this
            :class:`~pyLiveKML.KMLObjects.Object`. The parent must be specified for GEP synchronization.
        :param etree.Element update: The etree.Element of the <Update> tag that will be appended to.
        """
        parent_element = etree.Element(with_ns(parent.kml_tag), attrib={"targetId": str(parent.id)})
        item = self.construct_kml()
        parent_element.append(item)
        root.append(parent_element)
        return item

    def change_kml(self, root: etree.Element) -> None:
        """Construct a complete <Change> element tree as a child of an <Update> tag.

        :param etree.Element update: The etree.Element of the <Update> tag that will be appended to.
        """
        p_id = getattr(self, "id", None)
        attribs = None
        if p_id is not None:
            attribs = {"id": str(p_id)}
        item = etree.SubElement(root, _tag=with_ns(self.kml_tag), attrib=attribs)
        self.build_kml(item, with_children=False)

    def delete_kml(self, root: etree.Element) -> None:
        """Construct a complete <Delete> element tree as a child of an <Update> tag.

        :param etree.Element update: The etree.Element of the <Update> tag that will be appended to.
        """
        etree.SubElement(root, _tag=with_ns(self.kml_tag), attrib={"targetId": str(self.id)})

    def force_idle(self) -> None:
        """Force this :class:`~pyLiveKML.KMLObjects.Object` and **all of its children** to the IDLE state.

        This is typically done after the object has been deselected, which will cause
        it to be deleted from GEP at the next synchronization update. When the
        :class:`~pyLiveKML.KMLObjects.Object` is deleted by GEP, all of its
        children, and any :class:`~pyLiveKML.KMLObjects.Feature` objects that it
        encloses, will also be automatically deleted. There is no need to emit <Delete>
        tags for these deletions, and in fact doing so will likely cause GEP to have
        conniptions.
        """
        self._state = ObjectState.IDLE
        for c in self.children:
            c.child.force_idle()

    def field_changed(self) -> None:
        """Flag that a field or property of this :class:`~pyLiveKML.KMLObjects.Object` has changed.

        If this flag is set, it indicates that re-synchronization with GEP may be required.
        """
        if self._state == ObjectState.CREATED:  # or self._state == State.IDLE:
            self._state = ObjectState.CHANGING
        elif self._state == ObjectState.DELETE_CREATED:
            self._state = ObjectState.DELETE_CHANGED
        elif self._state == ObjectState.IDLE:
            pass

    def update_generated(self) -> None:
        """Modify the state of the :class:`~pyLiveKML.KMLObjects.Object` to reflect that a synchronization update has been emitted."""
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

    def activate(self, value: bool, cascade: bool = False) -> None:
        """Activate or deactivate this :class:`~pyLiveKML.KMLObjects.Object` for display in GEP.

        :param bool value: True for activation, False for deactivation
        :param bool cascade: True if the activation is to be cascaded to all child Objects.
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
        # cascade Activate downwards for Children
        if value:
            for c in self.children:
                c.child.activate(True)
        else:
            for c in self.children:
                c.child.force_idle()


class Object(_BaseObject, ABC):
    """A KML 'Object', per https://developers.google.com/kml/documentation/kmlreference#object.

    Note that the :class:`~pyLiveKML.KMLObjects.Object` class is explicitly abstract,
    and is the base class from which most other KML elements (anything with an :attr:`id`
    property) derive.
    """

    _suppress_id: bool = False

    def __init__(self) -> None:
        """Object instance constructor."""
        super().__init__()


ObjectChild = NamedTuple(
    "ObjectChild", [("parent", _BaseObject), ("child", _BaseObject)]
)
"""Named tuple that describes a parent:child relationship between two :class:`~pyLiveKML.KMLObjects.Object` instances.
"""


_LOB = TypeVar("_LOB", bound="_BaseObject")


class _ListObject(_BaseObject, list[_LOB], Generic[_LOB]):
    """Internal class for KML objects that may contain a list of a type of child object.

    The most obvious example is `Container` and it's subclasses `Document` and `Folder`,
    but there are others: `MultiGeometry`, `MultiTrack`, `Schema` and `Tour`.

    The point to this is to allow for detection and handling of changes to the contents
    of these lists.
    """

    def clear(self) -> None:
        self.field_changed()
        super().clear()

    def remove(self, value: _LOB) -> None:
        self.field_changed()
        super().remove(value)

    def append(self, value: _LOB) -> None:
        self.field_changed()
        super().append(value)

    def extend(self, iterable: Iterable[_LOB]) -> None:
        self.field_changed()
        super().extend(iterable)
