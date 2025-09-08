"""NetworkLink module."""

from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML.objects.AbstractView import AbstractView
from pyLiveKML.objects.ExtendedData import ExtendedData
from pyLiveKML.objects.Feature import Feature
from pyLiveKML.objects.Link import Link
from pyLiveKML.objects.Object import _FieldDef, _ChildDef
from pyLiveKML.objects.Region import Region
from pyLiveKML.objects.StyleSelector import StyleSelector
from pyLiveKML.objects.TimePrimitive import TimePrimitive


class NetworkLink(Feature):
    """A KML 'NetworkLink' tag constructor.

    References a KML file or KMZ archive on a local or remote network. Use the `link`
    attribute to specify the location of the KML file. Within that `Link`, you can define
    the refresh options for updating the file, based on time and camera change.
    `NetworkLink`s can be used in combination with `Region`s to handle very large
    datasets efficiently.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#networklink

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
    fly_to_view: bool | None, default = None
        If `True`, causes Google Earth to fly to the view of the `LookAt` or `Camera` in
        the `NetworkLinkControl` (if it exists). If the `NetworkLinkControl` does not
        contain an `AbstractView` element, Google Earth flies to the `LookAt` or `Camera`
        element in the `Feature` child within the `<kml>` tag in the refreshed file. If the
        `<kml>` tag does not have a `LookAt` or `Camera` specified, or `fly_to_view` is
        `False`, the view is unchanged.
    refresh_visibility: bool | None, default = None
        If `False`, leaves the visibility of features within the control of the Google
        Earth user. Set to `True` to reset the visibility of features each time the
        `NetworkLink` is refreshed.
    link : Link | None, default = None
        Specifies the location of the KML file to be loaded.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "NetworkLink"
    _kml_fields = Feature._kml_fields + (
        _FieldDef("fly_to_view", "flyToView"),
        _FieldDef("refresh_visibility", "refreshVisibility"),
    )
    _kml_children = Feature._kml_children + (_ChildDef("link"),)

    def __init__(
        self,
        # inherited from `Feature`
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
        # Specific to `NetworkLink`
        fly_to_view: bool | None = None,
        refresh_visibility: bool | None = None,
        link: Link | None = None,
    ):
        """NetworkLink instance constructor."""
        Feature.__init__(
            self,
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
        self.fly_to_view = fly_to_view
        self.refresh_visibility = refresh_visibility
        self.link = link
