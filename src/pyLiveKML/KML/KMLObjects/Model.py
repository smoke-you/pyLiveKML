"""Model module."""

from typing import Any, Iterator, Sequence
from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import (
    AltitudeMode,
    Angle90,
    Angle180,
    AnglePos180,
    Angle360,
    ArgParser,
    NoParse,
    DumpDirect,
)
from pyLiveKML.KML.KMLObjects.Link import Link
from pyLiveKML.KML.KMLObjects.Object import Object, ObjectChild


class Location(Object):
    """Specifies the exact coordinates of the Model's origin in latitude, longitude, and altitude."""

    _kml_type = "Location"
    _kml_fields = (
        ArgParser("longitude", Angle180, "longitude", DumpDirect,),
        ArgParser("latitude", Angle90, "latitude", DumpDirect,),
        ArgParser("altitude", NoParse, "altitude", DumpDirect,),
    )

    def __init__(
        self,
        longitude: float = 0,
        latitude: float = 0,
        altitude: float = 0,
    ):
        """Location instance constructor."""
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = altitude

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        etree.SubElement(root, "longitude").text = f"{self.longitude:0.6f}"
        etree.SubElement(root, "latitude").text = f"{self.latitude:0.6f}"
        etree.SubElement(root, "altitude").text = f"{self.altitude:0.1f}"


class Orientation(Object):
    """Describes rotation of a 3D model's coordinate system to position the object in Google Earth."""

    _kml_type = "Location"
    _kml_fields = (
        ArgParser("heading", Angle360, "heading", DumpDirect,),
        ArgParser("tilt", AnglePos180, "tilt", DumpDirect,),
        ArgParser("roll", Angle180, "roll", DumpDirect,),
    )

    def __init__(
        self,
        heading: float = 0,
        tilt: float = 0,
        roll: float = 0,
    ):
        """Location instance constructor."""
        self.heading = heading
        self.tilt = tilt
        self.roll = roll

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        etree.SubElement(root, "heading").text = f"{self.heading:0.3f}"
        etree.SubElement(root, "tilt").text = f"{self.tilt:0.3f}"
        etree.SubElement(root, "roll").text = f"{self.roll:0.3f}"


class Scale(Object):
    """Scales a model along the x, y, and z axes in the model's coordinate space."""

    _kml_type = "Scale"
    _kml_fields = (
        ArgParser("x", NoParse, "x", DumpDirect,),
        ArgParser("y", NoParse, "y", DumpDirect,),
        ArgParser("z", NoParse, "z", DumpDirect,),
    )

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        z: float = 0,
    ):
        """Scale instance constructor."""
        self.x = x
        self.y = y
        self.z = z

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        etree.SubElement(root, "x").text = str(self.x)
        etree.SubElement(root, "y").text = str(self.y)
        etree.SubElement(root, "z").text = str(self.z)


class Alias(Object):
    """<Alias> contains a mapping from a <sourceHref> to a <targetHref>."""

    _kml_type = "Alias"
    _kml_fields = (
        ArgParser("target_href", NoParse, "targetHref", DumpDirect,),
        ArgParser("source_href", NoParse, "sourceHref", DumpDirect,),
    )

    def __init__(
        self,
        target_href: str,
        source_href: str,
    ):
        """Alias instance constructor."""
        self.target_href = target_href
        self.source_href = source_href

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        etree.SubElement(root, "target_href").text = self.target_href
        etree.SubElement(root, "source_href").text = self.source_href


class Model(Object):
    """A KML 'Model', per https://developers.google.com/kml/documentation/kmlreference#model."""

    _kml_type = "Model"

    def __init__(
        self,
        link: Link,
        altitude_mode: AltitudeMode | None = None,
        longitude: float = 0,
        latitude: float = 0,
        altitude: float = 0,
        heading: float = 0,
        tilt: float = 0,
        roll: float = 0,
        x: float = 0,
        y: float = 0,
        z: float = 0,
        resource_map: Sequence[Alias] | Alias | None = None,
    ) -> None:
        """Model instance constructor."""
        Object.__init__(self)
        self.link = link
        altitude_mode = (
            AltitudeMode.CLAMP_TO_GROUND if altitude_mode is None else altitude_mode
        )
        self.altitude_mode: AltitudeMode = altitude_mode
        self.location: Location = Location(longitude, latitude, altitude)
        self.orientation: Orientation = Orientation(heading, tilt, roll)
        self.scale: Scale = Scale(x, y, z)
        self.resource_map: list[Alias] = []
        if resource_map is not None:
            if isinstance(resource_map, Alias):
                self.resource_map.append(resource_map)
            else:
                self.resource_map.extend(resource_map)

    def __setattr__(self, name: str, value: Any) -> None:
        """Model setattr method."""
        if name == "altitude_mode":
            if self.altitude_mode != value:
                self.altitude_mode = value
                self.field_changed()
        elif name == "link":
            raise KeyError(
                "Not permitted to assign a new Link; update the existing one instead."
            )
        elif name == "location":
            raise KeyError(
                "Not permitted to assign a new Location; update the existing one instead."
            )
        elif name == "orientation":
            raise KeyError(
                "Not permitted to assign a new Orientation; update the existing one instead."
            )
        elif name == "scale":
            raise KeyError(
                "Not permitted to assign a new Scale; update the existing one instead."
            )
        elif name == "resource_map":
            raise KeyError(
                "Not permitted to assign a new ResourceMap; update the existing one instead."
            )
        super().__setattr__(name, value)

    @property
    def children(self) -> Iterator[ObjectChild]:
        """The children of the instance."""
        yield ObjectChild(self, self.location)
        yield ObjectChild(self, self.orientation)
        yield ObjectChild(self, self.scale)
        yield ObjectChild(self, self.link)
        for r in self.resource_map:
            yield ObjectChild(parent=self, child=r)

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        etree.SubElement(root, "altitudeMode").text = self.altitude_mode.value
        root.append(self.location.construct_kml())
        root.append(self.orientation.construct_kml())
        root.append(self.scale.construct_kml())
        root.append(self.link.construct_kml())
        if with_children:
            if self.resource_map:
                rm = etree.SubElement(root, "ResourceMap")
                for r in self.resource_map:
                    rm.append(r.construct_kml())
