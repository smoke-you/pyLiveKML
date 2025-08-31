"""Placemark module."""

from typing import Iterator

from lxml import etree  # type: ignore

from pyLiveKML.KMLObjects.AbstractView import AbstractView
from pyLiveKML.KMLObjects.Feature import Feature
from pyLiveKML.KMLObjects.Geometry import Geometry
from pyLiveKML.KMLObjects.Object import Object, ObjectChild
from pyLiveKML.KMLObjects.Region import Region
from pyLiveKML.KMLObjects.StyleSelector import StyleSelector
from pyLiveKML.KMLObjects.TimePrimitive import TimePrimitive


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

    def __init__(
        self,
        geometry: Geometry,
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
        inline_style: StyleSelector | None = None,
        style_url: str | None = None,
        region: Region | None = None,
    ):
        """Placemark instance constructor."""
        Feature.__init__(
            self,
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
            styles=inline_style,
            region=region,
        )
        self.geometry = geometry

    @property
    def children(self) -> Iterator[ObjectChild]:
        """The children of the instance.

        Overridden from :attr:`pyLiveKML.KMLObjects.Object.Object.children` to yield
        the children of a :class:`~pyLiveKML.KMLObjects.Placemark`, i.e. a single
        :class:`~pyLiveKML.KMLObjects.Geometry` instance, zero or more
        :class:`~pyLiveKML.KMLObjects.StyleSelector` instances, and any dependent
        :class:`~pyLiveKML.KMLObjects.SubStyle` instances.
        """
        yield from super(Feature, self).children
        yield ObjectChild(parent=self, child=self.geometry)
        yield from self.geometry.children

    @property
    def direct_children(self) -> Iterator[Object]:
        """Retrieve a generator over the direct children of the object.

        That is, retrieve any `Object` instances that are embedded in this `Object`.
        """
        yield from super().direct_children
        yield self.geometry
