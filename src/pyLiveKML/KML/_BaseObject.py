from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Type

from lxml import etree  # type: ignore

from pyLiveKML.KML.GeoColor import GeoColor
from pyLiveKML.KML.utils import with_ns


class _KMLDump(ABC):

    @classmethod
    @abstractmethod
    def dump(cls, value: Any) -> Any:
        raise NotImplementedError


class NoDump(_KMLDump):
    """Dump nothing."""

    @classmethod
    def dump(cls, value: Any) -> Any:
        """Dump and format a KML object field."""
        return ""


class DumpDirect(_KMLDump):
    """Dump to string."""

    @classmethod
    def dump(cls, value: Any) -> Any:
        """Dump and format a KML object field."""
        if value is None:
            return None
        if isinstance(value, Enum):
            return str(value.value)
        if isinstance(value, bool):
            return str(int(value))
        return str(value)


class _KMLParser(ABC):

    @classmethod
    @abstractmethod
    def parse(cls, value: Any) -> Any:
        raise NotImplementedError


class NoParse(_KMLParser):
    """A value that will not be changed."""

    @classmethod
    def parse(cls, value: Any) -> Any:
        """Transform the argument."""
        return value


class Angle90(_KMLParser):
    """A value ≥−90 and ≤90.

    See https://developers.google.com/kml/documentation/kmlreference#kml-fields
    """

    @classmethod
    def parse(cls, value: Any) -> Any:
        """Transform the argument."""
        value = float(value)
        return 90 if value > 90 else -90 if value < -90 else value


class AnglePos90(_KMLParser):
    """A value ≥0 and ≤90.

    See https://developers.google.com/kml/documentation/kmlreference#kml-fields
    """

    @classmethod
    def parse(cls, value: Any) -> Any:
        """Transform the argument."""
        value = float(value)
        return 90 if value > 90 else 0 if value < 0 else value


class Angle180(_KMLParser):
    """A value ≥−180 and ≤180.

    See https://developers.google.com/kml/documentation/kmlreference#kml-fields
    """

    @classmethod
    def parse(cls, value: Any) -> Any:
        """Transform the argument."""
        value = float(value)
        while value > 180:
            value = value - 360
        while value < -180:
            value = value + 360
        return value


class AnglePos180(_KMLParser):
    """A value ≥0 and ≤180.

    See https://developers.google.com/kml/documentation/kmlreference#kml-fields
    """

    @classmethod
    def parse(cls, value: Any) -> Any:
        """Transform the argument."""
        value = float(value)
        return 180 if value > 180 else 0 if value < 0 else value


class Angle360(_KMLParser):
    """A value ≥−360 and ≤360.

    See https://developers.google.com/kml/documentation/kmlreference#kml-fields
    """

    @classmethod
    def parse(cls, value: Any) -> Any:
        """Transform the argument."""
        value = float(value)
        return (
            value % 360 if value > 360 else -(-value % 360) if value < -360 else value
        )


class ColorParse(_KMLParser):
    """A color, typically as a 32-bit ABGR value."""

    @classmethod
    def parse(cls, value: Any) -> Any:
        """Transform the argument."""
        if isinstance(value, int):
            return GeoColor(value)
        return value


class _FieldDef:
    """Describes how a field of a KML object is to be published.

    KML object class definitions specify a tuple of _FieldDef instances as the `_kml_fields`
    class variable.

    :param str name: The name of the field, from the perspective of the Python object.
    :param Type[_KMLParser] parser: The parser class that will be used to transform any value
        assigned to the field. This allows e.g. floats to be constrained to an appropriate
        range.
    :param str tag: The text that will be assigned to the KML tag for the field when it
        is published. May include a prefixed and colon-separated namespace, e.g. "gx:option"
        is valid.
    :param Type[_KMLDump] dumper: The dumper class that will be used to convert and publish
        the field's value to KML.
    """

    def __init__(
        self,
        name: str,
        tag: str | None = None,
        parser: Type[_KMLParser] = NoParse,
        dumper: Type[_KMLDump] = DumpDirect,
    ):
        """_FieldDef instance constructor."""
        self.name = name
        self.typename = tag if tag is not None else name
        self.parser = parser
        self.dumper = dumper


class _BaseObject(ABC):

    _kml_tag: str = ""
    _kml_fields: tuple[_FieldDef, ...] = tuple()

    def __setattr__(self, name: str, value: Any) -> None:
        """Object setattr method."""
        match = next(filter(lambda x: x.name == name, self._kml_fields), None)
        value = match.parser.parse(value) if match is not None else value
        return super().__setattr__(name, value)

    def __eq__(self, value: object) -> bool:
        """Object eq method."""
        return isinstance(value, type(self)) and all(
            map(
                lambda x: getattr(self, x.name) == getattr(value, x.name),
                self._kml_fields,
            )
        )

    @property
    def kml_tag(self) -> str:
        """The class' KML type string.

        Property that specifies the name of the XML tag that forms the root of
        the KML representation of this :class:`~pyLiveKML.KMLObjects.Object`.
        """
        return self._kml_tag

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element.

        Generate the KML representation of the internal fields of this
        :class:`~pyLiveKML.KMLObjects.Object`, and append it to the provided root
        etree.Element.

        :param etree.Element root: The root XML element that will be appended to.
        :param bool with_children: True if the children of this instance should be
            included in the build.
        """
        for f in (f for f in self._kml_fields if f.dumper != NoDump):
            value = f.dumper.dump(getattr(self, f.name))
            if value:
                etree.SubElement(root, with_ns(f.typename)).text = value

    def construct_kml(self) -> etree.Element:
        """Construct this :class:`~pyLiveKML.KMLObjects.Object`'s KML representation.

        :returns: The KML representation of the object as an etree.Element.
        """
        root = etree.Element(_tag=with_ns(self.kml_tag))
        self.build_kml(root)
        return root
