"""BalloonStyle module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import DisplayMode
from pyLiveKML.KML.KMLObjects.SubStyle import SubStyle


class BalloonStyle(SubStyle):
    """A KML 'BalloonStyle', per https://developers.google.com/kml/documentation/kmlreference#balloonstyle.

    Specifies how the description balloon of
    :class:`~pyLiveKML.KML.KMLObjects.Placemark` objects is drawn.

    :param str|None text: The (optional) text to be displayed in the balloon.
    :param int|None text_color: The (optional) color of the text to be displayed, in 32-bit ABGR format.
    :param int|None bg_color: The (optional) background color of the balloon, in 32-bit ABGR format.
    :param DisplayMode|None display_mode: The (optional) :class:`~pyLiveKML.KML.KML.DisplayMode` of the balloon.
    """

    _kml_type = "BalloonStyle"

    def __init__(
        self,
        text: str | None = None,
        text_color: int | None = None,
        bg_color: int | None = None,
        display_mode: DisplayMode | None = None,
    ):
        """BalloonStyle instance constructor."""
        SubStyle.__init__(self)
        self._text: str | None = text
        self._bg_color: int | None = bg_color
        self._text_color: int | None = text_color
        self._display_mode: DisplayMode | None = display_mode

    @property
    def bg_color(self) -> int | None:
        """The background color of the balloon, in 32-bit ABGR format."""
        return self._bg_color

    @bg_color.setter
    def bg_color(self, value: int | None) -> None:
        if self._bg_color != value:
            self._bg_color = value
            self.field_changed()

    @property
    def text_color(self) -> int | None:
        """The color of the text in the balloon, in 32-bit ABGR format."""
        return self._text_color

    @text_color.setter
    def text_color(self, value: int | None) -> None:
        if self._text_color != value:
            self._text_color = value
            self.field_changed()

    @property
    def text(self) -> str | None:
        """The text displayed in the balloon.

        :note: HTML markup, e.g. tables, is permissible.
        """
        return self._text

    @text.setter
    def text(self, value: str | None) -> None:
        if self._text != value:
            self._text = value
            self.field_changed()

    @property
    def display_mode(self) -> DisplayMode | None:
        """The balloon :class:`~pyLiveKML.KML.KML.DisplayMode`."""
        return self._display_mode

    @display_mode.setter
    def display_mode(self, value: DisplayMode | None) -> None:
        if self._display_mode != value:
            self._display_mode = value
            self.field_changed()

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        if self._bg_color is not None:
            etree.SubElement(root, "bgColor").text = f"{self.bg_color:08x}"
        if self._text_color is not None:
            etree.SubElement(root, "textColor").text = f"{self.text_color:08x}"
        if self._text is not None:
            etree.SubElement(root, "text").text = self._text
        if self._display_mode is not None:
            etree.SubElement(root, "displayMode").text = self._display_mode.value

    def __str__(self) -> str:
        """Return a string representation."""
        return f"{self.kml_type}"

    def __repr__(self) -> str:
        """Return a debug representation."""
        return self.__str__()
