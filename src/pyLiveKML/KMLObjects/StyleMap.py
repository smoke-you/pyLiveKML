"""StyleMap module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML import StyleStateEnum
from pyLiveKML.KML.Object import _BaseObject, _FieldDef
from pyLiveKML.KML.Object import _ChildDef
from pyLiveKML.KMLObjects.StyleSelector import StyleSelector
from pyLiveKML.KMLObjects.Style import Style


class _StyleMap_Pair(_BaseObject):
    """Hidden class for use by `StyleMap`."""

    _kml_tag = "Pair"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("key"),
        _FieldDef("style_url", "styleUrl"),
    )

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
    def value(self) -> str | Style | None:
        return self.style_url if self.style_url else self.style

    @value.setter
    def value(self, value: str | Style | None) -> None:
        if value is None:
            self.style = None
            self.style_url = None
        elif isinstance(value, str):
            self.style = None
            self.style_url = value
        else:
            self.style = value
            self.style_url = None

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        if self.style is not None:
            root.append(self.style.construct_kml())


class StyleMap(StyleSelector):
    """A KML 'StyleMap', per https://developers.google.com/kml/documentation/kmlreference#stylemap.

    Maps between two different :class:`~pyLiveKML.KMLObjects.Style` objects for the
    :attr:`~pyLiveKML.KML.KML.StyleState.NORMAL` and :attr:`~pyLiveKML.KML.KML.StyleState.HIGHLIGHT`
    states of a :class:`~pyLiveKML.KMLObjects.Feature` when it is displayed in GEP. The child
    :class:`~pyLiveKML.KMLObjects.Style` objects may be referenced by URI, or in-line in the
    :class:`~pyLiveKML.KMLObjects.StyleMap`.

    :param str|None normal_style_url: An (optional) URI reference for a :class:`~pyLiveKML.KMLObjects.Style`
        to be employed in :attr:`~pyLiveKML.KML.KML.StyleState.NORMAL` display mode.
    :param Style|None normal_style: An (optional) inline :class:`~pyLiveKML.KMLObjects.Style` to be employed
        in :attr:`~pyLiveKML.KML.KML.StyleState.NORMAL` display mode.
    :param str|None highlight_style_url: An (optional) URI reference for a
        :class:`~pyLiveKML.KMLObjects.Style` to be employed in :attr:`~pyLiveKML.KML.KML.StyleState.HIGHLIGHT`
        display mode.
    :param Style|None highlight_style: An (optional) inline :class:`~pyLiveKML.KMLObjects.Style` to be
        employed in :attr:`~pyLiveKML.KML.KML.StyleState.HIGHLIGHT` display mode.

    :note: It is both possible and reasonable to assign both a :attr:`styleUrl` and a
        :class:`~pyLiveKML.KMLObjects.Style` to either or both of the :attr:`~pyLiveKML.KML.KML.StyleState.NORMAL`
        and :attr:`~pyLiveKML.KML.KML.StyleState.HIGHLIGHT` states. Per the rules discussed at
        https://developers.google.com/kml/documentation/kmlreference#feature, an inline
        :class:`~pyLiveKML.KMLObjects.Style` will override a URI-referenced
        :class:`~pyLiveKML.KMLObjects.Style`.
    """

    _kml_tag = "StyleMap"
    _direct_children = StyleSelector._direct_children + (
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
    def normal(self) -> str | Style | None:
        """Normal style reference or instance."""
        return self._normal.value

    @normal.setter
    def normal(self, value: str | Style | None) -> None:
        self._normal.value = value

    @property
    def highlight(self) -> str | Style | None:
        """Highlight style reference or instance."""
        return self._highlight.value

    @highlight.setter
    def highlight(self, value: str | Style | None) -> None:
        self._highlight.value = value
