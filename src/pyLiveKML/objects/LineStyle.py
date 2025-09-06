"""LineStyle module."""

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import _FieldDef, ColorParse
from pyLiveKML.types.GeoColor import GeoColor
from pyLiveKML.objects.ColorStyle import ColorStyle


class LineStyle(ColorStyle):
    """A KML `<LineStyle>` tag constructor.

    Specifies the drawing style (color, color mode, and line width) for all line
    geometry. Line geometry includes the outlines of outlined `Polygon`s and the extruded
    "tether" of `Placemark` icons (if extrusion is enabled).

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#linestyle

    Parameters
    ----------
    width: float | None, default = None
        Width of the line, in pixels.
    color: GeoColor | int | None, default = None
    outer_color: GeoColor | int | None, default = None
        Color of the portion of the line defined by `outer_width`. Note that the
        `outer_color` and `outer_width` attributes are ignored when a `LineStyle` is
        applied to a `Polygon` or `LinearRing`.
    outer_width: float | None, default = None
        A value between 0.0 and 1.0 that specifies the proportion of the line that uses
        the `outer_color`. Only applies to lines setting width with `physical_width`; it
        does not apply to lines using `width`. See also `draw_order` in `LineString`. A
        draw order value may be necessary if dual-colored lines are crossing each other,
        for example, for showing freeway interchanges.
    physical_width: float | None, default = None
        Physical width of the line, in meters.
    label_visibility: bool | None, default = None
        Whether or not to display a text label on a `LineString`. A `LineString`'s label
        is contained in the `name` attribute that is a sibling of `LineString`, i.e. is
        contained within the same `Placemark`.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "LineStyle"
    _kml_fields = ColorStyle._kml_fields + (
        _FieldDef("width"),
        _FieldDef("outer_color", "gx:outerColor", ColorParse),
        _FieldDef("outer_width", "gx:outerWidth"),
        _FieldDef("physical_width", "gx:physicalWidth"),
        _FieldDef("label_visibility", "gx:labelVisibility"),
    )

    def __init__(
        self,
        width: float | None = None,
        color: GeoColor | int | None = None,
        outer_color: GeoColor | int | None = None,
        outer_width: float | None = None,
        physical_width: float | None = None,
        label_visibility: bool | None = None,
    ):
        """LineStyle instance constructor."""
        ColorStyle.__init__(self, color)
        self.width = width
        self.outer_color = outer_color
        self.outer_width = outer_width
        self.physical_width = physical_width
        self.label_visibility = label_visibility
