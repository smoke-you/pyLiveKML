from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import UnitsEnum, Vec2Type


class Vec2:
    """
    KML field, per the documentation at https://developers.google.com/kml/documentation/kmlreference#kml-fields, that
    is used to define the reference point, handle, or *hotspot* for an icon in GEP.

    :param Vec2Type vec_type: The sub-type of the Vec2 object. Defaults to 'hotSpot'.
    :param float x: The x value of the Vec2; defaults to 0.5.
    :param float y: The y value of the Vec2; defaults to 0.5.
    :param UnitsEnum x_units: The units type of the Vec2 object's x value. Defaults to 'fraction'.
    :param UnitsEnum y_units: The units type of the Vec2 object's y value. Defaults to 'fraction'.

    :var Vec2Type vec_type: The sub-type of the Vec2 object. Defaults to 'hotSpot'.
    :var float x: The x value of the Vec2; defaults to 0.5.
    :var float y: The y value of the Vec2; defaults to 0.5.
    :var UnitsEnum x_units: The units type of the Vec2 object's x value. Defaults to 'fraction'.
    :var UnitsEnum y_units: The units type of the Vec2 object's y value. Defaults to 'fraction'.
    """

    def __init__(
        self,
        vec_type: Vec2Type = Vec2Type.HOTSPOT,
        x: float = 0.5,
        y: float = 0.5,
        x_units: UnitsEnum = UnitsEnum.FRACTION,
        y_units: UnitsEnum = UnitsEnum.FRACTION,
    ):
        super().__init__()
        self.name: str | None = None
        self.vec_type = vec_type
        self.x = x
        self.y = y
        self.x_units = x_units
        self.y_units = y_units

    @property
    def xml(self) -> etree.Element:
        """An XML representation of this object."""
        root = etree.Element(self.vec_type.value)
        root.attrib["x"] = str(self.x)
        root.attrib["y"] = str(self.y)
        root.attrib["xunits"] = self.x_units.value
        root.attrib["yunits"] = self.y_units.value
        return root

    def __eq__(self, other: object) -> bool:
        return (
            False
            if other is None
            else isinstance(other, Vec2)
            and self.name == other.name
            and self.x == other.x
            and self.y == other.y
            and self.x_units == other.x_units
            and self.y_units == other.y_units
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)
