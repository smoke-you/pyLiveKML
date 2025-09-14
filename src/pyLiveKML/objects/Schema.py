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

"""Schema module."""

from typing import Iterable, Iterator

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import (
    _BaseObject,
    _DependentDef,
    _FieldDef,
    _RootAttribDef,
    Object,
)


class SimpleField(_BaseObject):
    """SimpleField class.

    `Schema` instances contain a collection of `SimpleField` instances.
    """

    _kml_tag = "SimpleField"
    _kml_fields = _BaseObject._kml_fields + (_FieldDef("display_name", "displayName"),)
    _kml_root_attribs = _BaseObject._kml_root_attribs + (
        _RootAttribDef("type", "type"),
        _RootAttribDef("name", "name"),
    )

    def __init__(
        self,
        type: str,
        name: str,
        display_name: str | None = None,
    ) -> None:
        """SimpleField instance constructor."""
        super().__init__()
        self.type = type
        self.name = name
        self.display_name = display_name


class Schema(Object):
    """A KML `<Schema>` tag constructor.

    Specifies a custom KML schema that is used to add custom data to KML `Feature`s.
    `Schema` is always a child of `Document`.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#schema

    Parameters
    ----------
    name : str
        The name of the `Schema`.
    schema_fields : SimpleField | Iterable[SimpleField] | None, default = None
        The fields of the `Schema`.

    Attributes
    ----------
    Same as parameters

    """

    _kml_tag = "Schema"
    _kml_dependents = Object._kml_dependents + (_DependentDef("schema_fields"),)
    _kml_root_attribs = Object._kml_root_attribs + (_RootAttribDef("name", "name"),)

    def __init__(
        self,
        name: str,
        schema_fields: SimpleField | Iterable[SimpleField] | None = None,
    ) -> None:
        """Construct Schema instance."""
        Object.__init__(self)
        self.name = name
        self._schema_fields = list[SimpleField]()
        self.schema_fields = schema_fields

    @property
    def schema_fields(self) -> Iterator[SimpleField]:
        """Generator over schema fields."""
        yield from self._schema_fields

    @schema_fields.setter
    def schema_fields(self, value: SimpleField | Iterable[SimpleField] | None) -> None:
        self._schema_fields.clear()
        if value is not None:
            if isinstance(value, SimpleField):
                self._schema_fields.append(value)
            else:
                self._schema_fields.extend(value)
