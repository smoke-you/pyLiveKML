"""Track module."""

from datetime import datetime
from typing import Iterator, Iterable, Any

from dateutil.parser import parse as dtparse
from lxml import etree  # type: ignore

from pyLiveKML.types import AltitudeModeEnum
from pyLiveKML.objects.Object import (
    _ChildDef,
    _FieldDef,
    Angle180,
    Angle360,
    Angle90,
    AnglePos180,
)
from pyLiveKML.errors import TrackElementsMismatch
from pyLiveKML.utils import with_ns
from pyLiveKML.objects.Geometry import Geometry
from pyLiveKML.objects.Model import Model


class TrackCoord:
    """Coordinates class, specific to the <gx:Track> KML tag."""

    def __init__(
        self,
        longitude: float = 0,
        latitude: float = 0,
        altitude: float = 0,
    ):
        """TrackCoord instance constructor."""
        super().__init__()
        self.longitude = Angle180.parse(longitude)
        self.latitude = Angle90.parse(latitude)
        self.altitude = altitude

    def __str__(self) -> str:
        """Return a string representation."""
        return f"{self.longitude} {self.latitude} {self.altitude}"


class TrackAngles:
    """Angles (heading/tilt/roll) class, specific to the <gx:Track> KML tag."""

    def __init__(
        self,
        heading: float = 0,
        tilt: float = 0,
        roll: float = 0,
    ) -> None:
        """TrackAngles instance constructor."""
        super().__init__()
        self.heading = Angle360.parse(heading)
        self.tilt = AnglePos180.parse(tilt)
        self.roll = Angle180.parse(roll)

    def __str__(self) -> str:
        """Return a string representation."""
        return f"{self.heading} {self.tilt} {self.roll}"


class TrackElement:
    """Track element class, specific to the <gx:Track> KML tag.

    Used to collect the various components of each track point that are then distributed
    across the <gx:Track> tag.
    """

    def __init__(
        self,
        when: datetime | str,
        coords: TrackCoord | tuple[float, ...] | None,
        angles: TrackAngles | tuple[float, ...] | None,
        extended_data: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        """TrackElement instance constructor."""
        super().__init__()
        if isinstance(when, datetime):
            self.when = when
        else:
            self.when = dtparse(when)
        self.coords: TrackCoord | None = None
        if coords is None or isinstance(coords, TrackCoord):
            self.coords = coords
        else:
            self.coords = TrackCoord(*coords)
        self.angles: TrackAngles | None = None
        if angles is None or isinstance(angles, TrackAngles):
            self.angles = angles
        else:
            self.angles = TrackAngles(*angles)
        self.extended_data = extended_data


class Track(Geometry):
    """A KML 'gx:Track', per https://developers.google.com/kml/documentation/kmlreference#gxtrack."""

    _kml_tag = "gx:Track"
    _kml_fields = Geometry._kml_fields + (
        _FieldDef("altitude_mode", "gx:altitudeMode"),
    )
    _kml_children = Geometry._kml_children + (_ChildDef("model"),)

    def __init__(
        self,
        altitude_mode: AltitudeModeEnum | None = None,
        elements: TrackElement | Iterable[TrackElement] | None = None,
        model: Model | None = None,
    ) -> None:
        """Track instance constructor."""
        Geometry.__init__(self)
        self.altitude_mode = altitude_mode
        self.model = model
        self._schemas = dict[str, set[str]]()
        self._elements = list[TrackElement]()
        self.elements = elements

    @property
    def elements(self) -> Iterator[TrackElement]:
        """Retrieve a generator over the set of enclosed `TrackElements`."""
        yield from self._elements

    @elements.setter
    def elements(self, value: TrackElement | Iterable[TrackElement] | None) -> None:
        self._elements.clear()
        self._schemas.clear()
        if value is None:
            return
        if isinstance(value, TrackElement):
            self._elements.append(value)
        else:
            xdlens = set[int]()
            for e in value:
                if e.extended_data is None:
                    xdlens.add(0)
                else:
                    for fname in e.extended_data.values():
                        for fval in fname.values():
                            xdlens.add(0 if fval is None else len(fval))
            if len(xdlens) != 1:
                raise TrackElementsMismatch()
            self._elements.extend(value)
            for xd in (
                e.extended_data for e in self._elements if e.extended_data is not None
            ):
                for schema, fields in xd.items():
                    if schema not in self._schemas:
                        self._schemas[schema] = set[str]()
                    self._schemas[schema].update(fields.keys())

    def build_kml(
        self,
        root: etree.Element,
        with_children: bool = True,
        with_dependents: bool = True,
    ) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        value: str
        for e in self.elements:
            etree.SubElement(root, with_ns("when")).text = e.when.isoformat()
        for e in self.elements:
            value = "" if e.coords is None else str(e.coords)
            etree.SubElement(root, with_ns("gx:coord")).text = value
        for e in self.elements:
            value = "" if e.angles is None else str(e.angles)
            etree.SubElement(root, with_ns("gx:angles")).text = value
        if self._schemas:
            e_xd = etree.SubElement(root, "ExtendedData")
            for sch, fields in self._schemas.items():
                e_sch = etree.SubElement(e_xd, "SchemaData", attrib={"schemaUrl": sch})
                for f in sorted(fields):
                    e_field = etree.SubElement(
                        e_sch,
                        with_ns("gx:SimpleArrayData"),
                        attrib={with_ns("kml:name"): f},
                    )
                    for e in self.elements:
                        value = ""
                        if (
                            e.extended_data
                            and sch in e.extended_data
                            and f in e.extended_data[sch]
                            and e.extended_data[sch][f] is not None
                        ):
                            value = str(e.extended_data[sch][f])
                        etree.SubElement(e_field, with_ns("gx:value")).text = value
