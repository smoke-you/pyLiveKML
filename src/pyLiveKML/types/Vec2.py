"""Vec2 module."""

from abc import ABC

from lxml import etree  # type: ignore

from pyLiveKML.types.types import UnitsEnum
from pyLiveKML.objects.Object import _BaseObject


class Vec2(_BaseObject, ABC):
    """Abstract base for Vec2 subclasses."""

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

    def build_kml(
        self,
        root: etree.Element,
        with_children: bool = True,
        with_dependents: bool = True,
    ) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        attribs = {
            "x": str(self.x),
            "y": str(self.y),
            "xunits": self.x_units.value,
            "yunits": self.y_units.value,
        }
        etree.SubElement(root, self._kml_tag, attrib=attribs)

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
    """HotSpot Vec2 subclass.

    Used only by the `IconStyle` class.
    """

    _kml_tag = "hotSpot"


class OverlayXY(Vec2):
    """OverlayXY Vec2 subclass.

    Used only by the `ScreenOverlay` class.
    """

    _kml_tag = "overlayXY"


class ScreenXY(Vec2):
    """ScreenXY Vec2 subclass.

    Used only by the `ScreenOverlay` class.
    """

    _kml_tag = "screenXY"


class RotationXY(Vec2):
    """RotationXY Vec2 subclass.

    Used only by the `ScreenOverlay` class.
    """

    _kml_tag = "rotationXY"


class Size(Vec2):
    """Size Vec2 subclass.

    Used only by the `ScreenOverlay` class.
    """

    _kml_tag = "size"
