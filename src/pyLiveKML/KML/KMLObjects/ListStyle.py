"""ListStyle module."""

from typing import Sequence

from lxml import etree  # type: ignore

from pyLiveKML.KML import ItemIconModeEnum, ListItemTypeEnum
from pyLiveKML.KML.GeoColor import GeoColor
from pyLiveKML.KML._BaseObject import (
    _BaseObject,
    _FieldDef,
    ColorParse,
    DumpDirect,
    NoParse,
)
from pyLiveKML.KML.KMLObjects.SubStyle import SubStyle


class ItemIcon(_BaseObject):
    """ItemIcon class definition."""

    _kml_tag = "ItemIcon"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("icon_state", NoParse, "state", DumpDirect),
        _FieldDef("href", NoParse, "href", DumpDirect),
    )

    def __init__(
        self,
        icon_state: ItemIconModeEnum | None = None,
        href: str | None = None,
    ):
        """ItemIcon instance constructor."""
        super().__init__()
        self.icon_state = icon_state
        self.href = href


class ListStyle(SubStyle):
    """A KML 'ListStyle', per https://developers.google.com/kml/documentation/kmlreference#liststyle.

    Specifies how a :class:`~pyLiveKML.KML.KMLObjects.Feature` is displayed in GEP's user List View.

    :param ListItemType|None list_item_type: The (optional) behaviour model for the list item.
    :param int|None bg_color: The (optional) background color for the list item.
    :param ItemIconMode|None item_icon_state: The (optional) icon state that will be displayed for the list item.
    :param str|None item_icon_href: The (optional) URI for the image will be displayed for the list item.
    """

    _kml_tag = "ListStyle"
    _kml_fields = SubStyle._kml_fields + (
        _FieldDef("list_item_type", NoParse, "listItemType", DumpDirect),
        _FieldDef("bg_color", ColorParse, "bgColor", DumpDirect),
    )

    def __init__(
        self,
        list_item_type: ListItemTypeEnum | None = None,
        bg_color: GeoColor | int | None = None,
        icons: ItemIcon | Sequence[ItemIcon] | None = None,
    ):
        """ListStyle instance constructor."""
        SubStyle.__init__(self)
        self.list_item_type = list_item_type
        self.bg_color = bg_color
        self.icons = list[ItemIcon]()
        if icons is not None:
            if isinstance(icons, ItemIcon):
                self.icons.append(icons)
            else:
                self.icons.extend(icons)

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        for i in self.icons:
            i.build_kml(etree.SubElement(root, i._kml_tag), False)
