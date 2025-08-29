"""StyleMap module."""

import enum

from lxml import etree  # type: ignore

from pyLiveKML.KML import StyleStateEnum
from pyLiveKML.KML._BaseObject import _BaseObject, _FieldDef, DumpDirect, NoParse
from pyLiveKML.KML.KMLObjects.StyleSelector import StyleSelector


class _StyleMap_Pair(_BaseObject):
    """Hidden class for use by `StyleMap`."""

    _kml_type = "Pair"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("key", NoParse, "key", DumpDirect),
        _FieldDef("style_url", NoParse, "styleUrl", DumpDirect),
    )

    def __init__(self, key: StyleStateEnum, style_url: str):
        """_StyleMap_Pair instance constructor."""
        super().__init__()
        self.key = key
        self.style_url = style_url


class StyleMap(StyleSelector):
    """A KML 'StyleMap', per https://developers.google.com/kml/documentation/kmlreference#stylemap.

    Maps between two different :class:`~pyLiveKML.KML.KMLObjects.Style` objects for the
    :attr:`~pyLiveKML.KML.KML.StyleState.NORMAL` and :attr:`~pyLiveKML.KML.KML.StyleState.HIGHLIGHT`
    states of a :class:`~pyLiveKML.KML.KMLObjects.Feature` when it is displayed in GEP. The child
    :class:`~pyLiveKML.KML.KMLObjects.Style` objects may be referenced by URI, or in-line in the
    :class:`~pyLiveKML.KML.KMLObjects.StyleMap`.

    :param str|None normal_style_url: An (optional) URI reference for a :class:`~pyLiveKML.KML.KMLObjects.Style`
        to be employed in :attr:`~pyLiveKML.KML.KML.StyleState.NORMAL` display mode.
    :param Style|None normal_style: An (optional) inline :class:`~pyLiveKML.KML.KMLObjects.Style` to be employed
        in :attr:`~pyLiveKML.KML.KML.StyleState.NORMAL` display mode.
    :param str|None highlight_style_url: An (optional) URI reference for a
        :class:`~pyLiveKML.KML.KMLObjects.Style` to be employed in :attr:`~pyLiveKML.KML.KML.StyleState.HIGHLIGHT`
        display mode.
    :param Style|None highlight_style: An (optional) inline :class:`~pyLiveKML.KML.KMLObjects.Style` to be
        employed in :attr:`~pyLiveKML.KML.KML.StyleState.HIGHLIGHT` display mode.

    :note: It is both possible and reasonable to assign both a :attr:`styleUrl` and a
        :class:`~pyLiveKML.KML.KMLObjects.Style` to either or both of the :attr:`~pyLiveKML.KML.KML.StyleState.NORMAL`
        and :attr:`~pyLiveKML.KML.KML.StyleState.HIGHLIGHT` states. Per the rules discussed at
        https://developers.google.com/kml/documentation/kmlreference#feature, an inline
        :class:`~pyLiveKML.KML.KMLObjects.Style` will override a URI-referenced
        :class:`~pyLiveKML.KML.KMLObjects.Style`.
    """

    _kml_type = "StyleMap"
    _direct_children = StyleSelector._direct_children + ("normal", "highlight")

    def __init__(
        self,
        normal_style_url: str,
        highlight_style_url: str,
    ):
        """StyleMap instance constructor."""
        super().__init__()
        self.normal = _StyleMap_Pair(StyleStateEnum.NORMAL, normal_style_url)
        self.highlight = _StyleMap_Pair(StyleStateEnum.HIGHLIGHT, highlight_style_url)
