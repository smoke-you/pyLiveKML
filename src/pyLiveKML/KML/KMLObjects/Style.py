from typing import Optional, Iterator

from lxml import etree  # type: ignore

from .BalloonStyle import BalloonStyle
from .IconStyle import IconStyle
from .LabelStyle import LabelStyle
from .LineStyle import LineStyle
from .ListStyle import ListStyle
from .Object import ObjectChild
from .PolyStyle import PolyStyle
from .StyleSelector import StyleSelector


class Style(StyleSelector):
    """A KML 'Style', per https://developers.google.com/kml/documentation/kmlreference#style. A group of
    :class:`~pyLiveKML.KML.KMLObjects.SubStyle` objects that can be referenced by its :attr:`id` or inserted in-line
    into a :class:`~pyLiveKML.KML.KMLObjects.Feature`.

    :param Optional[BalloonStyle] balloon_style: An (optional) :class:`~pyLiveKML.KML.KMLObjects.BalloonStyle` to be
        embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`.
    :param Optional[IconStyle] icon_style: An (optional) :class:`~pyLiveKML.KML.KMLObjects.IconStyle` to be
        embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`.
    :param Optional[LabelStyle] label_style: An (optional) :class:`~pyLiveKML.KML.KMLObjects.LabelStyle` to be
        embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`.
    :param Optional[LineStyle] line_style: An (optional) :class:`~pyLiveKML.KML.KMLObjects.LineStyle` to be
        embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`.
    :param Optional[ListStyle] list_style: An (optional) :class:`~pyLiveKML.KML.KMLObjects.ListStyle` to be
        embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`.
    :param Optional[PolyStyle] poly_style: An (optional) :class:`~pyLiveKML.KML.KMLObjects.PolyStyle` to be
        embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`.
    """

    @property
    def kml_type(self) -> str:
        """Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set the KML tag name to
        'Style'"""
        return "Style"

    @property
    def children(self) -> Iterator[ObjectChild]:
        """Overridden from :attr:`pyLiveKML.KML.KMLObjects.Object.Object.children` to yield the children of a
        :class:`~pyLiveKML.KML.KMLObjects.Style`, i.e. one or more :class:`~pyLiveKML.KML.KMLObjects.SubStyle`
        instances.
        """
        if self._balloon_style:
            yield ObjectChild(parent=self, child=self._balloon_style)
        if self._icon_style:
            yield ObjectChild(parent=self, child=self._icon_style)
        if self._label_style:
            yield ObjectChild(parent=self, child=self._label_style)
        if self._line_style:
            yield ObjectChild(parent=self, child=self._line_style)
        if self._list_style:
            yield ObjectChild(parent=self, child=self._list_style)
        if self._poly_style:
            yield ObjectChild(parent=self, child=self._poly_style)

    @property
    def balloon_style(self) -> Optional[BalloonStyle]:
        """A :class:`~pyLiveKML.KML.KMLObjects.BalloonStyle` embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`"""
        return self._balloon_style

    @property
    def icon_style(self) -> Optional[IconStyle]:
        """An :class:`~pyLiveKML.KML.KMLObjects.IconStyle` embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`"""
        return self._icon_style

    @property
    def label_style(self) -> Optional[LabelStyle]:
        """A :class:`~pyLiveKML.KML.KMLObjects.LabelStyle` embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`"""
        return self._label_style

    @property
    def line_style(self) -> Optional[LineStyle]:
        """A :class:`~pyLiveKML.KML.KMLObjects.LineStyle` embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`"""
        return self._line_style

    @property
    def list_style(self) -> Optional[ListStyle]:
        """A :class:`~pyLiveKML.KML.KMLObjects.ListStyle` embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`"""
        return self._list_style

    @property
    def poly_style(self) -> Optional[PolyStyle]:
        """A :class:`~pyLiveKML.KML.KMLObjects.PolyStyle` embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`"""
        return self._poly_style

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        if with_children:
            if self._balloon_style is not None:
                root.append(self._balloon_style.construct_kml())
            if self._icon_style is not None:
                root.append(self._icon_style.construct_kml())
            if self._label_style is not None:
                root.append(self._label_style.construct_kml())
            if self._line_style is not None:
                root.append(self._line_style.construct_kml())
            if self._list_style is not None:
                root.append(self._list_style.construct_kml())
            if self._poly_style is not None:
                root.append(self._poly_style.construct_kml())

    def __init__(
        self,
        balloon_style: Optional[BalloonStyle] = None,
        icon_style: Optional[IconStyle] = None,
        label_style: Optional[LabelStyle] = None,
        line_style: Optional[LineStyle] = None,
        list_style: Optional[ListStyle] = None,
        poly_style: Optional[PolyStyle] = None,
    ):
        StyleSelector.__init__(self)
        self._balloon_style: Optional[BalloonStyle] = balloon_style
        self._icon_style: Optional[IconStyle] = icon_style
        self._label_style: Optional[LabelStyle] = label_style
        self._line_style: Optional[LineStyle] = line_style
        self._list_style: Optional[ListStyle] = list_style
        self._poly_style: Optional[PolyStyle] = poly_style

    def __str__(self) -> str:
        return f"{self.kml_type}"

    def __repr__(self) -> str:
        return self.__str__()
