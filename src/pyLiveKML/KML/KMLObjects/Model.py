"""Model module."""

from typing import Sequence

from lxml import etree  # type: ignore

from pyLiveKML.KML import AltitudeModeEnum
from pyLiveKML.KML._BaseObject import (
    _BaseObject,
    _FieldDef,
    Angle90,
    Angle180,
    AnglePos180,
    Angle360,
    DumpDirect,
    NoParse,
)
from pyLiveKML.KML.KMLObjects.Link import Link
from pyLiveKML.KML.KMLObjects.Object import Object


class Location(_BaseObject):
    """Specifies the exact coordinates of the Model's origin in latitude, longitude, and altitude."""

    _kml_tag = "Location"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("longitude", Angle180, "longitude", DumpDirect),
        _FieldDef("latitude", Angle90, "latitude", DumpDirect),
        _FieldDef("altitude", NoParse, "altitude", DumpDirect),
    )

    def __init__(
        self,
        longitude: float = 0,
        latitude: float = 0,
        altitude: float = 0,
    ):
        """Location instance constructor."""
        super().__init__()
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = altitude


class Orientation(_BaseObject):
    """Describes rotation of a 3D model's coordinate system to position the object in Google Earth."""

    _kml_tag = "Location"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("heading", Angle360, "heading", DumpDirect),
        _FieldDef("tilt", AnglePos180, "tilt", DumpDirect),
        _FieldDef("roll", Angle180, "roll", DumpDirect),
    )

    def __init__(
        self,
        heading: float = 0,
        tilt: float = 0,
        roll: float = 0,
    ):
        """Location instance constructor."""
        super().__init__()
        self.heading = heading
        self.tilt = tilt
        self.roll = roll


class Scale(_BaseObject):
    """Scales a model along the x, y, and z axes in the model's coordinate space."""

    _kml_tag = "Scale"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("x", NoParse, "x", DumpDirect),
        _FieldDef("y", NoParse, "y", DumpDirect),
        _FieldDef("z", NoParse, "z", DumpDirect),
    )

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        z: float = 0,
    ):
        """Scale instance constructor."""
        super().__init__()
        self.x = x
        self.y = y
        self.z = z


class Alias(_BaseObject):
    """<Alias> contains a mapping from a <sourceHref> to a <targetHref>."""

    _kml_tag = "Alias"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("target_href", NoParse, "targetHref", DumpDirect),
        _FieldDef("source_href", NoParse, "sourceHref", DumpDirect),
    )

    def __init__(
        self,
        target_href: str,
        source_href: str,
    ):
        """Alias instance constructor."""
        super().__init__()
        self.target_href = target_href
        self.source_href = source_href


class ResourceMap(_BaseObject):
    """<ResourceMap> contains a list of <Alias> objects."""

    _kml_tag = "ResourceMap"

    def __init__(self, resources: Sequence[Alias] | Alias | None = None) -> None:
        """ResourceMap instance constructor."""
        super().__init__()
        self.resources = list[Alias]()
        if resources is not None:
            if isinstance(resources, Alias):
                self.resources.append(resources)
            else:
                self.resources.extend(resources)

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        for r in self.resources:
            root.append(r.construct_kml())


class Model(Object):
    """A KML 'Model', per https://developers.google.com/kml/documentation/kmlreference#model."""

    _kml_tag = "Model"
    _kml_fields = Object._kml_fields + (
        _FieldDef("altitude_mode", NoParse, "altitudeMode", DumpDirect),
    )
    _direct_children = Object._direct_children + (
        "link",
        "location",
        "orientation",
        "scale",
        "resources",
    )

    def __init__(
        self,
        link: Link,
        altitude_mode: AltitudeModeEnum | None = None,
        longitude: float = 0,
        latitude: float = 0,
        altitude: float = 0,
        heading: float = 0,
        tilt: float = 0,
        roll: float = 0,
        x: float = 0,
        y: float = 0,
        z: float = 0,
        resources: Sequence[Alias] | Alias | None = None,
    ) -> None:
        """Model instance constructor."""
        Object.__init__(self)
        self.link = link
        altitude_mode = (
            AltitudeModeEnum.CLAMP_TO_GROUND if altitude_mode is None else altitude_mode
        )
        self.altitude_mode = altitude_mode
        self.location = Location(longitude, latitude, altitude)
        self.orientation = Orientation(heading, tilt, roll)
        self.scale = Scale(x, y, z)
        self.resources = ResourceMap(resources)
