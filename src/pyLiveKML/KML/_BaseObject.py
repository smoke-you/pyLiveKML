from abc import ABC
from collections.abc import Iterable
from typing import Any, Iterator, NamedTuple, Optional

from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import ArgParser, NoDump


class _BaseObject(ABC):

    _kml_type: str = ""
    _kml_fields: tuple[ArgParser, ...] = tuple()

    def __setattr__(self, name: str, value: Any) -> None:
        """Object setattr method."""
        match = next(filter(lambda x: x.name, self._kml_fields), None)
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
    def kml_type(self) -> str:
        """The class' KML type string.

        Property that specifies the name of the XML tag that forms the root of
        the KML representation of this :class:`~pyLiveKML.KML.KMLObjects.Object`.
        """
        return self._kml_type

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element.

        Generate the KML representation of the internal fields of this
        :class:`~pyLiveKML.KML.KMLObjects.Object`, and append it to the provided root
        etree.Element.

        :param etree.Element root: The root XML element that will be appended to.
        :param bool with_children: True if the children of this instance should be
            included in the build.
        """
        for f in (f for f in self._kml_fields if f.dumper != NoDump):
            value = f.dumper.dump(getattr(self, f.name))
            if value:
                etree.SubElement(root, f.typename).text = value

    def construct_kml(self) -> etree.Element:
        """Construct this :class:`~pyLiveKML.KML.KMLObjects.Object`'s KML representation.

        :returns: The KML representation of the object as an etree.Element.
        """
        root = etree.Element(_tag=self.kml_type)
        self.build_kml(root)
        return root
