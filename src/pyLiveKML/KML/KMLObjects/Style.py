"""Style module."""

from typing import Iterator

from lxml import etree  # type: ignore

from pyLiveKML.KML.KMLObjects.BalloonStyle import BalloonStyle
from pyLiveKML.KML.KMLObjects.IconStyle import IconStyle
from pyLiveKML.KML.KMLObjects.LabelStyle import LabelStyle
from pyLiveKML.KML.KMLObjects.LineStyle import LineStyle
from pyLiveKML.KML.KMLObjects.ListStyle import ListStyle
from pyLiveKML.KML.KMLObjects.PolyStyle import PolyStyle
from pyLiveKML.KML.KMLObjects.StyleSelector import StyleSelector
from pyLiveKML.KML.KMLObjects.Object import ObjectChild


class Style(StyleSelector):
    """A KML 'Style', per https://developers.google.com/kml/documentation/kmlreference#style.
    
    A group of :class:`~pyLiveKML.KML.KMLObjects.SubStyle` objects that can be referenced 
    by its :attr:`id` or inserted in-line into a :class:`~pyLiveKML.KML.KMLObjects.Feature`.

    :param BalloonStyle|None balloon_style: An (optional) :class:`~pyLiveKML.KML.KMLObjects.BalloonStyle` to be
        embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`.
    :param IconStyle|None icon_style: An (optional) :class:`~pyLiveKML.KML.KMLObjects.IconStyle` to be
        embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`.
    :param LabelStyle|None label_style: An (optional) :class:`~pyLiveKML.KML.KMLObjects.LabelStyle` to be
        embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`.
    :param LineStyle|None line_style: An (optional) :class:`~pyLiveKML.KML.KMLObjects.LineStyle` to be
        embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`.
    :param ListStyle|None list_style: An (optional) :class:`~pyLiveKML.KML.KMLObjects.ListStyle` to be
        embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`.
    :param PolyStyle|None poly_style: An (optional) :class:`~pyLiveKML.KML.KMLObjects.PolyStyle` to be
        embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`.
    """

    def __init__(
        self,
        balloon_style: BalloonStyle | None = None,
        icon_style: IconStyle | None = None,
        label_style: LabelStyle | None = None,
        line_style: LineStyle | None = None,
        list_style: ListStyle | None = None,
        poly_style: PolyStyle | None = None,
    ):
        """Style instance constructor."""
        StyleSelector.__init__(self)
        self._balloon_style: BalloonStyle | None = balloon_style
        self._icon_style: IconStyle | None = icon_style
        self._label_style: LabelStyle | None = label_style
        self._line_style: LineStyle | None = line_style
        self._list_style: ListStyle | None = list_style
        self._poly_style: PolyStyle | None = poly_style

    @property
    def kml_type(self) -> str:
        """The class' KML type string.
        
        Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set 
        the KML tag name to 'Style'.
        """
        return "Style"

    @property
    def children(self) -> Iterator[ObjectChild]:
        """The children of the instance.
        
        Overridden from :attr:`pyLiveKML.KML.KMLObjects.Object.Object.children` to yield 
        the children of a :class:`~pyLiveKML.KML.KMLObjects.Style`, i.e. one or more 
        :class:`~pyLiveKML.KML.KMLObjects.SubStyle` instances.
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
    def balloon_style(self) -> BalloonStyle | None:
        """A :class:`~pyLiveKML.KML.KMLObjects.BalloonStyle` embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`."""
        return self._balloon_style

    @property
    def icon_style(self) -> IconStyle | None:
        """An :class:`~pyLiveKML.KML.KMLObjects.IconStyle` embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`."""
        return self._icon_style

    @property
    def label_style(self) -> LabelStyle | None:
        """A :class:`~pyLiveKML.KML.KMLObjects.LabelStyle` embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`."""
        return self._label_style

    @property
    def line_style(self) -> LineStyle | None:
        """A :class:`~pyLiveKML.KML.KMLObjects.LineStyle` embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`."""
        return self._line_style

    @property
    def list_style(self) -> ListStyle | None:
        """A :class:`~pyLiveKML.KML.KMLObjects.ListStyle` embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`."""
        return self._list_style

    @property
    def poly_style(self) -> PolyStyle | None:
        """A :class:`~pyLiveKML.KML.KMLObjects.PolyStyle` embedded in this :class:`~pyLiveKML.KML.KMLObjects.Style`."""
        return self._poly_style

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
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

    def __str__(self) -> str:
        """Return a string representation."""
        return f"{self.kml_type}"

    def __repr__(self) -> str:
        """Return a debug representation."""
        return self.__str__()
