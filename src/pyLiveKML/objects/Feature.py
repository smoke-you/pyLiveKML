"""Feature module.

:note: Includes the `Container` class definition as well, to avoid a circular import.
"""

from abc import ABC
from typing import Iterable, Iterator

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import Object, _FieldDef, NoDump, _ChildDef, _DependentDef
from pyLiveKML.utils import with_ns
from pyLiveKML.objects.AbstractView import AbstractView
from pyLiveKML.objects.Region import Region
from pyLiveKML.objects.StyleSelector import StyleSelector
from pyLiveKML.objects.TimePrimitive import TimePrimitive


class Feature(Object, ABC):
    """A KML `<Feature>` tag constructor.

    This is an abstract element and cannot be used directly in a KML file.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#feature

    Parameters
    ----------
    name : str|None, default = None
        User-defined text displayed in the 3D viewer as the label for the object.
    visibility : bool | None, default = None
        Specifies whether the `Feature` is drawn in the 3D viewer when it is initially
        loaded. In order for a `Feature` to be visible, the `<visibility>` tag of all
        its ancestors must also be set `True`.
    author_name : str | None, default = None
        The name of the author of the `Feature`.
    author_link : str | None, default = None
        URL of the web page containing the KML file.
    address : str | None, default = None
        A string value representing an unstructured address written as a standard street,
        city, state address, and/or as a postal code.
    phone_number : str | None, default = None
        A string value representing a telephone number. This element is used by Google
        Maps Mobile only. The industry standard for Java-enabled cellular phones is
        RFC2806.
    snippet : str | None, default = None
        A short description of the `Feature`. In Google Earth, this description is
        displayed in the "Places" panel under the name of the `Feature`. If a `<Snippet>`
        is not supplied, the first two lines of the `<description>` are used. In Google
        Earth, if a `Placemark` contains both a `<description>` and a `<Snippet>`, the
        `<Snippet>` appears beneath the `Placemark` in the "Places" panel, and the
        `<description>` appears in the `Placemark`'s description balloon. This tag does
        not support HTML markup.
    snippet_max_lines : int | None, default = None
    description : str | None, default = None
        User-supplied content that appears in the description balloon. HTML *is*
        supported, but it is **highly** recommended to read the detailed documentation
        at
        https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-feature
    abstract_view : AbstractView | None, default = None
        Any concrete subclass of :class:`pyLiveKML.objects.AbstractView`, i.e. either a
        :class:`pyLiveKML.objects.Camera` or :class:`pyLiveKML.objects.LookAt`
    time_primitive : TimePrimitive | None, default = None
        Any concrete subclass of :class:`pyLiveKML.objects.TimePrimitive`, i.e. either a
        :class:`pyLiveKML.objects.TimeStamp` or :class:`pyLiveKML.objects.TimeSpan`
    style_url : str | None = None
        URL of a `<Style>` or `<StyleMap>` defined in a `<Document>`. If the style is in
        the same file, use a # reference. If the style is defined in an external file,
        use a full URL along with # referencing.
    styles : StyleSelector | Iterable[StyleSelector] | None, default = None
        One or more `Style`s and `StyleMap`s can be defined to customize the appearance
        of any element derived from `Feature` or of the `Geometry` in a `Placemark`. A
        style defined within a `Feature` is called an "inline style" and applies only to
        the `Feature` that contains it. A style defined as the child of a `<Document>` is
        called a "shared style." A shared style must have an id defined for it. This id
        is referenced by one or more `Features` within the `<Document>`. In cases where
        a style element is defined both in a shared style and in an inline style for a
        `Feature` — that is, a `Folder`, `GroundOverlay`, `NetworkLink`, `Placemark`, or
        `ScreenOverlay` — the value for the `Feature`'s inline style takes precedence over
        the value for the shared style.
    region : Region | None, default = None
        `Feature`s and `Geometry`'s associated with a `Region` are drawn only when the
        `Region` is active.

    """

    _kml_fields = Object._kml_fields + (
        _FieldDef("name"),
        _FieldDef("visibility"),
        _FieldDef("author_name", dumper=NoDump),
        _FieldDef("author_link", dumper=NoDump),
        _FieldDef("address"),
        _FieldDef("snippet", dumper=NoDump),
        _FieldDef("snippet_max_line", dumper=NoDump),
        _FieldDef("phone_number", "phoneNumber"),
        _FieldDef("description"),
        _FieldDef("style_url", "styleUrl"),
    )
    _kml_children: tuple[_ChildDef, ...] = Object._kml_children + (_ChildDef("styles"),)
    _kml_dependents = Object._kml_dependents + (
        _DependentDef("abstract_view"),
        _DependentDef("time_primitive"),
        _DependentDef("region"),
    )

    def __init__(
        self,
        name: str | None = None,
        visibility: bool | None = None,
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

    def build_kml(
        self,
        root: etree.Element,
        with_children: bool = True,
        with_dependents: bool = True,
    ) -> None:
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

    # override Object.activate() to enable upwards cascade, i.e. if a Feature contained
    # in an inactive parent Feature is activate, the parent Feature must also be
    # activated in order for GEP synchronization to work correctly.
    def activate(self, value: bool, cascade: bool = False) -> None:
        """Cascade activation upwards, but do not cascade deactivation upwards.

        Overrides :func:`~pyLiveKML.KMLObjects.Object.Object.activate` to implement upwards cascade of activation.
        That is, if a :class:`~pyLiveKML.KMLObjects.Feature` enclosed in the object tree depending from a
        deactivated  parent :class:`~pyLiveKML.KMLObjects.Feature` is activated, the reverse tree's parents must also
        be activated in order for GEP synchronization to work correctly.
        """
        Object.activate(self, value, cascade)
        # Cascade activation *upwards* for Features, but *do not* cascade deactivation upwards
        if value and self._container:
            self._container.activate(True, False)

    def __str__(self) -> str:
        """Return a string representation."""
        return f"{self.kml_tag}:{self.name}"
