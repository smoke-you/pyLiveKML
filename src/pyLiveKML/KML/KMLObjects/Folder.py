from typing import Iterable

from pyLiveKML.KML.KMLObjects.Feature import Feature, Container
from pyLiveKML.KML.KMLObjects.StyleSelector import StyleSelector


class Folder(Container):
    """A KML 'Folder', per https://developers.google.com/kml/documentation/kmlreference#folder.
    :class:`~pyLiveKML.KML.KMLObjects.Folder` inherits from :class:`~pyLiveKML.KML.KMLObjects.Container` and hence
    :class:`~pyLiveKML.KML.KMLObjects.Folder` objects are containers for :class:`~pyLiveKML.KML.KMLObjects.Feature`
    objects, including other :class:`~pyLiveKML.KML.KMLObjects.Container` instances.

    :param str|None name: The (optional) name for this :class:`~pyLiveKML.KML.KMLObjects.Folder` that will
        be displayed in GEP.
    :param bool|None visibility: The (optional) initial visibility for this
        :class:`~pyLiveKML.KML.KMLObjects.Folder` in GEP.
    :param bool|None is_open: Optional flag to indicate whether the
        :class:`~pyLiveKML.KML.KMLObjects.Folder` will be displayed as 'open' in the GEP user List View.
    :param str|None style_url: An (optional) style URL, generally a reference to a global
        :class:`~pyLiveKML.KML.KMLObjects.StyleSelector` in a parent of this
        :class:`~pyLiveKML.KML.KMLObjects.Folder`.
    :param Iterable[StyleSelector]|None styles: An (optional) iterable of
        :class:`~pyLiveKML.KML.KMLObjects.StyleSelector` instances that will be local to this
        :class:`~pyLiveKML.KML.KMLObjects.Folder`.
    :param Iterable[Feature]|None features: An (optional) iterable of
        :class:`~pyLiveKML.KML.KMLObjects.Feature` instances to be enclosed by this
        :class:`~pyLiveKML.KML.KMLObjects.Folder`.
    """

    @property
    def kml_type(self) -> str:
        """Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set the KML tag name to
        'Folder'"""
        return "Folder"

    def __init__(
        self,
        name: str | None = None,
        visibility: bool | None = None,
        is_open: bool | None = None,
        style_url: str | None = None,
        styles: Iterable[StyleSelector] | None = None,
        features: Iterable[Feature] | None = None,
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
