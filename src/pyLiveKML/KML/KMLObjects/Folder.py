from typing import Optional, Iterable

from .Feature import Feature
from .Container import Container
from .StyleSelector import StyleSelector


class Folder(Container):
    """A KML 'Folder', per https://developers.google.com/kml/documentation/kmlreference#folder.
    :class:`~pyLiveKML.KML.KMLObjects.Folder` inherits from :class:`~pyLiveKML.KML.KMLObjects.Container` and hence
    :class:`~pyLiveKML.KML.KMLObjects.Folder` objects are containers for :class:`~pyLiveKML.KML.KMLObjects.Feature`
    objects, including other :class:`~pyLiveKML.KML.KMLObjects.Container` instances.

    :param Optional[str] name: The (optional) name for this :class:`~pyLiveKML.KML.KMLObjects.Folder` that will
        be displayed in GEP.
    :param Optional[bool] visibility: The (optional) initial visibility for this
        :class:`~pyLiveKML.KML.KMLObjects.Folder` in GEP.
    :param Optional[bool] is_open: Optional flag to indicate whether the
        :class:`~pyLiveKML.KML.KMLObjects.Folder` will be displayed as 'open' in the GEP user List View.
    :param Optional[str] style_url: An (optional) style URL, generally a reference to a global
        :class:`~pyLiveKML.KML.KMLObjects.StyleSelector` in a parent of this
        :class:`~pyLiveKML.KML.KMLObjects.Folder`.
    :param Optional[Iterable[StyleSelector]] styles: An (optional) iterable of
        :class:`~pyLiveKML.KML.KMLObjects.StyleSelector` instances that will be local to this
        :class:`~pyLiveKML.KML.KMLObjects.Folder`.
    :param Optional[Iterable[Feature]] features: An (optional) iterable of
        :class:`~pyLiveKML.KML.KMLObjects.Feature` instances to be enclosed by this
        :class:`~pyLiveKML.KML.KMLObjects.Folder`.
    """

    @property
    def kml_type(self) -> str:
        """Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set the KML tag name to
        'Folder'"""
        return 'Folder'

    def __init__(
            self,
            name: Optional[str] = None,
            visibility: Optional[bool] = None,
            is_open: Optional[bool] = None,
            style_url: Optional[str] = None,
            styles: Optional[Iterable[StyleSelector]] = None,
            features: Optional[Iterable[Feature]] = None,
    ):
        Container.__init__(
            self,
            name=name,
            visibility=visibility,
            is_open=is_open,
            style_url=style_url,
            styles=styles,
            features=features,
        )
