from abc import ABC
from typing import Optional, Iterable, NamedTuple, Iterator

from lxml import etree

from ..KML import KML_UPDATE_CONTAINER_LIMIT_DEFAULT, State
from .Feature import Feature
from .Object import Object, ObjectChild
from .StyleSelector import StyleSelector


class Container(list[Feature], Feature, ABC):
    """A KML 'Container', per https://developers.google.com/kml/documentation/kmlreference#container. Note that while
    Containers are explicitly abstract, :class:`~pyLiveKML.KML.KMLObjects.Container` is the base class for KML
    :class:`~pyLiveKML.KML.KMLObjects.Folder` and :class:`~pyLiveKML.KML.KMLObjects.Document` that have an "existence"
    in GEP, i.e. that are (potentially) user-editable because they appear in the GEP user List View, and that may
    'contain' other :class:`~pyLiveKML.KML.KMLObjects.Feature` objects, including other concrete
    :class:`~pyLiveKML.KML.KMLObjects.Container` objects.

    :param Optional[str] name: The (optional) name for this :class:`~pyLiveKML.KML.KMLObjects.Container` that will
        be displayed in GEP.
    :param Optional[bool] visibility: The (optional) initial visibility for this
        :class:`~pyLiveKML.KML.KMLObjects.Container` in GEP.
    :param Optional[bool] is_open: Optional boolean flag to indicate whether the
        :class:`~pyLiveKML.KML.KMLObjects.Container` will be displayed as 'open' in the GEP user List View.
    :param Optional[int] update_limit: Only applies to the root of a :class:`~pyLiveKML.KML.KMLObjects.Feature` tree.
        The (approximate) maximum number of contained :class:`~pyLiveKML.KML.KMLObjects.Feature` instances that will be
        synchronized from this :class:`~pyLiveKML.KML.KMLObjects.Container` during any one synchronization update.
    :param Optional[str] style_url: An (optional) style URL, generally a reference to a global
        :class:`~pyLiveKML.KML.KMLObjects.StyleSelector` in a parent of this
        :class:`~pyLiveKML.KML.KMLObjects.Container`.
    :param Optional[Iterable[StyleSelector]] styles: An (optional) Iterable of
        :class:`~pyLiveKML.KML.KMLObjects.StyleSelector` objects that will be local to this
        :class:`~pyLiveKML.KML.KMLObjects.Container`.
    :param Optional[Iterable[Feature]] features: An (optional) Iterable of :class:`~pyLiveKML.KML.KMLObjects.Feature`
        objects to be enclosed by this :class:`~pyLiveKML.KML.KMLObjects.Container`.
    """

    @property
    def containers(self) -> Iterator['ContainedFeature']:
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
    def features(self) -> Iterator['ContainedFeature']:
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
    def is_open(self) -> Optional[bool]:
        """True if the :class:`~pyLiveKML.KML.KMLObjects.Container` will be initially displayed in an 'open' state in
        the GEP user List View, else False if it will be initially displayed in a 'closed' state.  None implies the
        default of False.
        """
        return self._is_open

    @is_open.setter
    def is_open(self, value: Optional[bool]):
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
    def update_limit(self, value: int):
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

    def build_kml(self, root: etree.Element, with_children=True):
        if self.name is not None:
            etree.SubElement(root, 'name').text = self.name
        if self.visibility is not None:
            etree.SubElement(root, 'visibility').text = str(int(self.visibility))
        if self.is_open is not None:
            etree.SubElement(root, 'open').text = str(int(self.is_open))
        if self.description is not None:
            etree.SubElement(root, 'description').text = self.description
        if with_children:
            for s in self._styles:
                root.append(s.construct_kml())

    def append(self, item: Feature):
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

    def force_idle(self, cascade: bool = False):
        """Overridden from :func:`~pyLiveKML.KML.KMLObjects.Object.Object.force_idle` to enable the entire tree of
        enclosed :class:`~pyLiveKML.KML.KMLObjects.Feature` (and :class:`~pyLiveKML.KML.KMLObjects.Container`)
        instances, and child :class:`~pyLiveKML.KML.KMLObjects.Object` instances, that is rooted in this
        :class:`~pyLiveKML.KML.KMLObjects.Container` to be forced to the IDLE state.
        """
        Object.force_idle(self)
        if cascade:
            self.force_features_idle()

    def force_features_idle(self):
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

    def select(self, value: bool, cascade: bool = False):
        """Overrides :func:`~pyLiveKML.KML.KMLObjects.Feature.Feature.select` to implement select/deselect cascade to
        enclosed :class:`~pyLiveKML.KML.KMLObjects.Feature` objects, and to ensure that if a
        :class:`~pyLiveKML.KML.KMLObjects.Container` is deleted from GEP, its' enclosed
        :class:`~pyLiveKML.KML.KMLObjects.Feature` objects are forced IDLE to maintain synchronization.
        """
        Feature.select(self, value, cascade)
        if cascade:
            for f in self:
                f.select(value, True)
        if self._state == State.DELETE_CREATED or self._state == State.DELETE_CHANGED:
            self.__deleted.clear()
            self.force_features_idle()

    def __init__(
            self,
            name: Optional[str] = None,
            visibility: Optional[bool] = None,
            is_open: Optional[bool] = None,
            update_limit: int = KML_UPDATE_CONTAINER_LIMIT_DEFAULT,
            style_url: Optional[str] = None,
            styles: Optional[Iterable[StyleSelector]] = None,
            features: Optional[Iterable[Feature]] = None,
    ):
        list[Feature].__init__(self)
        Feature.__init__(
            self,
            name=name,
            visibility=visibility,
            style_url=style_url,
            styles=styles
        )
        ABC.__init__(self)
        if features:
            self.extend(features)
        self._is_open = is_open
        self._update_limit = KML_UPDATE_CONTAINER_LIMIT_DEFAULT
        self.update_limit = update_limit
        self.__deleted = list[Feature]()

    def __str__(self):
        return Feature.__str__(self)

    def __repr__(self):
        return Feature.__repr__(self)


ContainedFeature = NamedTuple('ContainedFeature', [('container', Container), ('feature', Feature)])
"""Named tuple that describes a container:contained relationship between a :class:`~pyLiveKML.KML.KMLObjects.Container` 
instance and a :class:`~pyLiveKML.KML.KMLObjects.Feature` instance.
"""
