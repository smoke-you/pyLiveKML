"""Folder module."""

from typing import Iterable

from pyLiveKML import KML_UPDATE_CONTAINER_LIMIT_DEFAULT
from pyLiveKML.objects.AbstractView import AbstractView
from pyLiveKML.objects.Feature import Feature
from pyLiveKML.objects.Container import Container
from pyLiveKML.objects.StyleSelector import StyleSelector
from pyLiveKML.objects.TimePrimitive import TimePrimitive


class Folder(Container):
    """A KML 'Folder', per https://developers.google.com/kml/documentation/kmlreference#folder.

    :class:`~pyLiveKML.KMLObjects.Folder` inherits from :class:`~pyLiveKML.KMLObjects.Container` and hence
    :class:`~pyLiveKML.KMLObjects.Folder` objects are containers for :class:`~pyLiveKML.KMLObjects.Feature`
    objects, including other :class:`~pyLiveKML.KMLObjects.Container` instances.

    :param str|None name: The (optional) name for this :class:`~pyLiveKML.KMLObjects.Folder` that will
        be displayed in GEP.
    :param bool|None visibility: The (optional) initial visibility for this
        :class:`~pyLiveKML.KMLObjects.Folder` in GEP.
    :param bool|None is_open: Optional flag to indicate whether the
        :class:`~pyLiveKML.KMLObjects.Folder` will be displayed as 'open' in the GEP user List View.
    :param str|None style_url: An (optional) style URL, generally a reference to a global
        :class:`~pyLiveKML.KMLObjects.StyleSelector` in a parent of this
        :class:`~pyLiveKML.KMLObjects.Folder`.
    :param Iterable[StyleSelector]|None styles: An (optional) iterable of
        :class:`~pyLiveKML.KMLObjects.StyleSelector` instances that will be local to this
        :class:`~pyLiveKML.KMLObjects.Folder`.
    :param Iterable[Feature]|None features: An (optional) iterable of
        :class:`~pyLiveKML.KMLObjects.Feature` instances to be enclosed by this
        :class:`~pyLiveKML.KMLObjects.Folder`.
    """

    _kml_tag = "Folder"

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
        features: Feature | Iterable[Feature] | None = None,
    ):
        """Folder instance constructor."""
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
