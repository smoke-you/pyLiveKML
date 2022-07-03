from typing import Optional

from lxml import etree

from pyLiveKML.KML.KML import ListItemType, ItemIconMode
from pyLiveKML.KML.KMLObjects.SubStyle import SubStyle


class ListStyle(SubStyle):
    """
    A KML 'ListStyle', per https://developers.google.com/kml/documentation/kmlreference#liststyle.  Specifies
    how a :class:`~pyLiveKML.KML.KMLObjects.Feature` is displayed in GEP's user List View.

    :param Optional[ListItemType] list_item_type: The (optional) behaviour model for the list item.
    :param Optional[int] bg_color: The (optional) background color for the list item.
    :param Optional[ItemIconMode] item_icon_state: The (optional) icon state that will be displayed for the list item.
    :param Optional[str] item_icon_href: The (optional) URI for the image will be displayed for the list item.
    """

    @property
    def kml_type(self) -> str:
        """Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set the KML tag name to
        'ListStyle'"""
        return 'ListStyle'

    @property
    def list_item_type(self) -> Optional[ListItemType]:
        """The behaviour model for the list item.
        """
        return self._list_item_type

    @list_item_type.setter
    def list_item_type(self, value: Optional[ListItemType]):
        if self._list_item_type != value:
            self._list_item_type = value
            self.field_changed()

    @property
    def bg_color(self) -> Optional[int]:
        """The background color of the list item, as a 32-bit ABGR color.
        """
        return self._bg_color

    @bg_color.setter
    def bg_color(self, value: Optional[int]):
        if self._bg_color != value:
            self._bg_color = value
            self.field_changed()

    @property
    def item_icon_state(self) -> Optional[ItemIconMode]:
        """The icon state that will be displayed in the GEP user List View for the item.
        """
        return self._item_icon_state

    @item_icon_state.setter
    def item_icon_state(self, value: Optional[ItemIconMode]):
        if self._item_icon_state != value:
            self._item_icon_state = value
            self.field_changed()

    @property
    def item_icon_href(self) -> Optional[str]:
        """The URI for the image that will be displayed in the GEP user List View for the item.
        """
        return self._item_icon_href

    @item_icon_href.setter
    def item_icon_href(self, value: Optional[str]):
        if self._item_icon_href != value:
            self._item_icon_href = value
            self.field_changed()

    def build_kml(self, root: etree.Element, with_children=True):
        if self._list_item_type is not None:
            etree.SubElement(root, 'listItemType').text = self._list_item_type.value
        if self._bg_color is not None:
            etree.SubElement(root, 'bg_color').text = f'{self.bg_color:08x}'
        if self._item_icon_state is not None or self._item_icon_href is not None:
            item_icon = etree.SubElement(root, 'ItemIcon')
            if self._item_icon_state is not None:
                etree.SubElement(item_icon, 'state').text = self._item_icon_state.value
            if self._item_icon_href is not None:
                etree.SubElement(item_icon, 'href').text = self._item_icon_href

    def __init__(
            self,
            list_item_type: Optional[ListItemType] = None,
            bg_color: Optional[int] = None,
            item_icon_state: Optional[ItemIconMode] = None,
            item_icon_href: Optional[str] = None,
    ):
        SubStyle.__init__(self)
        self._list_item_type = list_item_type
        self._bg_color = bg_color
        self._item_icon_state = item_icon_state
        self._item_icon_href = item_icon_href

    def __str__(self):
        return f'{self.kml_type}'

    def __repr__(self):
        return self.__str__()
