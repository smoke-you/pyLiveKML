from typing import Optional, Iterator, cast

from lxml import etree  # type: ignore

from .Feature import Feature
from .Geometry import Geometry
from .StyleSelector import StyleSelector
from .Object import ObjectChild


class Placemark(Feature):
    """A KML 'Placemark', per https://developers.google.com/kml/documentation/kmlreference#placemark.
    :class:`~pyLiveKML.KML.KMLObjects.Placemark` objects are containers for a geospatial element to be displayed in GEP.

    :param Geometry geometry: A concrete :class:`~pyLiveKML.KML.KMLObjects.Geometry` instance that will be displayed
        in GEP for this :class:`~pyLiveKML.KML.KMLObjects.Placemark`.
    :param Optional[str] name: The (optional) name that will be displayed in GEP for this
        :class:`~pyLiveKML.KML.KMLObjects.Placemark`.
    :param Optional[bool] visibility: The (optional) initial visibility for this
        :class:`~pyLiveKML.KML.KMLObjects.Placemark` in GEP.
    :param Optional[StyleSelector] inline_style: An (optional) :class:`~pyLiveKML.KML.KMLObjects.StyleSelector` that
        will be applied to this :class:`~pyLiveKML.KML.KMLObjects.Placemark` (only).
    :param Optional[str] style_url: An (optional) style URL, generally a reference to a global
        :class:`~pyLiveKML.KML.KMLObjects.StyleSelector` in a parent of this
        :class:`~pyLiveKML.KML.KMLObjects.Placemark`.
    """

    def __init__(
        self,
        geometry: Geometry,
        name: Optional[str] = None,
        visibility: Optional[bool] = None,
        inline_style: Optional[StyleSelector] = None,
        style_url: Optional[str] = None,
    ):
        Feature.__init__(self, name=name, visibility=visibility, style_url=style_url)
        self._geometry = geometry
        if inline_style:
            self._styles.append(inline_style)

    @property
    def kml_type(self) -> str:
        """Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set the KML tag name to
        'Placemark'
        """
        return "Placemark"

    @property
    def children(self) -> Iterator[ObjectChild]:
        """Overridden from :attr:`pyLiveKML.KML.KMLObjects.Object.Object.children` to yield the children of a
        :class:`~pyLiveKML.KML.KMLObjects.Placemark`, i.e. a :class:`~pyLiveKML.KML.KMLObjects.Geometry` instance, zero
        or more :class:`~pyLiveKML.KML.KMLObjects.StyleSelector` instances, and any dependent
        :class:`~pyLiveKML.KML.KMLObjects.SubStyle` instances.
        """
        yield ObjectChild(parent=self, child=self.geometry)
        yield from self.geometry.children
        for s in self._styles:
            yield ObjectChild(parent=self, child=s)
            yield from s.children

    @property
    def geometry(self) -> Geometry:
        """The geospatial object, or :class:`~pyLiveKML.KML.KMLObjects.Geometry`, that will be displayed in GEP as
        this :class:`~pyLiveKML.KML.KMLObjects.Placemark`.
        """
        return self._geometry

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        if self._name is not None:
            etree.SubElement(root, "name").text = self.name
        if self._visibility is not None:
            etree.SubElement(root, "visibility").text = str(
                int(cast(bool, self.visibility))
            )
        if self._description is not None:
            etree.SubElement(root, "description").text = self.description
        if self._style_url is not None:
            etree.SubElement(root, "styleUrl").text = self._style_url
        if with_children:
            for s in self._styles:
                root.append(s.construct_kml())
            root.append(self.geometry.construct_kml())
