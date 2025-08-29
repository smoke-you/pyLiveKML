"""Placemark module."""

from typing import Iterator

from lxml import etree  # type: ignore

from pyLiveKML.KMLObjects.Feature import Feature
from pyLiveKML.KMLObjects.Geometry import Geometry
from pyLiveKML.KMLObjects.Object import ObjectChild
from pyLiveKML.KMLObjects.StyleSelector import StyleSelector


class Placemark(Feature):
    """A KML 'Placemark', per https://developers.google.com/kml/documentation/kmlreference#placemark.

    :class:`~pyLiveKML.KMLObjects.Placemark` objects are containers for a geospatial element to be displayed in GEP.

    :param Geometry geometry: A concrete :class:`~pyLiveKML.KMLObjects.Geometry` instance that will be displayed
        in GEP for this :class:`~pyLiveKML.KMLObjects.Placemark`.
    :param str|None name: The (optional) name that will be displayed in GEP for this
        :class:`~pyLiveKML.KMLObjects.Placemark`.
    :param bool|None visibility: The (optional) initial visibility for this
        :class:`~pyLiveKML.KMLObjects.Placemark` in GEP.
    :param StyleSelector|None inline_style: An (optional) :class:`~pyLiveKML.KMLObjects.StyleSelector` that
        will be applied to this :class:`~pyLiveKML.KMLObjects.Placemark` (only).
    :param str|None style_url: An (optional) style URL, generally a reference to a global
        :class:`~pyLiveKML.KMLObjects.StyleSelector` in a parent of this
        :class:`~pyLiveKML.KMLObjects.Placemark`.
    """

    _kml_tag = "Placemark"
    _direct_children = Feature._direct_children + ("_geometry",)

    def __init__(
        self,
        geometry: Geometry,
        name: str | None = None,
        visibility: bool | None = None,
        inline_style: StyleSelector | None = None,
        style_url: str | None = None,
    ):
        """Placemark instance constructor."""
        Feature.__init__(self, name=name, visibility=visibility, style_url=style_url)
        self._geometry = geometry
        if inline_style:
            self._styles.append(inline_style)

    @property
    def children(self) -> Iterator[ObjectChild]:
        """The children of the instance.

        Overridden from :attr:`pyLiveKML.KMLObjects.Object.Object.children` to yield
        the children of a :class:`~pyLiveKML.KMLObjects.Placemark`, i.e. a single
        :class:`~pyLiveKML.KMLObjects.Geometry` instance, zero or more
        :class:`~pyLiveKML.KMLObjects.StyleSelector` instances, and any dependent
        :class:`~pyLiveKML.KMLObjects.SubStyle` instances.
        """
        yield ObjectChild(parent=self, child=self.geometry)
        yield from self.geometry.children
        for s in self._styles:
            yield ObjectChild(parent=self, child=s)
            yield from s.children

    @property
    def geometry(self) -> Geometry:
        """The child :class:`~pyLiveKML.KMLObjects.Geometry` instance.

        The geospatial object, or :class:`~pyLiveKML.KMLObjects.Geometry`, that will
        be displayed in GEP as this :class:`~pyLiveKML.KMLObjects.Placemark`.
        """
        return self._geometry
