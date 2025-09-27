# pyLiveKML: A python library that streams geospatial data using the KML protocol.
# Copyright (C) 2022 smoke-you

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""ExtendedData module."""

from abc import ABC
from typing import Any, Iterable, Iterator

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import (
    _BaseObject,
    _DependentDef,
    _FieldDef,
    _RootAttribDef,
)


class _ExtendedDataItem(_BaseObject, ABC):
    """Private base class for `ExtendedData` items."""

    def __init__(self, **kwargs: Any) -> None:
        """_ExtendedDataItem instance constructor."""
        _BaseObject.__init__(self, **kwargs)
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
    _kml_root_attribs = _BaseObject._kml_root_attribs + (
        _RootAttribDef("name", "name"),
    )
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("display_name", "displayName"),
        _FieldDef("value"),
    )

    def __init__(
        self,
        name: str,
        display_name: str | None,
        value: str | None,
        **kwargs: Any,
    ) -> None:
        """DataItem instance constructor."""
        _ExtendedDataItem.__init__(self, **kwargs)
        self.name = name
        self.display_name = display_name
        self.value = value


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
    _kml_root_attribs = _BaseObject._kml_root_attribs + (
        _RootAttribDef("schemaUrl", "schema_ref"),
    )

    def __init__(
        self,
        schema_ref: str,
        data: dict[str, str],
        **kwargs: Any,
    ) -> None:
        """SchemaDataItem instance constructor."""
        _ExtendedDataItem.__init__(self, **kwargs)
        self.schema_ref = schema_ref
        self.data = data

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
        **kwargs: Any,
    ) -> None:
        """Construct Schema instances."""
        _BaseObject.__init__(self, **kwargs)
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
