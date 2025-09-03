"""Style module."""

from typing import Iterator

from lxml import etree  # type: ignore

from pyLiveKML.KMLObjects.BalloonStyle import BalloonStyle
from pyLiveKML.KMLObjects.IconStyle import IconStyle
from pyLiveKML.KMLObjects.LabelStyle import LabelStyle
from pyLiveKML.KMLObjects.LineStyle import LineStyle
from pyLiveKML.KMLObjects.ListStyle import ListStyle
from pyLiveKML.KML.Object import ObjectChild, _ChildDef
from pyLiveKML.KMLObjects.PolyStyle import PolyStyle
from pyLiveKML.KMLObjects.StyleSelector import StyleSelector


class Style(StyleSelector):
    """A KML 'Style', per https://developers.google.com/kml/documentation/kmlreference#style.

    A group of :class:`~pyLiveKML.KMLObjects.SubStyle` objects that can be referenced
    by its :attr:`id` or inserted in-line into a :class:`~pyLiveKML.KMLObjects.Feature`.

    :param BalloonStyle|None balloon_style: An (optional) :class:`~pyLiveKML.KMLObjects.BalloonStyle` to be
        embedded in this :class:`~pyLiveKML.KMLObjects.Style`.
    :param IconStyle|None icon_style: An (optional) :class:`~pyLiveKML.KMLObjects.IconStyle` to be
        embedded in this :class:`~pyLiveKML.KMLObjects.Style`.
    :param LabelStyle|None label_style: An (optional) :class:`~pyLiveKML.KMLObjects.LabelStyle` to be
        embedded in this :class:`~pyLiveKML.KMLObjects.Style`.
    :param LineStyle|None line_style: An (optional) :class:`~pyLiveKML.KMLObjects.LineStyle` to be
        embedded in this :class:`~pyLiveKML.KMLObjects.Style`.
    :param ListStyle|None list_style: An (optional) :class:`~pyLiveKML.KMLObjects.ListStyle` to be
        embedded in this :class:`~pyLiveKML.KMLObjects.Style`.
    :param PolyStyle|None poly_style: An (optional) :class:`~pyLiveKML.KMLObjects.PolyStyle` to be
        embedded in this :class:`~pyLiveKML.KMLObjects.Style`.
    """

    _kml_tag = "Style"
    _kml_children = StyleSelector._kml_children + (
        _ChildDef("balloon_style"),
        _ChildDef("icon_style"),
        _ChildDef("label_style"),
        _ChildDef("line_style"),
        _ChildDef("list_style"),
        _ChildDef("poly_style"),
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
