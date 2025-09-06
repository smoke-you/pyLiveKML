"""IconStyle module."""

from lxml import etree  # type: ignore

from pyLiveKML.types import ColorModeEnum, HotSpot, GeoColor
from pyLiveKML.objects.Object import _BaseObject, _FieldDef, NoDump, _DependentDef
from pyLiveKML.objects.ColorStyle import ColorStyle


class _IconStyle_Icon(_BaseObject):
    """A minimalist Icon class, used only within `IconStyle`."""

    _kml_tag = "Icon"
    _kml_fields = _BaseObject._kml_fields + (_FieldDef("href"),)

    def __init__(self, href: str):
        """_IconStyle_Icon instance constructor."""
        super().__init__()
        self.href = href


class IconStyle(ColorStyle):
    """A KML `<IconStyle>` tag constructor.

    Specifies how icons for `Point` placemarks are drawn, both in the "Places" panel and
    in the 3D viewer of Google Earth. The `icon` attribute specifies the icon image. The
    `scale` attribute specifies the x, y scaling of the icon. The color specified in the
    `color` attribute of `IconStyle` is blended with the color of the `Icon`.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#iconstyle

    Parameters
    ----------
    icon: str
        An HTTP address or a local file specification used to load an icon.
    scale: float, default = 1.0
        Resizes the icon.
    heading: float | None, default = None
        Direction in decimal degrees. If not specified, defaults to 0. Values range from
        0 to 360 degrees.
    color: GeoColor | int | None, default = None
    color_mode: ColorModeEnum | None, default = None
    hot_spot: HotSpot | None, default = None
        Specifies the position within the icon that is "anchored" to the `Point` to which
        the style is applied.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "IconStyle"
    _kml_fields = ColorStyle._kml_fields + (
        _FieldDef("icon", dumper=NoDump),
        _FieldDef("scale"),
        _FieldDef("heading"),
    )
    _kml_dependents = ColorStyle._kml_dependents + (
        _DependentDef("icon"),
        _DependentDef("hot_spot"),
    )

    def __init__(
        self,
        icon: str,
        scale: float = 1.0,
        heading: float | None = None,
        color: GeoColor | int | None = None,
        color_mode: ColorModeEnum | None = None,
        hot_spot: HotSpot | None = None,
    ):
        """IconStyle instance constructor."""
        ColorStyle.__init__(self, color=color, color_mode=color_mode)
        self.scale = scale
        self.heading = heading
        self.icon = _IconStyle_Icon(icon)
        self.hot_spot = hot_spot
