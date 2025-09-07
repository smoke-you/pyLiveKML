"""StyleMap module."""

from lxml import etree  # type: ignore

from pyLiveKML.types.types import StyleStateEnum
from pyLiveKML.objects.Object import _BaseObject, _FieldDef, _DependentDef, _ChildDef
from pyLiveKML.objects.StyleSelector import StyleSelector
from pyLiveKML.objects.Style import Style


class _StyleMap_Pair(_BaseObject):
    """Hidden class for use by `StyleMap`."""

    _kml_tag = "Pair"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("key"),
        _FieldDef("style_url", "styleUrl"),
    )
    _kml_dependents = _BaseObject._kml_dependents + (_DependentDef("style"),)

    def __init__(self, key: StyleStateEnum, style_ref: str | Style):
        """_StyleMap_Pair instance constructor."""
        super().__init__()
        self.key = key
        self.style: Style | None
        self.style_url: str | None
        if isinstance(style_ref, Style):
            self.style = style_ref
            self.style_url = None
        else:
            self.style = None
            self.style_url = style_ref

    @property
    def value(self) -> str | Style:
        return self.style_url if self.style_url else self.style if self.style else ""

    @value.setter
    def value(self, value: str | Style) -> None:
        if isinstance(value, str):
            self.style = None
            self.style_url = value
        else:
            self.style = value
            self.style_url = None


class StyleMap(StyleSelector):
    """A KML `<StyleMap>` tag constructor.

    A `StyleMap` maps between two different `Style`s. Typically a `StyleMap` is used to
    provide separate normal and highlighted styles for a `Placemark`, so that the
    highlighted version appears when the user mouses over the icon in Google Earth.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#stylemap

    Parameters
    ----------
    normal_style_ref : str | Style
        The "normal" style, displayed when the mouse **is not** hovering over the
        `Feature`.
    highlight_style_ref : str | Style
        The "highlighted" style, displayed when the mouse **is** hovering over the
        `Feature`.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "StyleMap"
    _kml_children = StyleSelector._kml_children + (
        _ChildDef("_normal"),
        _ChildDef("_highlight"),
    )

    def __init__(
        self,
        normal_style_ref: str | Style,
        highlight_style_ref: str | Style,
    ):
        """StyleMap instance constructor."""
        super().__init__()
        self._normal = _StyleMap_Pair(StyleStateEnum.NORMAL, normal_style_ref)
        self._highlight = _StyleMap_Pair(StyleStateEnum.HIGHLIGHT, highlight_style_ref)

    @property
    def normal(self) -> str | Style:
        """Normal style reference or instance.

        Parameters
        ----------
        value : str | Style

        Returns
        -------
        str | Style

        """
        return self._normal.value

    @normal.setter
    def normal(self, value: str | Style) -> None:
        self._normal.value = value

    @property
    def highlight(self) -> str | Style:
        """Highlight style reference or instance.

        Parameters
        ----------
        value : str | Style

        Returns
        -------
        str | Style

        """
        return self._highlight.value

    @highlight.setter
    def highlight(self, value: str | Style) -> None:
        self._highlight.value = value
