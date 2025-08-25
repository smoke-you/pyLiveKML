"""NetworkLink module."""

from typing import Iterator, Iterable

from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import RefreshMode
from pyLiveKML.KML.KMLObjects.Feature import Feature
from pyLiveKML.KML.KMLObjects.Link import Link
from pyLiveKML.KML.KMLObjects.Object import ObjectChild
from pyLiveKML.KML.KMLObjects.StyleSelector import StyleSelector


class NetworkLink(Feature):
    """A KML 'NetworkLink', per https://developers.google.com/kml/documentation/kmlreference#networklink.

    :class:`~pyLiveKML.KML.KMLObjects.NetworkLink` objects are typically used to direct GEP to periodically retrieve a
    file from a specified href.

    :param str|None name: The (optional) text that will be displayed in the GEP user List View as the name of the
        :class:`~pyLiveKML.KML.KMLObjects.NetworkLink`.
    :param str|None href: An (optional) href for the file that will be loaded by the
        :class:`~pyLiveKML.KML.KMLObjects.NetworkLink`.
    :param RefreshMode|None refresh_mode: The (optional) refresh mode that will be used for file loading.
    :param float|None refresh_interval: The (optional) refresh interval, in seconds, that will be used for file
        loading.
    :param bool|None is_open: Optional flag to indicate whether the :class:`~pyLiveKML.KML.KMLObjects.NetworkLink`
        will be displayed as 'open' in the GEP user List View.
    """

    _kml_type = "NetworkLink"

    def __init__(
        self,
        name: str | None = None,
        visibility: bool | None = None,
        is_open: bool | None = None,
        description: str | None = None,
        style_url: str | None = None,
        styles: Iterable[StyleSelector] | None = None,
        href: str | None = None,
        refresh_mode: RefreshMode | None = None,
        refresh_interval: float | None = None,
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
        self._is_open = is_open
        self._link = Link(href, refresh_mode, refresh_interval)
        self._fly_to_view = False
        self._refresh_visibility = False

    @property
    def children(self) -> Iterator[ObjectChild]:
        """The children of the instance."""
        if self._link:
            yield ObjectChild(self, self._link)
        for s in self.styles:
            yield ObjectChild(self, s)

    @property
    def link(self) -> Link:
        """The child :class:`~pyLiveKML.KML.KMLObjects.Link` instance.

        The child :class:`~pyLiveKML.KML.KMLObjects.Link` object that identifies how and from where this
        :class:`~pyLiveKML.KML.KMLObjects.NetworkLink` will load its dependent file.
        """
        return self._link

    @property
    def fly_to_view(self) -> bool:
        """Flag to indicate whether GEP should fly to the instance's view location when it is loaded.

        True if this :class:`~pyLiveKML.KML.KMLObjects.NetworkLink` instructs GEP to
        fly to its view location when loaded, else False if it does not. None implies
        the default of False.
        """
        return self._fly_to_view

    @fly_to_view.setter
    def fly_to_view(self, value: bool) -> None:
        if self._fly_to_view != value:
            self._fly_to_view = value

    @property
    def refresh_visibility(self) -> bool:
        """Flag to indicate whether the visibility of the instance or its children can be changed in the UI.

        True if the GEP user is not permitted to control the visibility of the
        :class:`~pyLiveKML.KML.KMLObjects.NetworkLink` or its children, else False if
        the GEP user has full control over that visibility.  None implies the default
        of False.
        """
        return self._refresh_visibility

    @refresh_visibility.setter
    def refresh_visibility(self, value: bool) -> None:
        if self._refresh_visibility != value:
            self._refresh_visibility = value

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        if self._style_url:
            etree.SubElement(root, "styleUrl").text = self._style_url
        etree.SubElement(root, "refreshVisibility").text = str(
            int(self._refresh_visibility)
        )
        etree.SubElement(root, "flyToView").text = str(int(self._fly_to_view))
        if with_children:
            if self._link:
                root.append(self._link.construct_kml())
