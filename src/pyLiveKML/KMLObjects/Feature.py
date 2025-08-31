"""Feature module.

:note: Includes the `Container` class definition as well, to avoid a circular import.
"""

from abc import ABC
from typing import Iterable, Iterator, cast

from lxml import etree  # type: ignore

from pyLiveKML.KML._BaseObject import _FieldDef, NoDump
from pyLiveKML.KML.utils import with_ns
from pyLiveKML.KMLObjects.AbstractView import AbstractView
from pyLiveKML.KMLObjects.Object import Object, _ChildDef
from pyLiveKML.KMLObjects.Region import Region
from pyLiveKML.KMLObjects.StyleSelector import StyleSelector
from pyLiveKML.KMLObjects.TimePrimitive import TimePrimitive


class Feature(Object, ABC):
    """A KML 'Feature', per https://developers.google.com/kml/documentation/kmlreference#feature.

    :note: While Features are explicitly abstract in the KML specification,
    :class:`~pyLiveKML.KMLObjects.Feature` is the base class for KML
    :class:`~pyLiveKML.KMLObjects.Object` instances that have an "existence" in
    GEP, i.e. that are (potentially) user-editable because they appear in the GEP user
    List View.

    :param str|None name: The (optional) name for this :class:`~pyLiveKML.KMLObjects.Feature` that will be
        displayed in GEP.
    :param str|None description: The (optional) description for this :class:`~pyLiveKML.KMLObjects.Feature`
        that will be displayed in GEP as a text balloon if the :class:`~pyLiveKML.KMLObjects.Feature` is clicked.
    :param bool|None visibility: The (optional) initial visibility for this
        :class:`~pyLiveKML.KMLObjects.Feature` in GEP.
    :param Feature|None container: The (optional) :class:`~pyLiveKML.KMLObjects.Feature` (generally, a
        :class:`~pyLiveKML.KMLObjects.Container`) that encloses this
        :class:`~pyLiveKML.KMLObjects.Feature`.
    :param str|None style_url: An (optional) style URL, typically a reference to a global
        :class:`~pyLiveKML.KMLObjects.StyleSelector` in a :class:`~pyLiveKML.KMLObjects.Container` that
        encloses this :class:`~pyLiveKML.KMLObjects.Feature`.
    :param Iterable[StyleSelector]|None styles: An iterable of :class:`~pyLiveKML.KMLObjects.StyleSelector`
        objects that are local to this :class:`~pyLiveKML.KMLObjects.Feature`.
    """

    _kml_fields: tuple[_FieldDef, ...] = Object._kml_fields + (
        _FieldDef("name"),
        _FieldDef("visibility"),
        _FieldDef("is_open", "open"),
        _FieldDef("author_name", dumper=NoDump),
        _FieldDef("author_link", dumper=NoDump),
        _FieldDef("address"),
        _FieldDef("snippet", dumper=NoDump),
        _FieldDef("snippet_max_line", dumper=NoDump),
        _FieldDef("phone_number", "phoneNumber"),
        _FieldDef("description"),
        _FieldDef("style_url", "styleUrl"),
    )
    _direct_children: tuple[_ChildDef, ...] = Object._direct_children + (
        _ChildDef("abstract_view"),
        _ChildDef("time_primitive"),
        _ChildDef("region"),
        _ChildDef("_styles", None, False),
    )

    def __init__(
        self,
        name: str | None = None,
        visibility: bool | None = None,
        is_open: bool | None = None,
        author_name: str | None = None,
        author_link: str | None = None,
        address: str | None = None,
        phone_number: str | None = None,
        snippet: str | None = None,
        snippet_max_lines: int | None = None,
        description: str | None = None,
        abstract_view: AbstractView | None = None,
        time_primitive: TimePrimitive | None = None,
        style_url: str | None = None,
        styles: StyleSelector | Iterable[StyleSelector] | None = None,
        region: Region | None = None,
    ):
        """Feature instance constructor."""
        Object.__init__(self)
        ABC.__init__(self)
        self.name = name
        self.visibility = visibility
        self.is_open = is_open
        self.author_name = author_name
        self.author_link = author_link
        self.address = address
        self.phone_number = phone_number
        self.snippet = snippet
        self.snippet_max_lines = snippet_max_lines
        self.description = description
        self.abstract_view = abstract_view
        self.time_primitive = time_primitive
        self.style_url = style_url
        self._styles = list[StyleSelector]()
        self.styles = styles
        self.region = region

    @property
    def styles(self) -> Iterator[StyleSelector]:
        """The Style objects that are direct children of this instance.

        A generator to retrieve references to any :class:`~pyLiveKML.KMLObjects.Style` or
        :class:`~pyLiveKML.KMLObjects.StyleMap` objects that are children of this
        :class:`~pyLiveKML.KMLObjects.Feature`.

        :returns: A generator of :class:`~pyLiveKML.KMLObjects.StyleSelector` objects.
        """
        for s in self._styles:
            yield s

    @styles.setter
    def styles(self, value: StyleSelector | Iterable[StyleSelector] | None) -> None:
        self._styles.clear()
        if value is not None:
            if isinstance(value, StyleSelector):
                self._styles.append(value)
            else:
                self._styles.extend(value)

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        if self.author_name is not None:
            author = etree.SubElement(root, with_ns("atom:author"))
            etree.SubElement(author, with_ns("atom:name")).text = self.author_name
        if self.author_link is not None:
            etree.SubElement(
                root, with_ns("atom:link"), attrib={"href": self.author_link}
            )
        if self.snippet is not None:
            attribs = {}
            if self.snippet_max_lines is not None:
                attribs["maxLines"] = str(self.snippet_max_lines)
            etree.SubElement(root, "Snippet", attribs).text = self.snippet

    # override Object.select() to enable upwards cascade, i.e. if a Feature contained
    # in an unselected parent Feature is selected, the parent Feature must also be
    # selected in order for GEP synchronization to work correctly.
    def select(self, value: bool, cascade: bool = False) -> None:
        """Cascade select upwards, but do not cascade deselect upwards.

        Overrides :func:`~pyLiveKML.KMLObjects.Object.Object.select` to implement upwards cascade of selection.
        That is, if a :class:`~pyLiveKML.KMLObjects.Feature` enclosed in the object tree depending from an
        unselected  parent :class:`~pyLiveKML.KMLObjects.Feature` is selected, the reverse tree's parents must also
        be selected in order for GEP synchronization to work correctly.
        """
        Object.select(self, value, cascade)
        # Cascade Select *upwards* for Features, but *do not* cascade Deselect upwards
        if value and self._container:
            self._container.select(True, False)

    def __str__(self) -> str:
        """Return a string representation."""
        return f"{self.kml_tag}:{self.name}"
