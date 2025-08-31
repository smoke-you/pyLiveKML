"""Object module."""

from abc import ABC
from typing import Iterator, Iterable, cast
from uuid import uuid4, UUID
from lxml import etree  # type: ignore

from pyLiveKML.KML._BaseObject import (
    _BaseObject,
    ObjectState,
    _ListObject,
    ObjectChild,
    _ChildDef,
)
from pyLiveKML.KML.utils import with_ns


class Object(_BaseObject, ABC):
    """A KML 'Object', per https://developers.google.com/kml/documentation/kmlreference#object.

    Note that the :class:`~pyLiveKML.KMLObjects.Object` class is explicitly abstract,
    and is the base class from which most other KML elements (anything with an :attr:`id`
    property) derive.
    """

    _suppress_id: bool = False

    def __init__(self) -> None:
        """Object instance constructor."""
        super().__init__()
        self._id: UUID = uuid4()

    @property
    def id(self) -> UUID:
        """The unique identifier of this :class:`~pyLiveKML.KMLObjects.Object`."""
        return self._id

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element.

        Generate the KML representation of the internal fields of this
        :class:`~pyLiveKML.KMLObjects.Object`, and append it to the provided root
        etree.Element.

        :param etree.Element root: The root XML element that will be appended to.
        :param bool with_children: True if the children of this instance should be
            included in the build.
        """
        super().build_kml(root, with_children)
        if with_children:
            for dc in self.direct_children:
                id = None
                if not getattr(dc, "_suppress_id", True):
                    id = getattr(dc, "id", None)
                attribs = None if id is None else {"id": str(id)}
                branch = etree.SubElement(root, with_ns(dc._kml_tag), attrib=attribs)
                dc.build_kml(branch, True)

    def construct_kml(self) -> etree.Element:
        """Construct this :class:`~pyLiveKML.KMLObjects.Object`'s KML representation.

        :returns: The KML representation of the object as an etree.Element.
        """
        if self._suppress_id:
            attribs = None
        else:
            attribs = {"id": str(self.id)}
        root = etree.Element(_tag=with_ns(self.kml_tag), attrib=attribs)
        self.build_kml(root)
        return root

    def __str__(self) -> str:
        """Return a string representation."""
        return f"{self.kml_tag}"

    def __repr__(self) -> str:
        """Return a debug representation."""
        return self.__str__()
