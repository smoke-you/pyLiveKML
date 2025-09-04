"""Feature module.

:note: Includes the `Container` class definition as well, to avoid a circular import.
"""

from abc import ABC
from typing import Iterable, NamedTuple, Iterator

from lxml import etree  # type: ignore

from pyLiveKML import KML_UPDATE_CONTAINER_LIMIT_DEFAULT
from pyLiveKML.objects.AbstractView import AbstractView
from pyLiveKML.objects.Feature import Feature
from pyLiveKML.objects.Object import ObjectState, _ChildDef, ObjectChild, _ListObject
from pyLiveKML.objects.Region import Region
from pyLiveKML.objects.StyleSelector import StyleSelector
from pyLiveKML.objects.TimePrimitive import TimePrimitive


class Container(_ListObject[Feature], Feature, ABC):
    """A KML 'Container', per https://developers.google.com/kml/documentation/kmlreference#container.

    :note: While Containers are explicitly abstract,
    :class:`~pyLiveKML.KMLObjects.Container` is the base class for KML
    :class:`~pyLiveKML.KMLObjects.Folder` and
    :class:`~pyLiveKML.KMLObjects.Document` that have an "existence" in GEP, i.e.
    that are (potentially) user-editable because they appear in the GEP user List View,
    and that may 'contain' other :class:`~pyLiveKML.KMLObjects.Feature` objects,
    including other concrete :class:`~pyLiveKML.KMLObjects.Container` objects.

    :param str|None name: The (optional) name for this :class:`~pyLiveKML.KMLObjects.Container` that will
        be displayed in GEP.
    :param bool|None visibility: The (optional) initial visibility for this
        :class:`~pyLiveKML.KMLObjects.Container` in GEP.
    :param bool|None is_open: Optional boolean flag to indicate whether the
        :class:`~pyLiveKML.KMLObjects.Container` will be displayed as 'open' in the GEP user List View.
    :param int|None update_limit: Only applies to the root of a :class:`~pyLiveKML.KMLObjects.Feature` tree.
        The (approximate) maximum number of contained :class:`~pyLiveKML.KMLObjects.Feature` instances that will be
        synchronized from this :class:`~pyLiveKML.KMLObjects.Container` during any one synchronization update.
    :param str|None style_url: An (optional) style URL, generally a reference to a global
        :class:`~pyLiveKML.KMLObjects.StyleSelector` in a parent of this
        :class:`~pyLiveKML.KMLObjects.Container`.
    :param Iterable[StyleSelector]|None styles: An (optional) Iterable of
        :class:`~pyLiveKML.KMLObjects.StyleSelector` objects that will be local to this
        :class:`~pyLiveKML.KMLObjects.Container`.
    :param Iterable[Feature]|None features: An (optional) Iterable of :class:`~pyLiveKML.KMLObjects.Feature`
        objects to be enclosed by this :class:`~pyLiveKML.KMLObjects.Container`.
    """

    _kml_children: tuple[_ChildDef, ...] = Feature._kml_children + (
        _ChildDef("_contents"),
    )

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
        styles: StyleSelector | Iterable[StyleSelector] | None = None,
        region: Region | None = None,
        update_limit: int = KML_UPDATE_CONTAINER_LIMIT_DEFAULT,
        features: Feature | Iterable[Feature] | None = None,
    ):
        """Feature instance constructor."""
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
        _ListObject[Feature].__init__(self)
        ABC.__init__(self)
        self._deleted: list[Feature] = list[Feature]()
        self._contents = features
        self._is_open: bool | None = is_open
        self._update_limit: int = 0
        self.update_limit = update_limit

    @property
    def _contents(self) -> Iterator[Feature]:
        """Retrieve a generator over the `Features` in this `Container`."""
        yield from self

    @_contents.setter
    def _contents(self, value: Feature | Iterable[Feature] | None) -> None:
        self._deleted.extend(self)
        self.clear()
        if value is not None:
            if isinstance(value, Feature):
                self.append(value)
            else:
                self.extend(value)

    @property
    def update_limit(self) -> int:
        """The maximum size of a synchronization update.

        The (approximate) maximum number of KML objects that will be synchronized by any single
        synchronization update that is rooted in this :class:`~pyLiveKML.KMLObjects.Container`.
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

        A generator to retrieve instances of :class:`~pyLiveKML.KMLObjects.Feature` objects that have been
        deleted from this :class:`~pyLiveKML.KMLObjects.Container` but for which those deletions **have not** yet
        been synchronized with GEP. As the generator retrieves a deleted :class:`~pyLiveKML.KMLObjects.Feature`, it
        also completes the deletion process.

        :returns: A generator of :class:`~pyLiveKML.KMLObjects.Feature` objects.
        """
        while len(self._deleted) > 0:
            f = self._deleted[0]
            self._deleted.remove(f)
            yield f

    def remove(self, value: Feature) -> None:
        """Remove a :class:`~pyLiveKML.KMLObjects.Feature` from this :class:`~pyLiveKML.KMLObjects.Container`.

        Of course, the :class:`~pyLiveKML.KMLObjects.Feature` must be enclosed in this
        :class:`~pyLiveKML.KMLObjects.Container` to be able to be removed.

        :param Feature __value: The :class:`~pyLiveKML.KMLObjects.Feature` to be removed.
        """
        if value.active:
            self._deleted.append(value)
        _ListObject[Feature].remove(self, value)

    def force_idle(self, cascade: bool = False) -> None:
        """Force this instance, and _optionally_ its children, to the IDLE state.

        Overridden from :func:`~pyLiveKML.KMLObjects.Object.Object.force_idle` to enable the entire tree of
        enclosed :class:`~pyLiveKML.KMLObjects.Feature` (and :class:`~pyLiveKML.KMLObjects.Container`)
        instances, and child :class:`~pyLiveKML.KMLObjects.Object` instances, that is rooted in this
        :class:`~pyLiveKML.KMLObjects.Container` to be forced to the IDLE state.
        """
        super().force_idle()
        if cascade:
            self.force_features_idle()

    def force_features_idle(self) -> None:
        """Force this instance, and _all_ of its children, to the IDLE state.

        Force the entire tree of enclosed :class:`~pyLiveKML.KMLObjects.Feature` (and
        :class:`~pyLiveKML.KMLObjects.Container`) instances to be forced to the IDLE state. Typically called as a
        result of the target :class:`~pyLiveKML.KMLObjects.Container` being deleted from GEP.
        """
        for f in self:
            if isinstance(f, Container):
                # note the implication from force_idle() that cascade is _always_ true for force_features_idle
                f.force_idle(True)
            elif isinstance(f, Feature):
                f.force_idle()

    def activate(self, value: bool, cascade: bool = False) -> None:
        """Cascade activate upwards, but do not cascade deactivate upwards.

        Overrides :func:`~pyLiveKML.KMLObjects.Feature.Feature.activate` to implement activate/deactivate cascade to
        enclosed :class:`~pyLiveKML.KMLObjects.Feature` objects, and to ensure that if a
        :class:`~pyLiveKML.KMLObjects.Container` is deleted from GEP, its' enclosed
        :class:`~pyLiveKML.KMLObjects.Feature` objects are forced IDLE to maintain synchronization.
        """
        Feature.activate(self, value, cascade)
        if cascade:
            for f in self:
                f.activate(value, True)
        if (
            self._state == ObjectState.DELETE_CREATED
            or self._state == ObjectState.DELETE_CHANGED
        ):
            self._deleted.clear()
            self.force_features_idle()
