"""ColorStyle module."""

from abc import ABC

from pyLiveKML.objects.Object import _FieldDef, _ColorParse
from pyLiveKML.objects.SubStyle import SubStyle
from pyLiveKML.types import ColorModeEnum, GeoColor


class ColorStyle(SubStyle, ABC):
    """A KML `<ColorStyle>` tag constructor.

    This is an abstract element and cannot be used directly in a KML file. It provides
    elements for specifying the color and color mode of extended style types.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#colorstyle

    Parameters
    ----------
    color: GeoColor | int | None, default = None
    color_mode: ColorModeEnum | None, default = None

    Attributes
    ----------
    Same as parameters.

    """

    _kml_fields: tuple[_FieldDef, ...] = SubStyle._kml_fields + (
        _FieldDef("color", parser=_ColorParse),
        _FieldDef("color_mode", "colorMode"),
    )

    def __init__(
        self,
        color: GeoColor | int | None = None,
        color_mode: ColorModeEnum | None = None,
    ):
        """ColorStyle instance constructor."""
        SubStyle.__init__(self)
        ABC.__init__(self)
        self.color_mode = color_mode
        self.color = GeoColor(color) if isinstance(color, int) else color
