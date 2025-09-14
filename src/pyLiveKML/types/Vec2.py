"""Vec2 module."""

from abc import ABC

from lxml import etree  # type: ignore

from pyLiveKML.types.types import UnitsEnum
from pyLiveKML.objects.Object import _BaseObject, _RootAttribDef


class Vec2(_BaseObject, ABC):
    """Abstract base for Vec2 subclasses.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#kml-fields

    Parameters
    ----------
    x : float, default = 0.5
    y : float, default = 0.5
    x_units : UnitsEnum, default = UnitsEnum.FRACTION
    y_units : UnitsEnum, default = UnitsEnum.FRACTION

    """

    _kml_root_attribs = _BaseObject._kml_root_attribs + (
        _RootAttribDef("x", "x"),
        _RootAttribDef("y", "y"),
        _RootAttribDef("xunits", "x_units"),
        _RootAttribDef("yunits", "y_units"),
    )

    def __init__(
        self,
        x: float = 0.5,
        y: float = 0.5,
        x_units: UnitsEnum = UnitsEnum.FRACTION,
        y_units: UnitsEnum = UnitsEnum.FRACTION,
    ):
        """Vec2 instance constructor."""
        super().__init__()
        self.x = x
        self.y = y
        self.x_units = x_units
        self.y_units = y_units

    def __eq__(self, other: object) -> bool:
        """Check equality."""
        return (
            isinstance(other, type(self))
            and self.x == other.x
            and self.y == other.y
            and self.x_units == other.x_units
            and self.y_units == other.y_units
        )


class HotSpot(Vec2):
    """Icon hotspot descriptor.

    Specifies the position within an `<Icon>` that is "anchored" to a `<Point>`.

    The x and y values can be specified in three different ways: as pixels, as fractions
    of the icon, or as inset pixels, which is an offset in pixels from the upper right
    corner of the icon. The x and y positions can be specified in different ways; for
    example, x can be in pixels and y can be a fraction. The origin of the coordinate
    system is in the lower left corner of the icon.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#kml-fields
    * https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-iconstyle

    Parameters
    ----------
    x : float, default = 0.5
        Either the number of pixels, a fractional component of the icon, or a pixel inset
        indicating the x component of a point on the icon.
    y : float, default = 0.5
        Either the number of pixels, a fractional component of the icon, or a pixel inset
        indicating the y component of a point on the icon.
    x_units : UnitsEnum, default = UnitsEnum.FRACTION
        Units in which the x value is specified.
    y_units : UnitsEnum, default = UnitsEnum.FRACTION
        Units in which the y value is specified.

    """

    _kml_tag = "hotSpot"


class OverlayXY(Vec2):
    """Overlay image offset descriptor.

    Specifies a point on (or outside of) the overlay image that is mapped to the screen
    coordinate. It requires x and y values, and the units for those values.

    The x and y values can be specified in three different ways: as pixels, as fractions
    of the image, or as inset pixels, which is an offset in pixels from the upper right
    corner of the image. The x and y positions can be specified in different ways; for
    example, x can be in pixels and y can be a fraction. The origin of the coordinate
    system is in the lower left corner of the image.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#kml-fields
    * https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-screenoverlay

    Parameters
    ----------
    x : float, default = 0.5
        Either the number of pixels, a fractional component of the image, or a pixel inset
        indicating the x component of a point on the image.
    y : float, default = 0.5
        Either the number of pixels, a fractional component of the image, or a pixel inset
        indicating the y component of a point on the image.
    x_units : UnitsEnum, default = UnitsEnum.FRACTION
        Units in which the x value is specified.
    y_units : UnitsEnum, default = UnitsEnum.FRACTION
        Units in which the y value is specified.

    """

    _kml_tag = "overlayXY"


class ScreenXY(Vec2):
    """Overlay screen offset descriptor.

    Specifies a point relative to the screen origin that the overlay image is mapped to.

    The x and y values can be specified in three different ways: as pixels, as fractions
    of the screen, or as inset pixels, which is an offset in pixels from the upper right
    corner of the screen. The x and y positions can be specified in different ways; for
    example, x can be in pixels and y can be a fraction. The origin of the coordinate
    system is in the lower left corner of the screen.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#kml-fields
    * https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-screenoverlay

    Parameters
    ----------
    x : float, default = 0.5
        Either the number of pixels, a fractional component of the screen, or a pixel inset
        indicating the x component of a point on the screen.
    y : float, default = 0.5
        Either the number of pixels, a fractional component of the screen, or a pixel inset
        indicating the y component of a point on the screen.
    x_units : UnitsEnum, default = UnitsEnum.FRACTION
        Units in which the x value is specified.
    y_units : UnitsEnum, default = UnitsEnum.FRACTION
        Units in which the y value is specified.

    """

    _kml_tag = "screenXY"


class RotationXY(Vec2):
    """Overlay screen rotation descriptor.

    Point relative to the screen about which the screen overlay is rotated.

    The x and y values can be specified in three different ways: as pixels, as fractions
    of the screen, or as inset pixels, which is an offset in pixels from the upper right
    corner of the screen. The x and y positions can be specified in different ways; for
    example, x can be in pixels and y can be a fraction. The origin of the coordinate
    system is in the lower left corner of the screen.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#kml-fields
    * https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-screenoverlay

    Parameters
    ----------
    x : float, default = 0.5
        Either the number of pixels, a fractional component of the screen, or a pixel inset
        indicating the x component of a point on the screen.
    y : float, default = 0.5
        Either the number of pixels, a fractional component of the screen, or a pixel inset
        indicating the y component of a point on the screen.
    x_units : UnitsEnum, default = UnitsEnum.FRACTION
        Units in which the x value is specified.
    y_units : UnitsEnum, default = UnitsEnum.FRACTION
        Units in which the y value is specified.

    """

    _kml_tag = "rotationXY"


class Size(Vec2):
    """Overlay screen size descriptor.

    Specifies the size of the image for the screen overlay. Separately for x and y:

    * A value of -1 indicates to use the native dimension
    * A value of 0 indicates to maintain the aspect ratio
    * A value of n sets the value of the dimension

    The x and y values can be specified in three different ways: as pixels, as fractions
    of the image, or as inset pixels, which is an offset in pixels from the upper right
    corner of the image. The x and y positions can be specified in different ways; for
    example, x can be in pixels and y can be a fraction. The origin of the coordinate
    system is in the lower left corner of the image.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#kml-fields
    * https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-screenoverlay

    Parameters
    ----------
    x : float, default = 0.5
        Either the number of pixels, a fractional component of the screen, or a pixel inset
        indicating the x component of a point on the screen.
    y : float, default = 0.5
        Either the number of pixels, a fractional component of the screen, or a pixel inset
        indicating the y component of a point on the screen.
    x_units : UnitsEnum, default = UnitsEnum.FRACTION
        Units in which the x value is specified.
    y_units : UnitsEnum, default = UnitsEnum.FRACTION
        Units in which the y value is specified.

    """

    _kml_tag = "size"
