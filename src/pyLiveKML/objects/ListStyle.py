"""ListStyle module."""

from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML.types import ItemIconModeEnum, ListItemTypeEnum, GeoColor
from pyLiveKML.objects.Object import _BaseObject, _ChildDef, _FieldDef, ColorParse
from pyLiveKML.objects.SubStyle import SubStyle


class ItemIcon(_BaseObject):
    """A KML `<ItemIcon>` tag constructor.

    Icon used in the List view that reflects the state of a `Folder` or `Link` fetch.
    Icons associated with the open and closed modes are used for `Folder`s and
    `NetworkLink`s. Icons associated with the error and fetching0, fetching1, and
    fetching2 modes are used for `NetworkLink`s.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-liststyle

    Parameters
    ----------
    icon_state : ItemIconModeEnum | None, default = None
    href : str | None, default = None

    Attributes
    ----------
    Same as parameters.

    """

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
    """A KML `<ListStyle>` tag constructor.

    Specifies how a `Feature` is displayed in the list view. The list view is a hierarchy
    of containers and children; in Google Earth, this is the "Places" panel.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#liststyle

    Parameters
    ----------
    list_item_type: ListItemTypeEnum | None, default = None
        Specifies how a Feature is displayed in the list view.
    bg_color: GeoColor | int | None, default = None
        Background color for the `Feature`'s `snippet`.
    icons: ItemIcon | Iterable[ItemIcon] | None, default = None
        Mappings between the state of the list item, and the icon to be displayed in the
        "Places" panel.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "ListStyle"
    _kml_fields = SubStyle._kml_fields + (
        _FieldDef("list_item_type", "listItemType"),
        _FieldDef("bg_color", "bgColor", ColorParse),
    )
    _kml_children = SubStyle._kml_children + (_ChildDef("icons"),)

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
        """Retrieve a generator over the `icons` of this `ListStyle`.

        If the property setter is called, replaces the current list of icons with
        those provided.

        Parameters
        ----------
        value : ItemIcon | Iterable[ItemIcon] | None
            The new icons for the `ListStyle`.

        :returns: A generator over the `icons` of the `ListStyle`.
        :rtype: Iterator[ItemIcon]

        """
        yield from self._icons

    @icons.setter
    def icons(self, value: ItemIcon | Iterable[ItemIcon] | None) -> None:
        self._icons.clear()
        if value is not None:
            if isinstance(value, ItemIcon):
                self._icons.append(value)
            else:
                self._icons.extend(value)
