"""Style module."""

from typing import Iterator

from lxml import etree  # type: ignore

from pyLiveKML.objects.BalloonStyle import BalloonStyle
from pyLiveKML.objects.IconStyle import IconStyle
from pyLiveKML.objects.LabelStyle import LabelStyle
from pyLiveKML.objects.LineStyle import LineStyle
from pyLiveKML.objects.ListStyle import ListStyle
from pyLiveKML.objects.Object import ObjectChild, _ChildDef
from pyLiveKML.objects.PolyStyle import PolyStyle
from pyLiveKML.objects.StyleSelector import StyleSelector


class Style(StyleSelector):
    """A KML `<Style>` tag constructor.

    A `Style` defines an addressable style group that can be referenced by `StyleMap`s
    and `Feature`s. `Style`s affect how `Geometry` is presented in the 3D viewer and how
    `Feature`s appear in the "Places" panel of the List view. Shared styles are collected
    in a `Document` and must have an `id` defined for them so that they can be referenced
    by the individual `Feature`s that use them.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#style

    Parameters
    ----------
    balloon_style : BalloonStyle | None, default = None
    icon_style : IconStyle | None, default = None
    label_style : LabelStyle | None, default = None
    line_style : LineStyle | None, default = None
    list_style : ListStyle | None, default = None
    poly_style : PolyStyle | None, default = None

    Attributes
    ----------
    Same as parameters.

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
