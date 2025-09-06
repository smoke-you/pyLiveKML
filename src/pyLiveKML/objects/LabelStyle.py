"""ColorStyle module."""

from lxml import etree  # type: ignore

from pyLiveKML.types import ColorModeEnum, GeoColor
from pyLiveKML.objects.Object import _FieldDef
from pyLiveKML.objects.ColorStyle import ColorStyle


class LabelStyle(ColorStyle):
    """A KML `<LabelStyle>` tag constructor.

    Specifies how the `name` of a `Feature` is drawn in the 3D viewer.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#labelstyle

    Parameters
    ----------
    scale: float, default = 1.0
        Resizes the label.
    color: GeoColor | int | None, default = None
    color_mode: ColorModeEnum | None, default = None

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "LabelStyle"
    _kml_fields = ColorStyle._kml_fields + (_FieldDef("scale"),)

    def __init__(
        self,
        scale: float | None = None,
        color: GeoColor | int | None = None,
        color_mode: ColorModeEnum | None = None,
    ):
        """ColorStyle instance constructor."""
        super().__init__(color=color, color_mode=color_mode)
        self.scale = scale
