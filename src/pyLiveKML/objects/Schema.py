"""Schema module."""

from typing import Iterable, Iterator

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import (
    _BaseObject,
    _DependentDef,
    _FieldDef,
    Object,
)


class SimpleField(_BaseObject):
    """SimpleField class.

    `Schema` instances contain a collection of `SimpleField` instances.
    """

    _kml_tag = "SimpleField"
    _kml_fields = _BaseObject._kml_fields + (_FieldDef("display_name", "displayName"),)

    def __init__(
        self,
        type: str,
        name: str,
        display_name: str | None,
    ) -> None:
        """SimpleField instance constructor."""
        super().__init__()
        self.type = type
        self.name = name
        self.display_name = display_name

    def construct_kml(
        self, with_children: bool = True, with_dependents: bool = True
    ) -> etree.Element:
        """Construct this instances' KML representation."""
        root = etree.Element(
            self.kml_tag, attrib={"type": self.type, "name": self.name}
        )
        self.build_kml(root, with_children, with_dependents)
        return root


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

    def __init__(
        self,
        name: str,
        schema_fields: SimpleField | Iterable[SimpleField] | None = None,
    ) -> None:
        """Construct Schema instances."""
        Object.__init__(self)
        self.name = name
        self._schema_fields = list[SimpleField]()
        self.schema_fields = schema_fields

    @property
    def schema_fields(self) -> Iterator[SimpleField]:
        """Generator over schema_fields."""
        yield from self._schema_fields

    @schema_fields.setter
    def schema_fields(self, value: SimpleField | Iterable[SimpleField] | None) -> None:
        self._schema_fields.clear()
        if value is not None:
            if isinstance(value, SimpleField):
                self._schema_fields.append(value)
            else:
                self._schema_fields.extend(value)
