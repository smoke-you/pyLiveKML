"""ColorStyle module."""

from abc import ABC

from pyLiveKML.KML.KML import ColorMode
from pyLiveKML.KML.KMLObjects.SubStyle import SubStyle


class ColorStyle(SubStyle, ABC):
    """A KML 'ColorStyle', per https://developers.google.com/kml/documentation/kmlreference#colorstyle.

    ColorStyle is the abstract base class for a subset of the specific sub-styles that
    are optionally included in :class:`~pyLiveKML.KML.KMLObjects.Style` objects, and
    that act to apply a color, typically (but not exclusively) to
    :class:`~pyLiveKML.KML.KMLObjects.Feature` objects.

    :param int|None color: The (optional) color, in ABGR format, that will be applied by GEP if the
        :attr:`color_mode` is :attr:`~pyLiveKML.KML.KML.ColorMode.NORMAL`.
    :param ColorMode|None color_mode: The (optional) :class:`~pyLiveKML.KML.KML.ColorMode` that will be used by
        GEP to determine the displayed color.

    :var int|None color: The (optional) color, in ABGR format, that will be applied by GEP if the
        :attr:`color_mode` is :attr:`~pyLiveKML.KML.KML.ColorMode.NORMAL`.
    :var ColorMode|None color_mode: The (optional) :class:`~pyLiveKML.KML.KML.ColorMode` that will be used by GEP
        to determine the displayed color.
    """

    _kml_type = "ColorStyle"

    def __init__(self, color: int | None = None, color_mode: ColorMode | None = None):
        """ColorStyle instance constructor."""
        SubStyle.__init__(self)
        ABC.__init__(self)
        self._color: int | None = None
        self.color = color
        self._color_mode: ColorMode | None = color_mode

    @property
    def color(self) -> int | None:
        """Color, in 32-bit ABGR format (yes, the order is correct)."""
        return self._color

    @color.setter
    def color(self, value: int | None) -> None:
        val = (
            None
            if value is None
            else 0 if value <= 0 else 0xFFFFFFFF if value >= 0xFFFFFFFF else value
        )
        if self._color != val:
            self._color = val
            self.field_changed()

    @property
    def color_mode(self) -> ColorMode | None:
        """The :class:`~pyLiveKML.KML.KML.ColorMode` that will be used by GEP to determine the displayed color."""
        return self._color_mode

    @color_mode.setter
    def color_mode(self, value: ColorMode | None) -> None:
        if self._color_mode != value:
            self._color_mode = value
            self.field_changed()
