from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import ListItemType, ItemIconMode
from pyLiveKML.KML.KMLObjects.SubStyle import SubStyle


class ListStyle(SubStyle):
    """
    A KML 'ListStyle', per https://developers.google.com/kml/documentation/kmlreference#liststyle.  Specifies
    how a :class:`~pyLiveKML.KML.KMLObjects.Feature` is displayed in GEP's user List View.

    :param ListItemType|None list_item_type: The (optional) behaviour model for the list item.
    :param int|None bg_color: The (optional) background color for the list item.
    :param ItemIconMode|None item_icon_state: The (optional) icon state that will be displayed for the list item.
    :param str|None item_icon_href: The (optional) URI for the image will be displayed for the list item.
    """

    def __init__(
        self,
        list_item_type: ListItemType | None = None,
        bg_color: int | None = None,
        item_icon_state: ItemIconMode | None = None,
        item_icon_href: str | None = None,
    ):
        SubStyle.__init__(self)
        self._list_item_type: ListItemType | None = list_item_type
        self._bg_color: int | None = bg_color
        self._item_icon_state: ItemIconMode | None = item_icon_state
        self._item_icon_href: str | None = item_icon_href

    @property
    def kml_type(self) -> str:
        """Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set the KML tag name to
        'ListStyle'"""
        return "ListStyle"

    @property
    def list_item_type(self) -> ListItemType | None:
        """The behaviour model for the list item."""
        return self._list_item_type

    @list_item_type.setter
    def list_item_type(self, value: ListItemType | None) -> None:
        if self._list_item_type != value:
            self._list_item_type = value
            self.field_changed()

    @property
    def bg_color(self) -> int | None:
        """The background color of the list item, as a 32-bit ABGR color."""
        return self._bg_color

    @bg_color.setter
    def bg_color(self, value: int | None) -> None:
        if self._bg_color != value:
            self._bg_color = value
            self.field_changed()

    @property
    def item_icon_state(self) -> ItemIconMode | None:
        """The icon state that will be displayed in the GEP user List View for the item."""
        return self._item_icon_state

    @item_icon_state.setter
    def item_icon_state(self, value: ItemIconMode | None) -> None:
        if self._item_icon_state != value:
            self._item_icon_state = value
            self.field_changed()

    @property
    def item_icon_href(self) -> str | None:
        """The URI for the image that will be displayed in the GEP user List View for the item."""
        return self._item_icon_href

    @item_icon_href.setter
    def item_icon_href(self, value: str | None) -> None:
        if self._item_icon_href != value:
            self._item_icon_href = value
            self.field_changed()

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        if self._list_item_type is not None:
            etree.SubElement(root, "listItemType").text = self._list_item_type.value
        if self._bg_color is not None:
            etree.SubElement(root, "bg_color").text = f"{self.bg_color:08x}"
        if self._item_icon_state is not None or self._item_icon_href is not None:
            item_icon = etree.SubElement(root, "ItemIcon")
            if self._item_icon_state is not None:
                etree.SubElement(item_icon, "state").text = self._item_icon_state.value
            if self._item_icon_href is not None:
                etree.SubElement(item_icon, "href").text = self._item_icon_href

    def __str__(self) -> str:
        return f"{self.kml_type}"

    def __repr__(self) -> str:
        return self.__str__()
