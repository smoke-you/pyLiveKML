from abc import ABC
from typing import Iterable, NamedTuple, Iterator, cast

from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import KML_UPDATE_CONTAINER_LIMIT_DEFAULT, ObjectState
from pyLiveKML.KML.KMLObjects.Object import Object, ObjectChild
from pyLiveKML.KML.KMLObjects.StyleSelector import StyleSelector
from pyLiveKML.KML.errors.errors import FeatureInaccessibleError


class Feature(Object, ABC):
    """A KML 'Feature', per https://developers.google.com/kml/documentation/kmlreference#feature. Note that while
    Features are explicitly abstract in the KML specification, :class:`~pyLiveKML.KML.KMLObjects.Feature` is the base
    class for KML :class:`~pyLiveKML.KML.KMLObjects.Object` instances that have an "existence" in GEP, i.e. that are
    (potentially) user-editable because they appear in the GEP user List View.

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

    def __init__(
        self,
        name: str | None = None,
        description: str | None = None,
        visibility: bool | None = None,
        container: "Feature|None" = None,
        style_url: str | None = None,
        styles: Iterable[StyleSelector] | None = None,
    ):
        Object.__init__(self)
        ABC.__init__(self)
        self._container = container
        self._name = name
        self._visibility = visibility
        self._description = description
        self._style_url = style_url
        self._styles = list[StyleSelector]()
        if styles:
            self._styles.extend(styles)

    @property
    def container(self) -> "Container|None":
        """The :class:`~pyLiveKML.KML.KMLObjects.Container` that immediately encloses this
        :class:`~pyLiveKML.KML.KMLObjects.Feature` in an ownership tree.

        :warning: The :attr:`container` property cannot be altered if the :class:`~pyLiveKML.KML.KMLObjects.Feature` is
            visible in GEP. Doing so would break GEP synchronization. Failure to observe this constraint will cause a
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
    def name(self) -> str | None:
        """The text that will be displayed as the name of the :class:`~pyLiveKML.KML.KMLObjects.Feature` in GEP."""
        return self._name

    @name.setter
    def name(self, value: str | None) -> None:
        if self._name != value:
            self._name = value
            self.field_changed()

    @property
    def visibility(self) -> bool | None:
        """True if the :class:`~pyLiveKML.KML.KMLObjects.Feature` will (initially) be checked (visible) in GEP, False
        otherwise.
        """
        return self._visibility

    @visibility.setter
    def visibility(self, value: bool | None) -> None:
        if self._visibility != value:
            self._visibility = value
            self.field_changed()

    @property
    def description(self) -> str | None:
        """The text description for this :class:`~pyLiveKML.KML.KMLObjects.Feature`, that will be displayed in a
        balloon in GEP if the :class:`~pyLiveKML.KML.KMLObjects.Feature` is clicked.

        :note: HTML and (some) JavaScript are permissible (in GEP > 5.0) for the :attr:`description` property. Refer to
            the KML specification at https://developers.google.com/kml/documentation/kmlreference for details.
        """
        return self._description

    @description.setter
    def description(self, value: str | None) -> None:
        if self._description != value:
            self._description = value
            self.field_changed()

    @property
    def styles(self) -> Iterator[StyleSelector]:
        """A generator to retrieve references to any :class:`~pyLiveKML.KML.KMLObjects.Style` or
        :class:`~pyLiveKML.KML.KMLObjects.StyleMap` objects that are children of this
        :class:`~pyLiveKML.KML.KMLObjects.Feature`.

        :returns: A generator of :class:`~pyLiveKML.KML.KMLObjects.StyleSelector` objects.
        """
        for s in self._styles:
            yield s

    # override Object.select() to enable upwards cascade, i.e. if a Feature contained in an unselected parent Feature
    # is selected, the parent Feature must also be selected in order for GEP synchronization to work correctly.
    def select(self, value: bool, cascade: bool = False) -> None:
        """Overrides :func:`~pyLiveKML.KML.KMLObjects.Object.Object.select` to implement upwards cascade of selection.
        That is, if a :class:`~pyLiveKML.KML.KMLObjects.Feature` enclosed in the object tree depending from an
        unselected  parent :class:`~pyLiveKML.KML.KMLObjects.Feature` is selected, the reverse tree's parents must also
        be selected in order for GEP synchronization to work correctly.
        """
        Object.select(self, value, cascade)
        # Cascade Select *upwards* for Features, but *do not* cascade Deselect upwards
        if value and self._container:
            self._container.select(True, False)

    def __str__(self) -> str:
        return f"{self.kml_type}:{self.name}"

    def __repr__(self) -> str:
        return self.__str__()


class Container(list[Feature], Feature, ABC):
    """A KML 'Container', per https://developers.google.com/kml/documentation/kmlreference#container. Note that while
    Containers are explicitly abstract, :class:`~pyLiveKML.KML.KMLObjects.Container` is the base class for KML
    :class:`~pyLiveKML.KML.KMLObjects.Folder` and :class:`~pyLiveKML.KML.KMLObjects.Document` that have an "existence"
    in GEP, i.e. that are (potentially) user-editable because they appear in the GEP user List View, and that may
    'contain' other :class:`~pyLiveKML.KML.KMLObjects.Feature` objects, including other concrete
    :class:`~pyLiveKML.KML.KMLObjects.Container` objects.

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
        update_limit: int = KML_UPDATE_CONTAINER_LIMIT_DEFAULT,
        style_url: str | None = None,
        styles: Iterable[StyleSelector] | None = None,
        features: Iterable[Feature] | None = None,
    ):
        list[Feature].__init__(self)
        Feature.__init__(
            self, name=name, visibility=visibility, style_url=style_url, styles=styles
        )
        ABC.__init__(self)
        if features:
            self.extend(features)
        self._is_open: bool | None = is_open
        self._update_limit: int = 0
        self.update_limit = update_limit
        self.__deleted: list[Feature] = list[Feature]()

    @property
    def containers(self) -> Iterator["ContainedFeature"]:
        """A generator to retrieve references to any :class:`~pyLiveKML.KML.KMLObjects.Container` objects that are
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
        """A generator to retrieve references to the :class:`~pyLiveKML.KML.KMLObjects.Feature` objects that are
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
    def children(self) -> Iterator[ObjectChild]:
        """Overridden from :attr:`pyLiveKML.KML.KMLObjects.Object.Object.children` to yield the children of a
        :class:`~pyLiveKML.KML.KMLObjects.Container`, i.e. one or more :class:`~pyLiveKML.KML.KMLObjects.StyleSelector`
        instances, and their children.
        """
        for s in self._styles:
            yield ObjectChild(parent=self, child=s)
            yield from s.children

    @property
    def is_open(self) -> bool | None:
        """True if the :class:`~pyLiveKML.KML.KMLObjects.Container` will be initially displayed in an 'open' state in
        the GEP user List View, else False if it will be initially displayed in a 'closed' state.  None implies the
        default of False.
        """
        return self._is_open

    @is_open.setter
    def is_open(self, value: bool | None) -> None:
        if self._is_open != value:
            self._is_open = value
            self.field_changed()

    @property
    def update_limit(self) -> int:
        """The (approximate) maximum number of KML objects that will be synchronized by any single
        synchronization update that is rooted in this :class:`~pyLiveKML.KML.KMLObjects.Container`.
        """
        return self._update_limit

    @update_limit.setter
    def update_limit(self, value: int) -> None:
        # note that because this is not a KML field, i.e. that is displayed by GEP, there is no need to call
        # self.field_changed() if the value is updated
        if value != self._update_limit and value > 0:
            self._update_limit = value

    @property
    def flush(self) -> Iterator[Feature]:
        """A generator to retrieve instances of :class:`~pyLiveKML.KML.KMLObjects.Feature` objects that have been
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
        """Overridden from :func:`~pyLiveKML.KML.KMLObjects.Object.construct_kml` to allow for the creation of
        contained or enclosed :class:`~pyLiveKML.KML.KMLObjects.Feature` instances, including other
        :class:`~pyLiveKML.KML.KMLObjects.Container` instances.
        """
        root = Object.construct_kml(self)
        if with_features:
            for f in self:
                if isinstance(f, Container):
                    root.append(f.construct_kml(with_features=True))
                elif isinstance(f, Feature):
                    root.append(f.construct_kml())
        return root

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        if self.name is not None:
            etree.SubElement(root, "name").text = self.name
        if self.visibility is not None:
            etree.SubElement(root, "visibility").text = str(int(self.visibility))
        if self.is_open is not None:
            etree.SubElement(root, "open").text = str(int(self.is_open))
        if self.description is not None:
            etree.SubElement(root, "description").text = self.description
        if with_children:
            for s in self._styles:
                root.append(s.construct_kml())

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
        """Overridden from :func:`~pyLiveKML.KML.KMLObjects.Object.Object.force_idle` to enable the entire tree of
        enclosed :class:`~pyLiveKML.KML.KMLObjects.Feature` (and :class:`~pyLiveKML.KML.KMLObjects.Container`)
        instances, and child :class:`~pyLiveKML.KML.KMLObjects.Object` instances, that is rooted in this
        :class:`~pyLiveKML.KML.KMLObjects.Container` to be forced to the IDLE state.
        """
        Object.force_idle(self)
        if cascade:
            self.force_features_idle()

    def force_features_idle(self) -> None:
        """Force the entire tree of enclosed :class:`~pyLiveKML.KML.KMLObjects.Feature` (and
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
        """Overrides :func:`~pyLiveKML.KML.KMLObjects.Feature.Feature.select` to implement select/deselect cascade to
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
        return Feature.__str__(self)

    def __repr__(self) -> str:
        return Feature.__repr__(self)


ContainedFeature = NamedTuple(
    "ContainedFeature", [("container", Container), ("feature", Feature)]
)
"""Named tuple that describes a container:contained relationship between a :class:`~pyLiveKML.KML.KMLObjects.Container` 
instance and a :class:`~pyLiveKML.KML.KMLObjects.Feature` instance.
"""
