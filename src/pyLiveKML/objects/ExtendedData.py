"""ExtendedData module."""

from abc import ABC
from typing import Iterable, Iterator

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import (
    _BaseObject,
    _DependentDef,
    _FieldDef,
)


class _ExtendedDataItem(_BaseObject, ABC):
    """Private base class for `ExtendedData` items."""

    def __init__(self) -> None:
        """_ExtendedDataItem instance constructor."""
        _BaseObject.__init__(self)
        ABC.__init__(self)


class DataItem(_ExtendedDataItem):
    """A KML `Data` tag constructor.

    Used only by `ExtendedData`.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#extendeddata
    * https://developers.google.com/kml/documentation/extendeddata

    Parameters
    ----------
    name : str
    display_name : str | None, default = None
    value : str | None, default = None

    Attributes
    ----------
    Same as parameters

    """

    _kml_tag = "Data"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("display_name", "displayName"),
        _FieldDef("value"),
    )

    def __init__(
        self,
        name: str,
        display_name: str | None,
        value: str | None,
    ) -> None:
        """DataItem instance constructor."""
        super().__init__()
        self.name = name
        self.display_name = display_name
        self.value = value

    def construct_kml(
        self, with_children: bool = True, with_dependents: bool = True
    ) -> etree.Element:
        """Override `construct_kml` for fine control."""
        root = etree.Element(self._kml_tag, attrib={"name": self.name})
        self.build_kml(root, with_children, with_dependents)
        return root


class SchemaDataItem(_ExtendedDataItem):
    """A KML `SchemaData` tag constructor.

    Used only by `ExtendedData`.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#extendeddata
    * https://developers.google.com/kml/documentation/extendeddata

    Parameters
    ----------
    schema_ref : str
        A # reference to a `Schema` `id` in the hosting `Document`.
    data : dict[str, str]
        For each key-value pair in `data`:
        * The key must be a `SimpleField` of that name in the `Schema` referenced by
        `schema_ref`.
        * The value will be displayed using the `SimpleField` reference by the key.

    Attributes
    ----------
    Same as parameters

    """

    _kml_tag = "SchemaData"

    def __init__(
        self,
        schema_ref: str,
        data: dict[str, str],
    ) -> None:
        """SchemaDataItem instance constructor."""
        super().__init__()
        self.schema_ref = schema_ref
        self.data = data

    def construct_kml(
        self, with_children: bool = True, with_dependents: bool = True
    ) -> etree.Element:
        """Override `construct_kml` for fine control."""
        root = etree.Element(self._kml_tag, attrib={"name": self.schema_ref})
        self.build_kml(root, with_children, with_dependents)
        return root

    def build_kml(
        self,
        root: etree.Element,
        with_children: bool = True,
        with_dependents: bool = True,
    ) -> None:
        """Override `build_kml` for fine control."""
        for k, v in self.data.items():
            etree.SubElement(root, "SimpleData", attrib={"name": k}).text = v


class ExtendedData(_BaseObject):
    """A KML `<ExtendedData>` tag constructor.

    The `ExtendedData` class offers three techniques for adding custom data to a KML
    `Feature`. These techniques are:

    * Adding untyped data/value pairs using `DataItem` instances (basic).
    * Declaring new typed fields using `Schema` and then instancing them using
    `SchemaDataItem` instances (advanced).
    * Referring to XML elements defined in other namespaces by referencing the external
    namespace within the KML file (basic). **This method is *not* supported by pyLiveKML**.

    These techniques can be combined within a single KML file or `Feature` for different
    pieces of data.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#extendeddata
    * https://developers.google.com/kml/documentation/extendeddata

    Parameters
    ----------
    items : _ExtendedDataItem | Iterable[_ExtendedDataItem] | None, default = None
        The items to be included in the `ExtendedData`. In practice, these may be any
        combination of `DataItem` and `SchemaDataItem` instances, in any order.

    Attributes
    ----------
    Same as parameters

    """

    _kml_tag = "ExtendedData"
    _kml_dependents = _BaseObject._kml_dependents + (_DependentDef("items"),)

    def __init__(
        self,
        items: _ExtendedDataItem | Iterable[_ExtendedDataItem] | None = None,
    ) -> None:
        """Construct Schema instances."""
        super().__init__()
        self._items = list[_ExtendedDataItem]()
        self.items = items

    @property
    def items(self) -> Iterator[_ExtendedDataItem]:
        """Generator over items."""
        yield from self._items

    @items.setter
    def items(
        self, value: _ExtendedDataItem | Iterable[_ExtendedDataItem] | None
    ) -> None:
        self._items.clear()
        if value is not None:
            if isinstance(value, _ExtendedDataItem):
                self._items.append(value)
            else:
                self._items.extend(value)
