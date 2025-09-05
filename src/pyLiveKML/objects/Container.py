"""Container module."""

from abc import ABC
from typing import Iterable, Iterator

from lxml import etree  # type: ignore

from pyLiveKML import KML_UPDATE_CONTAINER_LIMIT_DEFAULT
from pyLiveKML.objects.AbstractView import AbstractView
from pyLiveKML.objects.Feature import Feature
from pyLiveKML.objects.Object import ObjectState, _ChildDef, _ListObject
from pyLiveKML.objects.Region import Region
from pyLiveKML.objects.StyleSelector import StyleSelector
from pyLiveKML.objects.TimePrimitive import TimePrimitive


class Container(_ListObject[Feature], Feature, ABC):
    """A KML `<Container>` tag constructor.

    This is an abstract element and cannot be used directly in a KML file. A `Container`
    element holds one or more `Feature` elements, which may themselves be `Container`
    instances, so allows the creation of nested hierarchies.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#container

    Parameters
    ----------
    name : str|None, default = None
        User-defined text displayed in the 3D viewer as the label for the object.
    visibility : bool | None, default = None
        Specifies whether the `Feature` is drawn in the 3D viewer when it is initially
        loaded. In order for a `Feature` to be visible, the `<visibility>` tag of all
        its ancestors must also be set `True`.
    is_open : bool | None, default = None
        Specifies whether a `Document` or `Folder` appears closed or open when first
        loaded into the "Places" panel. `False` or `None` is collapsed (the default),
        `True` is expanded. This element applies only to `Document`, `Folder`, and
        `NetworkLink`.
    author_name : str | None, default = None
        The name of the author of the `Feature`.
    author_link : str | None, default = None
        URL of the web page containing the KML file.
    address : str | None, default = None
        A string value representing an unstructured address written as a standard street,
        city, state address, and/or as a postal code.
    phone_number : str | None, default = None
        A string value representing a telephone number. This element is used by Google
        Maps Mobile only. The industry standard for Java-enabled cellular phones is
        RFC2806.
    snippet : str | None, default = None
        A short description of the `Feature`. In Google Earth, this description is
        displayed in the "Places" panel under the name of the `Feature`. If a `<Snippet>`
        is not supplied, the first two lines of the `<description>` are used. In Google
        Earth, if a `Placemark` contains both a `<description>` and a `<Snippet>`, the
        `<Snippet>` appears beneath the `Placemark` in the "Places" panel, and the
        `<description>` appears in the `Placemark`'s description balloon. This tag does
        not support HTML markup.
    snippet_max_lines : int | None, default = None
    description : str | None, default = None
        User-supplied content that appears in the description balloon. HTML *is*
        supported, but it is **highly** recommended to read the detailed documentation
        at
        https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-feature
    abstract_view : AbstractView | None, default = None
        Any concrete subclass of :class:`pyLiveKML.objects.AbstractView`, i.e. either a
        :class:`pyLiveKML.objects.Camera` or :class:`pyLiveKML.objects.LookAt`
    time_primitive : TimePrimitive | None, default = None
        Any concrete subclass of :class:`pyLiveKML.objects.TimePrimitive`, i.e. either a
        :class:`pyLiveKML.objects.TimeStamp` or :class:`pyLiveKML.objects.TimeSpan`
    style_url : str | None = None
        URL of a `<Style>` or `<StyleMap>` defined in a `<Document>`. If the style is in
        the same file, use a # reference. If the style is defined in an external file,
        use a full URL along with # referencing.
    styles : StyleSelector | Iterable[StyleSelector] | None, default = None
        One or more `Style`s and `StyleMap`s can be defined to customize the appearance
        of any element derived from `Feature` or of the `Geometry` in a `Placemark`. A
        style defined within a `Feature` is called an "inline style" and applies only to
        the `Feature` that contains it. A style defined as the child of a `<Document>` is
        called a "shared style." A shared style must have an id defined for it. This id
        is referenced by one or more `Features` within the `<Document>`. In cases where
        a style element is defined both in a shared style and in an inline style for a
        `Feature` — that is, a `Folder`, `GroundOverlay`, `NetworkLink`, `Placemark`, or
        `ScreenOverlay` — the value for the `Feature`'s inline style takes precedence over
        the value for the shared style.
    region : Region | None, default = None
        `Feature`s and `Geometry`'s associated with a `Region` are drawn only when the
        `Region` is active.
    features : Feature | Iterable[Feature] | None, default = None
        The `Feature`'s contained by this `Container`.

    """

    _kml_children: tuple[_ChildDef, ...] = Feature._kml_children + (
        _ChildDef("features"),
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
        features: Feature | Iterable[Feature] | None = None,
    ):
        """Feature instance constructor."""
        Feature.__init__(
            self,
            name=name,
            visibility=visibility,
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
        self.features = features
        self._is_open: bool | None = is_open
        self._update_limit: int = 0

    @property
    def features(self) -> Iterator[Feature]:
        """Retrieve a generator over the `Features` in this `Container`.
        
        If the property setter is called, replaces the current list of contained 
        `Feature`'s with those provided.

        Parameters
        ----------
        value : Feature | Iterable[Feature] | None
            The new `Feature` elements for the `Container`.

        :returns: A generator over the `Features` in the `Container`.
        :rtype: Iterator[Feature]
        """
        yield from self

    @features.setter
    def features(self, value: Feature | Iterable[Feature] | None) -> None:
        self._deleted.extend(self)
        self.clear()
        if value is not None:
            if isinstance(value, Feature):
                self.append(value)
            else:
                self.extend(value)

    def clear(self) -> None:
        """Remove all of the `Feature`'s enclosed in this `Container`."""
        self._deleted.extend(self.features)
        super().clear()

    def remove(self, value: Feature) -> None:
        """Remove a single `Feature` from this `Container."""
        if value.active:
            self._deleted.append(value)
        super().remove(value)

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
