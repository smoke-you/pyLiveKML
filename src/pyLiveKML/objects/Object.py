"""Object module."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Generic, Iterable, Iterator, NamedTuple, Type, TypeVar, cast
from uuid import uuid4, UUID

from lxml import etree  # type: ignore

from pyLiveKML.types.GeoColor import GeoColor
from pyLiveKML.utils import with_ns


class _KMLDump(ABC):
    """Abstract base for various "Dump" implementations.

    "Dump" classes are used to convert a Python object into something suitable for
    publishing as a KML tag value.

    """

    @classmethod
    @abstractmethod
    def dump(cls, value: Any) -> Any:
        raise NotImplementedError


class NoDump(_KMLDump):
    """Dump nothing, i.e. an empty string."""

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
    """Abstract base for various "Parser" implementations.

    "Parser" classes are used to constrain or otherwise manipulate a parameter passed to
    a `_BaseObject`.

    """

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
    """A value in the range -90 to +90.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#kml-fields

    """

    @classmethod
    def parse(cls, value: Any) -> Any:
        """Transform the argument."""
        value = float(value)
        return 90 if value > 90 else -90 if value < -90 else value


class AnglePos90(_KMLParser):
    """A value in the range 0 to +90.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#kml-fields

    """

    @classmethod
    def parse(cls, value: Any) -> Any:
        """Transform the argument."""
        value = float(value)
        return 90 if value > 90 else 0 if value < 0 else value


class Angle180(_KMLParser):
    """A value in the range -180 to +180.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#kml-fields

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
    """A value in the range 0 to +180.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#kml-fields

    """

    @classmethod
    def parse(cls, value: Any) -> Any:
        """Transform the argument."""
        value = float(value)
        return 180 if value > 180 else 0 if value < 0 else value


class Angle360(_KMLParser):
    """A value in the range -360 to +360.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#kml-fields

    """

    @classmethod
    def parse(cls, value: Any) -> Any:
        """Transform the argument."""
        value = float(value)
        return (
            value % 360 if value > 360 else -(-value % 360) if value < -360 else value
        )


class ColorParse(_KMLParser):
    """Ensures that the output is a `GeoColor`, or `None`.

    Primarily intended to convert an `int` to a `GeoColor`.

    """

    @classmethod
    def parse(cls, value: Any) -> Any:
        """Transform the argument."""
        if isinstance(value, int):
            return GeoColor(value)
        return value


class _FieldDef:
    """Describes how a field of a KML object is to be published.

    KML object class definitions (may) specify a tuple of `_FieldDef` instances as the
    `_kml_fields` class variable.

    Parameters
    ----------
    name : str
        The name of the field, from the perspective of the Python object.
    tag : str | None, default = None
        The text that will be assigned to the KML tag for the field when it is published.
        May include a prefixed and colon-separated namespace, e.g. "gx:option" is valid.
    parser : Type[_KMLParser], default = NoParse
        The parser class that will be used to transform any value assigned to the field.
        This allows e.g. floats to be constrained to an appropriate range.
    dumper : Type[_KMLDump], default = DumpDirect
        The dumper class that will be used to convert and publish the field's value to
        KML.

    Attributes
    ----------
    Same as parameters.

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
    """Describes how a child of a KML object is to be published.

    KML object class definitions (may) specify a tuple of `_ChildDef` instances as the
    `_kml_children` class variable.

    Parameters
    ----------
    name : str
        The name of the field, from the perspective of the Python object.

    Attributes
    ----------
    Same as parameters.

    """

    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name


class _DependentDef:
    """Describes how a dependent object of a KML object is to be published.

    KML object class definitions (may) specify a tuple of `_DependentDef` instances as
    the `_kml_dependents` class variable.

    Parameters
    ----------
    name : str
        The name of the field, from the perspective of the Python object.

    Attributes
    ----------
    Same as parameters.

    """

    def __init__(
        self,
        name: str,
    ):
        self.name = name


class ObjectState(Enum):
    """Enumeration of possible states that objects derived from KML :class:`~pyLiveKML.KMLObjects.Object` may hold.

    The `ObjectState` enumeration is specific to the :mod:`pyLiveKML` package, i.e. it is
    *not* part of the KML specification. It is used exclusively for synchronization.

    """

    IDLE = 0
    CREATING = 1
    CREATED = 2
    CHANGING = 3
    DELETE_CREATED = 4
    DELETE_CHANGED = 5


class _BaseObject(ABC):
    """`_BaseObject` is a private class from which almost every KML tag constructor ultimately derives.

    This includes the `Object` class, which is what KML objects are **meant** to derive
    from. The primary difference between `_BaseObject` and `Object` is that `Object` sets
    the `_suppress_id` class variable `True`, while `_BaseObject` sets it `False`. What
    this means in practice is that KML tags that are constructed from `_BaseObject` do
    not include an `id` attribute, so cannot be targeted by e.g. `<Change>` or `<Delete>`
    tags.

    Note that while `_BaseObject` **suppresses** it's `id` when publishing to KML, it still
    **has** an `id` attribute.

    Apart from this, `_BaseObject` and `Object` are conceptually interchangeable.

    """

    _kml_tag: str = ""
    _kml_fields: tuple[_FieldDef, ...] = tuple()
    _kml_children: tuple[_ChildDef, ...] = tuple()
    _kml_dependents: tuple[_DependentDef, ...] = tuple()
    _suppress_id: bool = True

    def __init__(self) -> None:
        """_BaseObject instance constructor."""
        super().__init__()
        self._id = uuid4()
        self._container: _BaseObject | None = None
        self._state: ObjectState = ObjectState.IDLE

    def __setattr__(self, name: str, value: Any) -> None:
        """_BaseObject __setattr__ override method.

        Kicks in when setting an attribute with the same name as an entry in
        `_kml_fields`.

        If a match is made, executes the field's parser to constrain the
        parameter.

        If a matched field changes its value, flags this by calling `field_changed()`.

        """
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
        """_BaseObject __eq__ override method.

        When comparing two _BaseObject instances of the same type, considers them equal
        if all of the attributes listed in `_kml_fields` are of equal value.

        """
        return isinstance(value, self.__class__) and all(
            map(
                lambda x: getattr(self, x.name) == getattr(value, x.name),
                self._kml_fields,
            )
        )

    def __str__(self) -> str:
        """Return the `_BaseObject`'s `_kml_tag` by default."""
        return self._kml_tag

    def __repr__(self) -> str:
        """Return the `_BaseObject`'s string representation by default."""
        return str(self)

    @property
    def id(self) -> UUID:
        """The unique identifier of this `_BaseObject`."""
        return self._id

    @property
    def state(self) -> ObjectState:
        """The current GEP synchronization state of this `_BaseObject`."""
        return self._state

    @property
    def active(self) -> bool:
        """Whether the instance has been selected for display.

        Parameters
        ----------
        value : bool
            If `True`, activates the `_BaseObject`; if `False`, deactivates it.

        Returns
        -------
        bool
            `True` if the `_BaseObject` has been created in the UI and is not scheduled
            for deletion, otherwise `False`.

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
    def fields(self) -> Iterator[tuple[str, Any]]:
        """A generator over the `_BaseObject`'s field names and their values.

        Returns
        -------
        Iterator[tuple[str, Any]]
            In each tuple, the first element is the field name, and the second element is
            the field value.

        """
        for f in self._kml_fields:
            f_obj = getattr(self, f.name, None)
            if f_obj is not None:
                yield ((f.name, f_obj))

    @property
    def children(self) -> Iterator["ObjectChild"]:
        """A generator over the children of the instance.

        In this context, children are child objects that the parent *does not* rely upon.

        Returns
        -------
        Iterator[ObjectChild]
            The children, as `ObjectChild` instances.

        """
        for c in self._kml_children:
            c_obj = getattr(self, c.name, None)
            if c_obj is not None:
                if isinstance(c_obj, Iterable):
                    for cc in c_obj:
                        yield ObjectChild(self, cc)
                else:
                    yield ObjectChild(self, c_obj)

    @property
    def dependents(self) -> Iterator["ObjectChild"]:
        """A generator over the dependents of the instance.

        In this context, dependents are child objects that the parent relies upon, rather
        than contains. For example, the Features stored under a Container are *not*
        dependents of the Container, but they are children.

        Returns
        -------
        Iterator[ObjectChild]
            The dependents, as `ObjectChild` instances.

        """
        for d in self._kml_dependents:
            d_obj = getattr(self, d.name, None)
            if d_obj is not None:
                if isinstance(d_obj, Iterable):
                    for dd in d_obj:
                        yield ObjectChild(self, dd)
                else:
                    yield ObjectChild(self, d_obj)

    @property
    def kml_tag(self) -> str:
        """The class' KML type string.

        Property that specifies the name of the XML tag that forms the root of
        the KML representation of this `_BaseObject`.
        """
        return self._kml_tag

    def build_kml(
        self,
        root: etree.Element,
        with_children: bool = True,
        with_dependents: bool = True,
    ) -> None:
        """Construct the KML content and append it to the provided `etree.Element`.

        Generate the KML representation of the internal fields of this `_BaseObject`, and
        append it to the provided root `etree.Element`.

        Parameters
        ----------
        root : etree.Element
            The `etree.Element` to which the KML published for the object is to be
            appended.
        with_children : bool, default = True
            True if the children of this instance should be included in the build.
        with_dependents : bool, default = True
            True if the dependents of this instance should be included in the build.

        """
        for f in (f for f in self._kml_fields if f.dumper != NoDump):
            value = f.dumper.dump(getattr(self, f.name))
            if value:
                etree.SubElement(root, with_ns(f.typename)).text = value
        if with_dependents:
            for dd in self.dependents:
                branch = dd.child.construct_kml()
                root.append(branch)
        if with_children:
            for dc in self.children:
                branch = dc.child.construct_kml()
                root.append(branch)

    def construct_kml(
        self, with_children: bool = True, with_dependents: bool = True
    ) -> etree.Element:
        """Construct this `_BaseObject`'s KML representation.

        Parameters
        ----------
        root : etree.Element
        with_children : bool, default = True
            True if the children of this instance should be included in the build.
        with_dependents : bool, default = True
            True if the dependents of this instance should be included in the build.

        Returns
        -------
        etree.Element
            The KML representation of the `_BaseObject` as an `etree.Element`.

        """
        attribs = None if self._suppress_id else {"id": str(self.id)}
        root = etree.Element(_tag=with_ns(self.kml_tag), attrib=attribs)
        self.build_kml(root, with_children, with_dependents)
        return root

    def create_kml(self, root: etree.Element, parent: "_BaseObject") -> etree.Element:
        """Construct a complete `<Create>` element tag as a child of an `Update`.

        Parameters
        ----------
        root : etree.Element
            The etree.Element of the `<Update>` tag that will be appended to.
        parent : _BaseObject
            The immediate parent of this `_BaseObject`. Required for GEP synchronization,
            specifically the `targetId` attribute.

        Returns
        -------
        etree.Element
            The newly constructed child tag.

        """
        parent_element = etree.SubElement(
            root, with_ns(parent.kml_tag), attrib={"targetId": str(parent.id)}
        )

        child_attribs = None if self._suppress_id else {"id": str(self.id)}
        child_element = etree.SubElement(
            parent_element, with_ns(self.kml_tag), attrib=child_attribs
        )
        self.build_kml(child_element, False)
        return child_element

    def change_kml(self, root: etree.Element) -> None:
        """Construct a complete `<Change>` element tag as a child of an `Update`.

        Parameters
        ----------
        root : etree.Element
            The etree.Element of the `<Update>` tag that will be appended to.

        """
        item = etree.SubElement(
            root, _tag=with_ns(self.kml_tag), attrib={"targetId": str(self.id)}
        )
        self.build_kml(item, with_children=False, with_dependents=False)

    def delete_kml(self, root: etree.Element) -> None:
        """Construct a complete `<Delete>` element tag as a child of an `Update`.

        Parameters
        ----------
        root : etree.Element
            The etree.Element of the `<Update>` tag that will be appended to.

        """
        etree.SubElement(
            root, _tag=with_ns(self.kml_tag), attrib={"targetId": str(self.id)}
        )

    def activate(self, value: bool, cascade: bool = False) -> None:
        """Activate or deactivate this `_BaseObject` for display in GEP.

        Parameters
        ----------
        value : bool
            `True` to display the `_BaseObject`, `False` to remove it.
        cascade : bool, default = False
            `True` if the activation is to be cascaded to all child objects, `False`
            otherwise.

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
        # cascade Activate downwards for children
        if value:
            for c in self.children:
                c.child.activate(True, cascade)
        else:
            for c in self.dependents:
                c.child.force_idle()
            for c in self.children:
                c.child.force_idle()

    def field_changed(self) -> None:
        """Flag that an attribute of the `_BaseObject` may have changed.

        If this method is called, it indicates that re-synchronization with GEP may be
        required for the `_BaseObject`.

        """
        if self._state == ObjectState.CREATED:
            self._state = ObjectState.CHANGING
        elif self._state == ObjectState.DELETE_CREATED:
            self._state = ObjectState.DELETE_CHANGED
        # if not already CREATED or DELETE_CREATED, change nothing

    def synchronized(self) -> None:
        """Flag that a synchronization update has been emitted for the `_BaseObject`.

        Calling this method modifies the `state` to the next appropriate value.

        """
        if self._state == ObjectState.CREATING:
            self._state = ObjectState.CREATED
        elif self._state == ObjectState.CHANGING:
            self._state = ObjectState.CREATED
        elif (
            self._state == ObjectState.DELETE_CREATED
            or self._state == ObjectState.DELETE_CHANGED
        ):
            self._state = ObjectState.IDLE
        for d in self.dependents:
            d.child.synchronized()

    def force_idle(self) -> None:
        """Force this `_BaseObject` and **all of its children** to the `IDLE` state.

        This is typically done after the object has been deactivated, which will cause
        it to be deleted from GEP at the next synchronization update. When the
        `_BaseObject` is deleted by GEP, all of its children, and any `Feature`s that it
        encloses, will also be automatically deleted. There is no need to emit `<Delete>`
        tags for these deletions, and in fact doing so will likely cause GEP to have
        conniptions.

        """
        self._state = ObjectState.IDLE
        for d in self.dependents:
            d.child.force_idle()
        for c in self.children:
            c.child.force_idle()


class Object(_BaseObject, ABC):
    """A KML `<Object>` tag constructor.

    This is an abstract base class and cannot be used directly in a KML file. It provides
    the `id` attribute, which allows unique identification of a KML element, and the
    `targetId` attribute, which is used to reference objects that have already been
    loaded into Google Earth. The `id` attribute must be assigned if the <Update>
    mechanism is to be used.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#object

    """

    _suppress_id: bool = False
    _kml_children: tuple[_ChildDef, ...] = _BaseObject._kml_children

    def __init__(self) -> None:
        """Object instance constructor."""
        super().__init__()


class ObjectChild:
    """Describes a parent:child relationship between two `_BaseObject` instances.

    Parameters
    ----------
    parent: _BaseObject
    child: _BaseObject

    Attributes
    ----------
    Same as parameters.

    """

    def __init__(
        self,
        parent: _BaseObject,
        child: _BaseObject,
    ) -> None:
        """ObjectChild instance constructor."""
        self.parent = parent
        self.child = child


_LOB = TypeVar("_LOB", bound="_BaseObject")


class _ListObject(_BaseObject, list[_LOB], Generic[_LOB]):
    """Internal class for KML objects that may contain a list of a type of child object.

    The most obvious example is `Container` and it's subclasses `Document` and `Folder`,
    but there are others: `MultiGeometry`, `MultiTrack`, `Schema` and `Tour`.

    The point to this is to allow for detection and handling of changes to the contents
    of these lists.
    """

    def clear(self) -> None:
        """Override superclass `clear()` to call `field_changed()."""
        self.field_changed()
        super().clear()

    def remove(self, value: _LOB) -> None:
        """Override superclass `remove()` to call `field_changed()."""
        self.field_changed()
        super().remove(value)

    def append(self, value: _LOB) -> None:
        """Override superclass `append()` to call `field_changed()."""
        self.field_changed()
        super().append(value)

    def extend(self, iterable: Iterable[_LOB]) -> None:
        """Override superclass `extend()` to call `field_changed()."""
        self.field_changed()
        super().extend(iterable)
