"""ColorStyle module."""

from abc import ABC
from typing import cast

from pyLiveKML.KML import ColorModeEnum
from pyLiveKML.KML._BaseObject import _FieldDef, NoParse, ColorParse, DumpDirect
from pyLiveKML.KML.GeoColor import GeoColor
from pyLiveKML.KMLObjects.SubStyle import SubStyle


class ColorStyle(SubStyle, ABC):
    """A KML 'ColorStyle', per https://developers.google.com/kml/documentation/kmlreference#colorstyle.

    ColorStyle is the abstract base class for a subset of the specific sub-styles that
    are optionally included in :class:`~pyLiveKML.KMLObjects.Style` objects, and
    that act to apply a color, typically (but not exclusively) to
    :class:`~pyLiveKML.KMLObjects.Feature` objects.

    :param int|None color: The (optional) color, in ABGR format, that will be applied by GEP if the
        :attr:`color_mode` is :attr:`~pyLiveKML.KML.KML.ColorMode.NORMAL`.
    :param ColorMode|None color_mode: The (optional) :class:`~pyLiveKML.KML.KML.ColorMode` that will be used by
        GEP to determine the displayed color.

    :var int|None color: The (optional) color, in ABGR format, that will be applied by GEP if the
        :attr:`color_mode` is :attr:`~pyLiveKML.KML.KML.ColorMode.NORMAL`.
    :var ColorMode|None color_mode: The (optional) :class:`~pyLiveKML.KML.KML.ColorMode` that will be used by GEP
        to determine the displayed color.
    """

    _kml_fields: tuple[_FieldDef, ...] = SubStyle._kml_fields + (
        _FieldDef("color", parser=ColorParse),
        _FieldDef("color_mode", "colorMode"),
    )

    def __init__(
        self,
        color: GeoColor | int | None = None,
        color_mode: ColorModeEnum | None = None,
    ):
        """ColorStyle instance constructor."""
        SubStyle.__init__(self)
        ABC.__init__(self)
        self.color_mode = color_mode
        self.color = GeoColor(color) if isinstance(color, int) else color
