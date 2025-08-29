"""Feature module.

:note: Includes the `Container` class definition as well, to avoid a circular import.
"""

from abc import ABC
from typing import Iterable, NamedTuple, Iterator, cast

from lxml import etree  # type: ignore

from pyLiveKML.KML import KML_UPDATE_CONTAINER_LIMIT_DEFAULT, ObjectState
from pyLiveKML.KML._BaseObject import (
    _FieldDef,
    DumpDirect,
    NoParse,
    NoDump,
)
from pyLiveKML.KML.KMLObjects.AbstractView import AbstractView
from pyLiveKML.KML.KMLObjects.Object import Object, ObjectChild
from pyLiveKML.KML.KMLObjects.Region import Region
from pyLiveKML.KML.KMLObjects.StyleSelector import StyleSelector
from pyLiveKML.KML.KMLObjects.TimePrimitive import TimePrimitive
from pyLiveKML.KML.errors.errors import FeatureInaccessibleError


class Feature(Object, ABC):
    """A KML 'Feature', per https://developers.google.com/kml/documentation/kmlreference#feature.

    :note: While Features are explicitly abstract in the KML specification,
    :class:`~pyLiveKML.KML.KMLObjects.Feature` is the base class for KML
    :class:`~pyLiveKML.KML.KMLObjects.Object` instances that have an "existence" in
    GEP, i.e. that are (potentially) user-editable because they appear in the GEP user
    List View.

    :param str|None name: The (optional) name for this :class:`~pyLiveKML.KML.KMLObjects.Feature` that will be
        displayed in GEP.
    :param str|None description: The (optional) description for this :class:`~pyLiveKML.KML.KMLObjects.Feature`
        that will be displayed in GEP as a text balloon if the :class:`~pyLiveKML.KML.KMLObjects.Feature` is clicked.
    :param bool|None visibility: The (optional) initial visibility for this
        :class:`~pyLiveKML.KML.KMLObjects.Feature` in GEP.
    :param Feature|None container: The (optional) :class:`~pyLiveKML.KML.KMLObjects.Feature` (generally, a
        :class:`~pyLiveKML.KML.KMLObjects.Container`) that encloses this
        :class:`~pyLiveKML.KML.KMLObjects.Feature`.
    :param str|None style_url: An (optional) style URL, typically a reference to a global
        :class:`~pyLiveKML.KML.KMLObjects.StyleSelector` in a :class:`~pyLiveKML.KML.KMLObjects.Container` that
        encloses this :class:`~pyLiveKML.KML.KMLObjects.Feature`.
    :param Iterable[StyleSelector]|None styles: An iterable of :class:`~pyLiveKML.KML.KMLObjects.StyleSelector`
        objects that are local to this :class:`~pyLiveKML.KML.KMLObjects.Feature`.
    """

    _kml_fields = Object._kml_fields + (
        _FieldDef("name", NoParse, "name", DumpDirect),
        _FieldDef("visibility", NoParse, "visibility", DumpDirect),
        _FieldDef("is_open", NoParse, "open", DumpDirect),
        _FieldDef("author_name", NoParse, "", NoDump),
        _FieldDef("author_link", NoParse, "", NoDump),
        _FieldDef("address", NoParse, "address", DumpDirect),
        _FieldDef("snippet", NoParse, "", NoDump),
        _FieldDef("snippet_max_line", NoParse, "", NoDump),
        _FieldDef("phone_number", NoParse, "phoneNumber", DumpDirect),
        _FieldDef("description", NoParse, "description", DumpDirect),
        _FieldDef("style_url", NoParse, "styleUrl", DumpDirect),
    )
    _direct_children = Object._direct_children + (
        "abstract_view",
        "time_primitive",
        "region",
        "_styles",
    )

    def __init__(
        self,
        container: "Feature|None" = None,
        name: str | None = None,
        visibility: bool | None = None,
        is_open: bool | None = None,
        author_name: str | None = None,
        author_link: str | None = None,
        address: str | None = None,
        phone_number: str | None = None,
        snippet: str | None = None,
        snippet_max_lines: int | None = None,
        description: str | None = None,
        abstract_view: AbstractView | None = None,
        time_primitive: TimePrimitive | None = None,
        style_url: str | None = None,
        styles: Iterable[StyleSelector] | None = None,
        region: Region | None = None,
    ):
        """Feature instance constructor."""
        Object.__init__(self)
        ABC.__init__(self)
        self._container = container
        self.name = name
        self.visibility = visibility
        self.is_open = is_open
        self.author_name = author_name
        self.author_link = author_link
        self.address = address
        self.phone_number = phone_number
        self.snippet = snippet
        self.snippet_max_lines = snippet_max_lines
        self.description = description
        self._abstract_view = abstract_view
        self._time_primitive = time_primitive
        self.style_url = style_url
        self._styles = list[StyleSelector]()
        if styles:
            self._styles.extend(styles)
        self._region = region

    @property
    def container(self) -> "Container|None":
        """The parent of this instance.

        The :class:`~pyLiveKML.KML.KMLObjects.Container` that immediately encloses this
        :class:`~pyLiveKML.KML.KMLObjects.Feature` in an ownership tree.

        :warning: The :attr:`container` property cannot be altered if the
            :class:`~pyLiveKML.KML.KMLObjects.Feature` is visible in GEP. Doing so would
            break GEP synchronization. Failure to observe this constraint will cause a
            :class:`FeatureInaccessibleError` to be raised.
        """
        return cast(Container, self._container)

    @container.setter
    def container(self, value: "Container") -> None:
        if self._state == ObjectState.IDLE or self._state == ObjectState.CREATING:
            self._container = value
        else:
            raise FeatureInaccessibleError(
                "If a Feature is visible in GEP, you cannot change its' 'container' property."
            )

    @property
    def abstract_view(self) -> AbstractView | None:
        """The AbstractView associated with this Feature."""
        return self._abstract_view

    @abstract_view.setter
    def abstract_view(self, value: AbstractView | None) -> None:
        if self._abstract_view != value:
            self._abstract_view = value
            self.field_changed()

    @property
    def time_primitive(self) -> TimePrimitive | None:
        """The TimePrimitive associated with this Feature."""
        return self._time_primitive

    @time_primitive.setter
    def time_primitive(self, value: TimePrimitive | None) -> None:
        if self._time_primitive != value:
            self._time_primitive = value
            self.field_changed()

    @property
    def region(self) -> Region | None:
        """The active region for viewing this Feature."""
        return self._region

    @region.setter
    def region(self, value: Region | None) -> None:
        if self._region != value:
            self._region = value
            self.field_changed()

    @property
    def styles(self) -> Iterator[StyleSelector]:
        """The Style objects that are direct children of this instance.

        A generator to retrieve references to any :class:`~pyLiveKML.KML.KMLObjects.Style` or
        :class:`~pyLiveKML.KML.KMLObjects.StyleMap` objects that are children of this
        :class:`~pyLiveKML.KML.KMLObjects.Feature`.

        :returns: A generator of :class:`~pyLiveKML.KML.KMLObjects.StyleSelector` objects.
        """
        for s in self._styles:
            yield s

    @property
    def children(self) -> Iterator[ObjectChild]:
        """The children of this instance.

        Overridden from :attr:`pyLiveKML.KML.KMLObjects.Object.Object.children` to yield the children of a
        :class:`~pyLiveKML.KML.KMLObjects.Feature`, i.e. one or more :class:`~pyLiveKML.KML.KMLObjects.StyleSelector`
        instances, and their children.
        """
        if self.abstract_view is not None:
            yield ObjectChild(parent=self, child=self.abstract_view)
        if self.time_primitive is not None:
            yield ObjectChild(parent=self, child=self.time_primitive)
        if self.region is not None:
            yield ObjectChild(parent=self, child=self.region)
        for s in self._styles:
            yield ObjectChild(parent=self, child=s)
            yield from s.children

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        if self.author_name is not None:
            author = etree.SubElement(root, "atom:author")
            etree.SubElement(author, "atom:name").text = self.author_name
        if self.author_link is not None:
            etree.SubElement(root, "atom:link", attribs={"href": self.author_link})
        if self.snippet is not None:
            attribs = {}
            if self.snippet_max_lines is not None:
                attribs["maxLines"] = str(self.snippet_max_lines)
            etree.SubElement(root, "Snippet", attribs).text = self.snippet

        # if with_children:
        #     if self.abstract_view is not None:
        #         root.append(self.abstract_view.construct_kml())
        #     if self.time_primitive is not None:
        #         root.append(self.time_primitive.construct_kml())
        #     if self.region is not None:
        #         root.append(self.region.construct_kml())
        #     for s in self.styles:
        #         root.append(s.construct_kml())

    # override Object.select() to enable upwards cascade, i.e. if a Feature contained
    # in an unselected parent Feature is selected, the parent Feature must also be
    # selected in order for GEP synchronization to work correctly.
    def select(self, value: bool, cascade: bool = False) -> None:
        """Cascade select upwards, but do not cascade deselect upwards.

        Overrides :func:`~pyLiveKML.KML.KMLObjects.Object.Object.select` to implement upwards cascade of selection.
        That is, if a :class:`~pyLiveKML.KML.KMLObjects.Feature` enclosed in the object tree depending from an
        unselected  parent :class:`~pyLiveKML.KML.KMLObjects.Feature` is selected, the reverse tree's parents must also
        be selected in order for GEP synchronization to work correctly.
        """
        Object.select(self, value, cascade)
        # Cascade Select *upwards* for Features, but *do not* cascade Deselect upwards
        if value and self._container:
            self._container.select(True, False)

    def __str__(self) -> str:
        """Return a string representation."""
        return f"{self.kml_type}:{self.name}"

    def __repr__(self) -> str:
        """Return a debug representation."""
        return self.__str__()


class Container(list[Feature], Feature, ABC):
    """A KML 'Container', per https://developers.google.com/kml/documentation/kmlreference#container.

    :note: While Containers are explicitly abstract,
    :class:`~pyLiveKML.KML.KMLObjects.Container` is the base class for KML
    :class:`~pyLiveKML.KML.KMLObjects.Folder` and
    :class:`~pyLiveKML.KML.KMLObjects.Document` that have an "existence" in GEP, i.e.
    that are (potentially) user-editable because they appear in the GEP user List View,
    and that may 'contain' other :class:`~pyLiveKML.KML.KMLObjects.Feature` objects,
    including other concrete :class:`~pyLiveKML.KML.KMLObjects.Container` objects.

    :param str|None name: The (optional) name for this :class:`~pyLiveKML.KML.KMLObjects.Container` that will
        be displayed in GEP.
    :param bool|None visibility: The (optional) initial visibility for this
        :class:`~pyLiveKML.KML.KMLObjects.Container` in GEP.
    :param bool|None is_open: Optional boolean flag to indicate whether the
        :class:`~pyLiveKML.KML.KMLObjects.Container` will be displayed as 'open' in the GEP user List View.
    :param int|None update_limit: Only applies to the root of a :class:`~pyLiveKML.KML.KMLObjects.Feature` tree.
        The (approximate) maximum number of contained :class:`~pyLiveKML.KML.KMLObjects.Feature` instances that will be
        synchronized from this :class:`~pyLiveKML.KML.KMLObjects.Container` during any one synchronization update.
    :param str|None style_url: An (optional) style URL, generally a reference to a global
        :class:`~pyLiveKML.KML.KMLObjects.StyleSelector` in a parent of this
        :class:`~pyLiveKML.KML.KMLObjects.Container`.
    :param Iterable[StyleSelector]|None styles: An (optional) Iterable of
        :class:`~pyLiveKML.KML.KMLObjects.StyleSelector` objects that will be local to this
        :class:`~pyLiveKML.KML.KMLObjects.Container`.
    :param Iterable[Feature]|None features: An (optional) Iterable of :class:`~pyLiveKML.KML.KMLObjects.Feature`
        objects to be enclosed by this :class:`~pyLiveKML.KML.KMLObjects.Container`.
    """

    def __init__(
        self,
        name: str | None = None,
        visibility: bool | None = None,
        is_open: bool | None = None,
        author_name: str | None = None,
        author_link: str | None = None,
        address: str | None = None,
        phone_number: str | None = None,
        snippet: str | None = None,
        snippet_max_lines: int | None = None,
        description: str | None = None,
        abstract_view: AbstractView | None = None,
        time_primitive: TimePrimitive | None = None,
        style_url: str | None = None,
        styles: Iterable[StyleSelector] | None = None,
        region: Region | None = None,
        update_limit: int = KML_UPDATE_CONTAINER_LIMIT_DEFAULT,
        features: Feature | Iterable[Feature] | None = None,
    ):
        """Feature instance constructor."""
        list[Feature].__init__(self)
        Feature.__init__(
            self,
            name=name,
            visibility=visibility,
            is_open=is_open,
            author_name=author_name,
            author_link=author_link,
            address=address,
            phone_number=phone_number,
            snippet=snippet,
            snippet_max_lines=snippet_max_lines,
            description=description,
            abstract_view=abstract_view,
            time_primitive=time_primitive,
            style_url=style_url,
            styles=styles,
            region=region,
        )
        ABC.__init__(self)
        if features is not None:
            if isinstance(features, Feature):
                self.append(features)
            else:
                self.extend(features)
        self._is_open: bool | None = is_open
        self._update_limit: int = 0
        self.update_limit = update_limit
        self.__deleted: list[Feature] = list[Feature]()

    @property
    def containers(self) -> Iterator["ContainedFeature"]:
        """The children of the instance that are themselves Container instances.

        A generator to retrieve references to any :class:`~pyLiveKML.KML.KMLObjects.Container` objects that are
        enclosed by this :class:`~pyLiveKML.KML.KMLObjects.Container` object, and the tree that is rooted at it.

        :returns: A generator of :class:`~pyLiveKML.KML.KMLObjects.Container.ContainedFeature` named tuples that
            describe each enclosed :class:`~pyLiveKML.KML.KMLObjects.Container` as a (container, feature)
        """
        for f in self:
            if isinstance(f, Container):
                yield ContainedFeature(container=self, feature=f)
                yield from f.containers

    @property
    def features(self) -> Iterator["ContainedFeature"]:
        """The children of the instance that are Features, but are not Containers.

        A generator to retrieve references to the :class:`~pyLiveKML.KML.KMLObjects.Feature` objects that are
        enclosed by this :class:`~pyLiveKML.KML.KMLObjects.Container` object, and the tree that is rooted at it. Note
        that :class:`~pyLiveKML.KML.KMLObjects.Container` objects are *not* yielded by this generator, despite being
        specializations of :class:`~pyLiveKML.KML.KMLObjects.Feature`; use the :attr:`containers` property to retrieve
        them.

        :returns: A generator of :class:`~pyLiveKML.KML.KMLObjects.Container.ContainedFeature` named tuples that
            describes each enclosed :class:`~pyLiveKML.KML.KMLObjects.Feature` as a (container, feature)
        """
        for f in self:
            if isinstance(f, Container):
                yield from f.features
            elif isinstance(f, Feature):
                yield ContainedFeature(container=self, feature=f)

    @property
    def update_limit(self) -> int:
        """The maximum size of a synchronization update.

        The (approximate) maximum number of KML objects that will be synchronized by any single
        synchronization update that is rooted in this :class:`~pyLiveKML.KML.KMLObjects.Container`.
        """
        return self._update_limit

    @update_limit.setter
    def update_limit(self, value: int) -> None:
        # note that because this is not a KML field, i.e. that is displayed by GEP,
        # there is no need to call self.field_changed() if the value is updated
        if value != self._update_limit and value > 0:
            self._update_limit = value

    @property
    def flush(self) -> Iterator[Feature]:
        """Flush objects flagged as deleted out of the UI.

        A generator to retrieve instances of :class:`~pyLiveKML.KML.KMLObjects.Feature` objects that have been
        deleted from this :class:`~pyLiveKML.KML.KMLObjects.Container` but for which those deletions **have not** yet
        been synchronized with GEP. As the generator retrieves a deleted :class:`~pyLiveKML.KML.KMLObjects.Feature`, it
        also completes the deletion process.

        :returns: A generator of :class:`~pyLiveKML.KML.KMLObjects.Feature` objects.
        """
        while len(self.__deleted) > 0:
            f = self.__deleted[0]
            self.__deleted.remove(f)
            yield f

    def construct_kml(self, with_features: bool = False) -> etree.Element:
        """Construct the KML content for the instance.

        Overridden from :func:`~pyLiveKML.KML.KMLObjects.Object.construct_kml` to allow
        for the creation of contained or enclosed
        :class:`~pyLiveKML.KML.KMLObjects.Feature` instances, including other
        :class:`~pyLiveKML.KML.KMLObjects.Container` instances.
        """
        root = super().construct_kml()
        if with_features:
            for f in self:
                if isinstance(f, Container):
                    root.append(f.construct_kml(with_features=True))
                elif isinstance(f, Feature):
                    root.append(f.construct_kml())
        return root

    def append(self, item: Feature) -> None:
        """Append a :class:`~pyLiveKML.KML.KMLObjects.Feature` to this :class:`~pyLiveKML.KML.KMLObjects.Container`.

        :param Feature item: The :class:`~pyLiveKML.KML.KMLObjects.Feature` to be appended.
        """
        list[Feature].append(self, item)
        item.container = self

    def remove(self, __value: Feature) -> None:
        """Remove a :class:`~pyLiveKML.KML.KMLObjects.Feature` from this :class:`~pyLiveKML.KML.KMLObjects.Container`.

        Of course, the :class:`~pyLiveKML.KML.KMLObjects.Feature` must be enclosed in this
        :class:`~pyLiveKML.KML.KMLObjects.Container` to be able to be removed.

        :param Feature __value: The :class:`~pyLiveKML.KML.KMLObjects.Feature` to be removed.
        """
        if __value.selected:
            self.__deleted.append(__value)
        list[Feature].remove(self, __value)

    def force_idle(self, cascade: bool = False) -> None:
        """Force this instance, and _optionally_ its children, to the IDLE state.

        Overridden from :func:`~pyLiveKML.KML.KMLObjects.Object.Object.force_idle` to enable the entire tree of
        enclosed :class:`~pyLiveKML.KML.KMLObjects.Feature` (and :class:`~pyLiveKML.KML.KMLObjects.Container`)
        instances, and child :class:`~pyLiveKML.KML.KMLObjects.Object` instances, that is rooted in this
        :class:`~pyLiveKML.KML.KMLObjects.Container` to be forced to the IDLE state.
        """
        Object.force_idle(self)
        if cascade:
            self.force_features_idle()

    def force_features_idle(self) -> None:
        """Force this instance, and _all_ of its children, to the IDLE state.

        Force the entire tree of enclosed :class:`~pyLiveKML.KML.KMLObjects.Feature` (and
        :class:`~pyLiveKML.KML.KMLObjects.Container`) instances to be forced to the IDLE state. Typically called as a
        result of the target :class:`~pyLiveKML.KML.KMLObjects.Container` being deleted from GEP.
        """
        for f in self:
            if isinstance(f, Container):
                # note the implication from force_idle() that cascade is _always_ true for force_features_idle
                f.force_idle(True)
            elif isinstance(f, Feature):
                f.force_idle()

    def select(self, value: bool, cascade: bool = False) -> None:
        """Cascade select upwards, but do not cascade deselect upwards.

        Overrides :func:`~pyLiveKML.KML.KMLObjects.Feature.Feature.select` to implement select/deselect cascade to
        enclosed :class:`~pyLiveKML.KML.KMLObjects.Feature` objects, and to ensure that if a
        :class:`~pyLiveKML.KML.KMLObjects.Container` is deleted from GEP, its' enclosed
        :class:`~pyLiveKML.KML.KMLObjects.Feature` objects are forced IDLE to maintain synchronization.
        """
        Feature.select(self, value, cascade)
        if cascade:
            for f in self:
                f.select(value, True)
        if (
            self._state == ObjectState.DELETE_CREATED
            or self._state == ObjectState.DELETE_CHANGED
        ):
            self.__deleted.clear()
            self.force_features_idle()

    def __str__(self) -> str:
        """Return a string representation."""
        return Feature.__str__(self)

    def __repr__(self) -> str:
        """Return a debug representation."""
        return Feature.__repr__(self)


ContainedFeature = NamedTuple(
    "ContainedFeature", [("container", Container), ("feature", Feature)]
)
"""Named tuple that describes a container:contained relationship.

The container is a :class:`~pyLiveKML.KML.KMLObjects.Container` 
instance and the contained is a :class:`~pyLiveKML.KML.KMLObjects.Feature` 
instance.
"""
