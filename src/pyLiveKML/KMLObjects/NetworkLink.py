"""NetworkLink module."""

from typing import Iterator, Iterable

from lxml import etree  # type: ignore

from pyLiveKML.KML import RefreshModeEnum
from pyLiveKML.KML._BaseObject import _FieldDef
from pyLiveKML.KMLObjects.Feature import Feature
from pyLiveKML.KMLObjects.Link import Link
from pyLiveKML.KMLObjects.Object import ObjectChild, _ChildDef
from pyLiveKML.KMLObjects.StyleSelector import StyleSelector


class NetworkLink(Feature):
    """A KML 'NetworkLink', per https://developers.google.com/kml/documentation/kmlreference#networklink.

    :class:`~pyLiveKML.KMLObjects.NetworkLink` objects are typically used to direct GEP to periodically retrieve a
    file from a specified href.

    :param str|None name: The (optional) text that will be displayed in the GEP user List View as the name of the
        :class:`~pyLiveKML.KMLObjects.NetworkLink`.
    :param str|None href: An (optional) href for the file that will be loaded by the
        :class:`~pyLiveKML.KMLObjects.NetworkLink`.
    :param RefreshMode|None refresh_mode: The (optional) refresh mode that will be used for file loading.
    :param float|None refresh_interval: The (optional) refresh interval, in seconds, that will be used for file
        loading.
    :param bool|None is_open: Optional flag to indicate whether the :class:`~pyLiveKML.KMLObjects.NetworkLink`
        will be displayed as 'open' in the GEP user List View.
    """

    _kml_tag = "NetworkLink"
    _kml_fields = Feature._kml_fields + (
        _FieldDef("fly_to_view", "flyToView"),
        _FieldDef("refresh_visibility", "refreshVisibility"),
    )
    _direct_children = Feature._direct_children + (_ChildDef("link"),)

    def __init__(
        self,
        name: str | None = None,
        visibility: bool | None = None,
        is_open: bool | None = None,
        description: str | None = None,
        style_url: str | None = None,
        styles: Iterable[StyleSelector] | None = None,
        href: str | None = None,
        refresh_mode: RefreshModeEnum | None = None,
        refresh_interval: float | None = None,
        fly_to_view: bool | None = None,
        refresh_visibility: bool | None = None,
    ):
        """NetworkLink instance constructor."""
        Feature.__init__(
            self,
            name=name,
            visibility=visibility,
            is_open=is_open,
            description=description,
            style_url=style_url,
            styles=styles,
        )
        self.link = Link(href, refresh_mode, refresh_interval)
        self.fly_to_view = fly_to_view
        self.refresh_visibility = refresh_visibility

    @property
    def children(self) -> Iterator[ObjectChild]:
        """The children of the instance."""
        if self.link:
            yield ObjectChild(self, self.link)
        yield from super().children
