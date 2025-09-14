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

"""Tour module."""

from typing import Iterable, Iterator

from lxml import etree  # type: ignore

from pyLiveKML.objects.AbstractView import AbstractView
from pyLiveKML.objects.ExtendedData import ExtendedData
from pyLiveKML.objects.Feature import Feature
from pyLiveKML.objects.Object import (
    _BaseObject,
    _ChildDef,
    _DeletableMixin,
    _DependentDef,
    _FieldDef,
    _ListObject,
    Object,
)
from pyLiveKML.objects.Region import Region
from pyLiveKML.objects.StyleSelector import StyleSelector
from pyLiveKML.objects.TimePrimitive import TimePrimitive
from pyLiveKML.objects.TourPrimitive import TourPrimitive


class Playlist(_DeletableMixin, _ListObject[TourPrimitive], _BaseObject):
    """A KML `<Playlist>` tag constructor.

    Contains any number of `TourPrimitive` objects.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#contains_6

    Parameters
    ----------
    items : TourPrimitive | Iterable[TourPrimitive] | None, default = None
        The `TourPrimitive` items in the playlist.

    Attributes
    ----------
    Nil

    """

    _kml_tag = "gx:Playlist"
    _kml_children = _BaseObject._kml_children + (_ChildDef("items"),)
    _yield_self = True

    def __init__(
        self, items: TourPrimitive | Iterable[TourPrimitive] | None = None
    ) -> None:
        """Playlist instance constructor."""
        _DeletableMixin.__init__(self)
        _ListObject[TourPrimitive].__init__(self)
        _BaseObject.__init__(self)
        self.items = items

    @property
    def items(self) -> Iterator[TourPrimitive]:
        """Retrieve a generator over the `TourPrimitive`s in this `Tour`.

        If the property setter is called, replaces the current list of contained
        `TourPrimitive`s with those provided.

        Parameters
        ----------
        value : TourPrimitive | Iterable[TourPrimitive] | None
            The new `TourPrimitive` elements for the `Tour`.

        :returns: A generator over the `TourPrimitive`s in the `Tour`.
        :rtype: Iterator[TourPrimitive]

        """
        yield from self

    @items.setter
    def items(self, value: TourPrimitive | Iterable[TourPrimitive] | None) -> None:
        self.clear()
        if value is not None:
            if isinstance(value, TourPrimitive):
                self.append(value)
            else:
                self.extend(value)


class Tour(Feature):
    """A KML `<gx:Tour>` tag constructor.

    A `Tour` contains a single `PlayList`, which in turn contains an ordered list of
    `TourPrimitive` elements that define a tour in any KML browser.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#gxtour
    * https://developers.google.com/kml/documentation/touring

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
    playlist: TourPrimitive | list[TourPrimitive] | None, default = None

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "gx:Tour"
    _kml_dependents = Object._kml_dependents + (_DependentDef("playlist"),)

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
        playlist: TourPrimitive | Iterable[TourPrimitive] | None = None,
    ) -> None:
        """Tour instance constructor."""
        super().__init__(
            name=name,
            visibility=visibility,
            is_open=is_open,
            author_name=author_name,
            author_link=author_link,
            address=address,
            phone_number=phone_number,
            snippet=snippet,
            snippet_max_lines=snippet_max_lines,
            description=description,
            abstract_view=abstract_view,
            time_primitive=time_primitive,
            style_url=style_url,
            styles=styles,
            region=region,
            extended_data=extended_data,
        )
        self.playlist = Playlist(playlist)
