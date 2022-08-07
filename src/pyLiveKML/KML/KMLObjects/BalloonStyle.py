from typing import Optional

from lxml import etree

from ..KML import DisplayMode
from .SubStyle import SubStyle


class BalloonStyle(SubStyle):
    """
    A KML 'BalloonStyle', per https://developers.google.com/kml/documentation/kmlreference#balloonstyle.  Specifies 
    how the description balloon of :class:`~pyLiveKML.KML.KMLObjects.Placemark` objects is drawn.

    :param Optional[str] text: The (optional) text to be displayed in the balloon.
    :param Optional[int] text_color: The (optional) color of the text to be displayed, in 32-bit ABGR format.
    :param Optional[int] bg_color: The (optional) background color of the balloon, in 32-bit ABGR format.
    :param Optional[DisplayMode] display_mode: The (optional) :class:`~pyLiveKML.KML.KML.DisplayMode` of the balloon.
    """

    @property
    def kml_type(self) -> str:
        """Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set the KML tag name to
        'BalloonStyle'"""
        return 'BalloonStyle'

    @property
    def bg_color(self) -> Optional[int]:
        """The background color of the balloon, in 32-bit ABGR format.
        """
        return self._bg_color

    @bg_color.setter
    def bg_color(self, value: Optional[int]):
        if self._bg_color != value:
            self._bg_color = value
            self.field_changed()

    @property
    def text_color(self) -> Optional[int]:
        """The color of the text in the balloon, in 32-bit ABGR format.
        """
        return self._text_color

    @text_color.setter
    def text_color(self, value: Optional[int]):
        if self._text_color != value:
            self._text_color = value
            self.field_changed()

    @property
    def text(self) -> Optional[str]:
        """The text displayed in the balloon.  Note that HTML markup, e.g. tables, is permissible.
        """
        return self._text

    @text.setter
    def text(self, value: Optional[str]):
        if self._text != value:
            self._text = value
            self.field_changed()

    @property
    def display_mode(self) -> Optional[DisplayMode]:
        """The balloon :class:`~pyLiveKML.KML.KML.DisplayMode`.
        """
        return self._display_mode

    @display_mode.setter
    def display_mode(self, value: Optional[DisplayMode]):
        if self._display_mode != value:
            self._display_mode = value
            self.field_changed()

    def build_kml(self, root: etree.Element, with_children=True):
        if self._bg_color is not None:
            etree.SubElement(root, 'bgColor').text = f'{self.bg_color:08x}'
        if self._text_color is not None:
            etree.SubElement(root, 'textColor').text = f'{self.text_color:08x}'
        if self._text is not None:
            etree.SubElement(root, 'text').text = self._text
        if self._display_mode is not None:
            etree.SubElement(root, 'displayMode').text = self._display_mode.value

    def __init__(
            self,
            text: Optional[str] = None,
            text_color: Optional[int] = None,
            bg_color: Optional[int] = None,
            display_mode: Optional[DisplayMode] = None
    ):
        SubStyle.__init__(self)
        self._text = text
        self._bg_color = bg_color
        self._text_color = text_color
        self._display_mode = display_mode

    def __str__(self):
        return f'{self.kml_type}'

    def __repr__(self):
        return self.__str__()
