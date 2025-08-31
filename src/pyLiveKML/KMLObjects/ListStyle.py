"""ListStyle module."""

from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML.KML import ItemIconModeEnum, ListItemTypeEnum
from pyLiveKML.KML._BaseObject import _BaseObject, _FieldDef, ColorParse
from pyLiveKML.KML.GeoColor import GeoColor
from pyLiveKML.KMLObjects.Object import _ChildDef
from pyLiveKML.KMLObjects.SubStyle import SubStyle


class ItemIcon(_BaseObject):
    """ItemIcon class definition."""

    _kml_tag = "ItemIcon"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("icon_state", "state"),
        _FieldDef("href"),
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

    Specifies how a :class:`~pyLiveKML.KMLObjects.Feature` is displayed in GEP's user List View.

    :param ListItemType|None list_item_type: The (optional) behaviour model for the list item.
    :param int|None bg_color: The (optional) background color for the list item.
    :param ItemIconMode|None item_icon_state: The (optional) icon state that will be displayed for the list item.
    :param str|None item_icon_href: The (optional) URI for the image will be displayed for the list item.
    """

    _kml_tag = "ListStyle"
    _kml_fields = SubStyle._kml_fields + (
        _FieldDef("list_item_type", "listItemType"),
        _FieldDef("bg_color", "bgColor", ColorParse),
    )
    _direct_children = SubStyle._direct_children + (_ChildDef("icons", None, False),)

    def __init__(
        self,
        list_item_type: ListItemTypeEnum | None = None,
        bg_color: GeoColor | int | None = None,
        icons: ItemIcon | Iterable[ItemIcon] | None = None,
    ):
        """ListStyle instance constructor."""
        SubStyle.__init__(self)
        self.list_item_type = list_item_type
        self.bg_color = bg_color
        self._icons = list[ItemIcon]()
        self.icons = icons

    @property
    def icons(self) -> Iterable[ItemIcon]:
        """Generator across icon instances."""
        yield from self._icons

    @icons.setter
    def icons(self, value: ItemIcon | Iterable[ItemIcon] | None) -> None:
        self._icons.clear()
        if value is not None:
            if isinstance(value, ItemIcon):
                self._icons.append(value)
            else:
                self._icons.extend(value)
