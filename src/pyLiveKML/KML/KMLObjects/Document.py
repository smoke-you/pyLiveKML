"""Document module."""

from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import KML_UPDATE_CONTAINER_LIMIT_DEFAULT
from pyLiveKML.KML.KMLObjects.Feature import Feature, Container
from pyLiveKML.KML.KMLObjects.Schema import Schema
from pyLiveKML.KML.KMLObjects.StyleSelector import StyleSelector


class Document(Container):
    """A KML 'Document', per https://developers.google.com/kml/documentation/kmlreference#document.

    :class:`~pyLiveKML.KML.KMLObjects.Document` inherits from :class:`~pyLiveKML.KML.KMLObjects.Container` and hence
    :class:`~pyLiveKML.KML.KMLObjects.Document` objects are containers for :class:`~pyLiveKML.KML.KMLObjects.Feature`
    objects, including other :class:`~pyLiveKML.KML.KMLObjects.Container` instances.

    :param str|None name: The (optional) name for this :class:`~pyLiveKML.KML.KMLObjects.Document` that will
        be displayed in GEP.
    :param bool|None visibility: The (optional) initial visibility for this
        :class:`~pyLiveKML.KML.KMLObjects.Document` in GEP.
    :param bool|None is_open: Optional flag to indicate whether the
        :class:`~pyLiveKML.KML.KMLObjects.Document` will be displayed as 'open' in the GEP user List View.
    :param str|None style_url: An (optional) style URL, generally a reference to a global
        :class:`~pyLiveKML.KML.KMLObjects.StyleSelector` in a parent of this
        :class:`~pyLiveKML.KML.KMLObjects.Document`.
    :param Iterable[StyleSelector]|None styles: An (optional) iterable of
        :class:`~pyLiveKML.KML.KMLObjects.StyleSelector` instances that will be local to this
        :class:`~pyLiveKML.KML.KMLObjects.Document`.
    :param Iterable[Feature]|None features: An (optional) iterable of
        :class:`~pyLiveKML.KML.KMLObjects.Feature` instances to be enclosed by this
        :class:`~pyLiveKML.KML.KMLObjects.Document`.
    """

    _kml_type = "Document"

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
        style_url: str | None = None,
        styles: Iterable[StyleSelector] | None = None,
        update_limit: int = KML_UPDATE_CONTAINER_LIMIT_DEFAULT,
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
            style_url=style_url,
            styles=styles,
            update_limit=update_limit,
            features=features,
        )
        self.schemas = list[Schema]()
        if schemas is not None:
            if isinstance(schemas, Schema):
                self.schemas.append(schemas)
            else:
                self.schemas.extend(schemas)

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        for s in self.schemas:
            root.append(s.construct_kml())
