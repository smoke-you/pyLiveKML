"""Schema module."""

from typing import Iterable, Iterator

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import _BaseObject
from pyLiveKML.objects.Object import Object, _ListObject


# TODO: This needs some work. There are issues around how `SimpleField` works.
# Also need to consider the `<ExtendedData>` tag/class, and `SimpleArrayData` in `Track.`
# Too much complexity to deal with at this point.


class SimpleField(_BaseObject):
    """SimpleField class.

    `Schema` instances contain a collection of `SimpleField` instances.
    """

    _kml_tag = "SimpleField"

    def __init__(
        self,
        type: str,
        name: str,
        display_names: str | Iterable[str] | None,
    ) -> None:
        """SimpleField instance constructor."""
        self.type = type
        self.name = name
        self.display_names = list[str]()
        if display_names:
            if isinstance(display_names, str):
                self.display_names.append(display_names)
            else:
                self.display_names.extend(display_names)

    def build_kml(
        self,
        root: etree.Element,
        with_children: bool = True,
        with_dependents: bool = True,
    ) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        for dn in self.display_names:
            etree.SubElement(root, "displayName").text = dn

    def construct_kml(
        self, with_children: bool = True, with_dependents: bool = True
    ) -> etree.Element:
        """Construct this instances' KML representation."""
        root = etree.Element(
            self.kml_tag, attrib={"type": self.type, "name": self.name}
        )
        self.build_kml(root, with_children, with_dependents)
        return root


class Schema(_ListObject[SimpleField], Object):
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

    def __init__(
        self,
        name: str,
        schema_fields: SimpleField | Iterable[SimpleField] | None = None,
    ) -> None:
        """Construct Schema instances."""
        Object.__init__(self)
        _ListObject[SimpleField].__init__(self)
        self.name = name
        self.schema_fields = schema_fields

    @property
    def schema_fields(self) -> Iterator[SimpleField]:
        """Generator over schema_fields."""
        yield from self

    @schema_fields.setter
    def schema_fields(self, value: SimpleField | Iterable[SimpleField] | None) -> None:
        self.clear()
        if value is not None:
            if isinstance(value, SimpleField):
                self.append(value)
            else:
                self.extend(value)
