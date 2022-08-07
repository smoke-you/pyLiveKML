from abc import ABC
from typing import Optional

from ..KML import ColorMode
from .SubStyle import SubStyle


class ColorStyle(SubStyle, ABC):
    """A KML 'ColorStyle', per https://developers.google.com/kml/documentation/kmlreference#colorstyle.  The
    ColorStyle is the abstract base class for a subset of the specific sub-styles that are optionally included
    in :class:`~pyLiveKML.KML.KMLObjects.Style` objects, and that act to apply a color, typically (but not exclusively)
    to :class:`~pyLiveKML.KML.KMLObjects.Feature` objects.

    :param Optional[int] color: The (optional) color, in ABGR format, that will be applied by GEP if the
        :attr:`color_mode` is :attr:`~pyLiveKML.KML.KML.ColorMode.NORMAL`.
    :param Optional[ColorMode] color_mode: The (optional) :class:`~pyLiveKML.KML.KML.ColorMode` that will be used by
        GEP to determine the displayed color.

    :var Optional[int] color: The (optional) color, in ABGR format, that will be applied by GEP if the
        :attr:`color_mode` is :attr:`~pyLiveKML.KML.KML.ColorMode.NORMAL`.
    :var Optional[ColorMode] color_mode: The (optional) :class:`~pyLiveKML.KML.KML.ColorMode` that will be used by GEP
        to determine the displayed color.
    """
    @property
    def color(self) -> Optional[int]:
        """Color, in 32-bit ABGR format (yes, the order is correct).
        """
        return self._color

    @color.setter
    def color(self, value: Optional[int]):
        val = None if value is None else 0 if value <= 0 else 0xffffffff if value >= 0xffffffff else value
        if self._color != val:
            self._color = val
            self.field_changed()

    @property
    def color_mode(self) -> Optional[ColorMode]:
        """The :class:`~pyLiveKML.KML.KML.ColorMode` that will be used by GEP to determine the displayed color.
        """
        return self._color_mode

    @color_mode.setter
    def color_mode(self, value: Optional[ColorMode]):
        if self._color_mode != value:
            self._color_mode = value
            self.field_changed()

    def __init__(
            self,
            color: Optional[int] = None,
            color_mode: Optional[ColorMode] = None
    ):
        SubStyle.__init__(self)
        ABC.__init__(self)
        self._color = None
        self.color = color
        self._color_mode = color_mode
