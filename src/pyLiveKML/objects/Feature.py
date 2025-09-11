"""Feature module."""

from abc import ABC
from typing import Iterable, Iterator

from lxml import etree  # type: ignore

from pyLiveKML.objects.AbstractView import AbstractView
from pyLiveKML.objects.ExtendedData import ExtendedData
from pyLiveKML.objects.Object import (
    _ChildDef,
    _DependentDef,
    _FieldDef,
    _NoDump,
    Object,
)
from pyLiveKML.objects.Region import Region
from pyLiveKML.objects.StyleSelector import StyleSelector
from pyLiveKML.objects.TimePrimitive import TimePrimitive
from pyLiveKML.utils import with_ns


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
    is_open : bool | None, default = None
        Specifies whether a `Document` or `Folder` appears closed or open when first
        loaded into the "Places" panel. `False` or `None` is collapsed (the default),
        `True` is expanded. This element applies only to `Document`, `Folder`, and
        `NetworkLink`.
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
    extended_data : ExtendedData | None, default = None
        Allows you to add custom data to a KML file. This data can be:
        * Data that references an external XML schema.
        * Untyped data/value pairs.
        * Typed data.

        A given KML `Feature` can contain a combination of these types of custom data.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_fields = Object._kml_fields + (
        _FieldDef("name"),
        _FieldDef("is_open", "open"),
        _FieldDef("visibility"),
        _FieldDef("author_name", dumper=_NoDump),
        _FieldDef("author_link", dumper=_NoDump),
        _FieldDef("address"),
        _FieldDef("snippet", dumper=_NoDump),
        _FieldDef("snippet_max_line", dumper=_NoDump),
        _FieldDef("phone_number", "phoneNumber"),
        _FieldDef("description"),
        _FieldDef("style_url", "styleUrl"),
    )
    _kml_children: tuple[_ChildDef, ...] = Object._kml_children + (
        _ChildDef("abstract_view"),
        _ChildDef("regions"),
        _ChildDef("styles"),
    )
    _kml_dependents = Object._kml_dependents + (
        _DependentDef("time_primitive"),
        _DependentDef("extended_data"),
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
        extended_data: ExtendedData | None = None,
    ):
        """Feature instance constructor."""
        Object.__init__(self)
        ABC.__init__(self)
        self.name = name
        self.is_open = is_open
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
        self.extended_data = extended_data

    @property
    def styles(self) -> Iterator[StyleSelector]:
        """Retrieve a generator over the `StyleSelector` instances in this `Feature`.

        If the property setter is called, replaces the current list of contained
        `StyleSelector`'s with those provided.

        Parameters
        ----------
        value : StyleSelector | Iterable[StyleSelector] | None
            The new `StyleSelector` elements for the `Feature`.

        :returns: A generator over the `StyleSelector`s in the `Feature`.
        :rtype: Iterator[StyleSelector]

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

    # @property
    # def dependents(self) -> Iterator[ObjectChild]:
    #     """A generator over the dependents of the instance.

    #     Overridden from `_BaseObject` because when using the default behaviour, if
    #     `geometry` is a `MultiGeometry`, then the `MultiGeometry` itself is never
    #     yielded.

    #     :return: A generator over the dependents of the instance.
    #     :rtype: Iterator[ObjectChild]
    #     """
    #     yield from super().dependents
    #     if self.extended_data:
    #         yield ObjectChild(self, self.extended_data)

    def build_kml(
        self,
        root: etree.Element,
        with_children: bool = True,
        with_dependents: bool = True,
    ) -> None:
        """Build the KML sub-tags for this `Feature` and append it to the provided `etree.Element`.

        Overridden from :class:`pyLiveKML.objects.Object.Object` to perform some
        additional build steps.

        Parameters
        ----------
        root : etree.Element
            The tag into which the sub-tags are to be inserted.
        with_children : bool, default = True
            Whether the `children` of the `Feature` should be constructed as sub-tags.
        with_dependents : bool, default = True
            Whether the `dependents` of the `Feature` should be constructed as sub-tags.

        """
        super().build_kml(root, with_children, with_dependents)
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

    def __str__(self) -> str:
        """Return a string representation."""
        return f"{self.kml_tag}:{self.name}"
