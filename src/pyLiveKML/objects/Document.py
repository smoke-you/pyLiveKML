"""Document module."""

from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML import KML_UPDATE_CONTAINER_LIMIT_DEFAULT
from pyLiveKML.objects.Object import _ChildDef
from pyLiveKML.objects.AbstractView import AbstractView
from pyLiveKML.objects.Container import Container
from pyLiveKML.objects.Feature import Feature
from pyLiveKML.objects.Schema import Schema
from pyLiveKML.objects.StyleSelector import StyleSelector
from pyLiveKML.objects.TimePrimitive import TimePrimitive


class Document(Container):
    """A KML 'Document', per https://developers.google.com/kml/documentation/kmlreference#document.

    :class:`~pyLiveKML.KMLObjects.Document` inherits from :class:`~pyLiveKML.KMLObjects.Container` and hence
    :class:`~pyLiveKML.KMLObjects.Document` objects are containers for :class:`~pyLiveKML.KMLObjects.Feature`
    objects, including other :class:`~pyLiveKML.KMLObjects.Container` instances.

    :param str|None name: The (optional) name for this :class:`~pyLiveKML.KMLObjects.Document` that will
        be displayed in GEP.
    :param bool|None visibility: The (optional) initial visibility for this
        :class:`~pyLiveKML.KMLObjects.Document` in GEP.
    :param bool|None is_open: Optional flag to indicate whether the
        :class:`~pyLiveKML.KMLObjects.Document` will be displayed as 'open' in the GEP user List View.
    :param str|None style_url: An (optional) style URL, generally a reference to a global
        :class:`~pyLiveKML.KMLObjects.StyleSelector` in a parent of this
        :class:`~pyLiveKML.KMLObjects.Document`.
    :param Iterable[StyleSelector]|None styles: An (optional) iterable of
        :class:`~pyLiveKML.KMLObjects.StyleSelector` instances that will be local to this
        :class:`~pyLiveKML.KMLObjects.Document`.
    :param Iterable[Feature]|None features: An (optional) iterable of
        :class:`~pyLiveKML.KMLObjects.Feature` instances to be enclosed by this
        :class:`~pyLiveKML.KMLObjects.Document`.
    """

    _kml_tag = "Document"
    _kml_children = Container._kml_children + (_ChildDef("schemas"),)

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
        features: Feature | Iterable[Feature] | None = None,
        schemas: Schema | Iterable[Schema] | None = None,
    ):
        """Document instance constructor."""
        super().__init__(
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
            features=features,
        )
        self._schemas = list[Schema]()
        self.schemas = schemas

    @property
    def schemas(self) -> Iterable[Schema]:
        """Generator across schema instances."""
        yield from self._schemas

    @schemas.setter
    def schemas(self, value: Schema | Iterable[Schema] | None) -> None:
        self._schemas.clear()
        if value is not None:
            if isinstance(value, Schema):
                self._schemas.append(value)
            else:
                self._schemas.extend(value)
