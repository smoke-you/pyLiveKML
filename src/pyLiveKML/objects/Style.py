"""Style module."""

from typing import Any

from lxml import etree  # type: ignore

from pyLiveKML.objects.BalloonStyle import BalloonStyle
from pyLiveKML.objects.IconStyle import IconStyle
from pyLiveKML.objects.LabelStyle import LabelStyle
from pyLiveKML.objects.LineStyle import LineStyle
from pyLiveKML.objects.ListStyle import ListStyle
from pyLiveKML.objects.Object import _ChildDef
from pyLiveKML.objects.PolyStyle import PolyStyle
from pyLiveKML.objects.StyleSelector import StyleSelector
from pyLiveKML.objects.SubStyle import SubStyle


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
    *args | SubStyle
        Any number of positional `SubStyle` arguments. They will be assigned to the
        attribute of the correct type. There is only one instance of each attribute, so
        duplicates will overwrite any previous attribute value.
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
        *args: SubStyle,
        balloon_style: BalloonStyle | None = None,
        icon_style: IconStyle | None = None,
        label_style: LabelStyle | None = None,
        line_style: LineStyle | None = None,
        list_style: ListStyle | None = None,
        poly_style: PolyStyle | None = None,
    ):
        """Style instance constructor."""
        StyleSelector.__init__(self)
        self.balloon_style: BalloonStyle | None = None
        self.icon_style: IconStyle | None = None
        self.label_style: LabelStyle | None = None
        self.line_style: LineStyle | None = None
        self.list_style: ListStyle | None = None
        self.poly_style: PolyStyle | None = None
        for a in args:
            if isinstance(a, BalloonStyle):
                self.balloon_style = a
            elif isinstance(a, IconStyle):
                self.icon_style = a
            elif isinstance(a, LabelStyle):
                self.label_style = a
            elif isinstance(a, LineStyle):
                self.line_style = a
            elif isinstance(a, ListStyle):
                self.list_style = a
            elif isinstance(a, PolyStyle):
                self.poly_style = a
        if balloon_style:
            self.balloon_style = balloon_style
        if icon_style:
            self.icon_style = icon_style
        if label_style:
            self.label_style = label_style
        if line_style:
            self.line_style = line_style
        if list_style:
            self.list_style = list_style
        if poly_style:
            self.poly_style = poly_style
