"""Style module."""

from typing import Iterator

from lxml import etree  # type: ignore

from pyLiveKML.KML.KMLObjects.BalloonStyle import BalloonStyle
from pyLiveKML.KML.KMLObjects.IconStyle import IconStyle
from pyLiveKML.KML.KMLObjects.LabelStyle import LabelStyle
from pyLiveKML.KML.KMLObjects.LineStyle import LineStyle
from pyLiveKML.KML.KMLObjects.ListStyle import ListStyle
from pyLiveKML.KML.KMLObjects.Object import ObjectChild
from pyLiveKML.KML.KMLObjects.PolyStyle import PolyStyle
from pyLiveKML.KML.KMLObjects.StyleSelector import StyleSelector


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

    _kml_type = "Style"
    _direct_children = StyleSelector._direct_children + (
        "balloon_style",
        "icon_style",
        "label_style",
        "line_style",
        "list_style",
        "poly_style",
    )

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
        self.balloon_style = balloon_style
        self.icon_style = icon_style
        self.label_style = label_style
        self.line_style = line_style
        self.list_style = list_style
        self.poly_style = poly_style

    @property
    def children(self) -> Iterator[ObjectChild]:
        """The children of the instance.

        Overridden from :attr:`pyLiveKML.KML.KMLObjects.Object.Object.children` to yield
        the children of a :class:`~pyLiveKML.KML.KMLObjects.Style`, i.e. one or more
        :class:`~pyLiveKML.KML.KMLObjects.SubStyle` instances.
        """
        if self.balloon_style:
            yield ObjectChild(parent=self, child=self.balloon_style)
        if self.icon_style:
            yield ObjectChild(parent=self, child=self.icon_style)
        if self.label_style:
            yield ObjectChild(parent=self, child=self.label_style)
        if self.line_style:
            yield ObjectChild(parent=self, child=self.line_style)
        if self.list_style:
            yield ObjectChild(parent=self, child=self.list_style)
        if self.poly_style:
            yield ObjectChild(parent=self, child=self.poly_style)
