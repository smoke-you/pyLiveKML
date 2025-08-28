"""Track module."""

from datetime import datetime
from typing import Iterator, Iterable
from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import (
    AltitudeMode,
    Angle90,
    Angle180,
    AnglePos180,
    Angle360,
    _FieldDef,
    NoParse,
    DumpDirect,
)
from pyLiveKML.KML.KMLObjects.Model import Model
from pyLiveKML.KML.KMLObjects.Geometry import Geometry
from pyLiveKML.KML.KMLObjects.Object import Object, ObjectChild


class TrackCoord:

    def __init__(
        self,
        longitude: float = 0,
        latitude: float = 0,
        altitude: float = 0,
        empty: bool = False,
    ):
        super().__init__()
        self.longitude = Angle180.parse(longitude)
        self.latitude = Angle90.parse(latitude)
        self.altitude = altitude
        self.empty = empty

    def __str__(self) -> str:
        return "" if self.empty else f"{self.longitude} {self.latitude} {self.altitude}"


class TrackAngles:

    def __init__(
        self,
        heading: float = 0,
        tilt: float = 0,
        roll: float = 0,
        empty: bool = False,
    ) -> None:
        super().__init__()
        self.heading = Angle360.parse(heading)
        self.tilt = AnglePos180.parse(tilt)
        self.roll = Angle180.parse(roll)
        self.empty = empty

    def __str__(self) -> str:
        return "" if self.empty else f"{self.heading} {self.tilt} {self.roll}"


class TrackExtendedData:

    def __init__(self, schema_url: str, data: dict[str, str]) -> None:
        self.schema_url = schema_url
        self.data = data


class TrackElement:

    def __init__(
        self,
        when: datetime,
        coords: TrackCoord,
        angles: TrackAngles,
        extended_data: TrackExtendedData | None = None,
    ) -> None:
        super().__init__()
        self.when = when
        self.coords = coords
        self.angles = angles
        self.extended_data = extended_data


class Track(Geometry):
    """A KML 'gx:Track', per https://developers.google.com/kml/documentation/kmlreference#model."""

    _kml_type = "gx:Track"
    _fields = (_FieldDef("altitude_mode", NoParse, "altitudeMode", DumpDirect),)
    _direct_children = ("model",)

    def __init__(
        self,
        altitude_mode: AltitudeMode | None = None,
        elements: TrackElement | Iterable[TrackElement] | None = None,
        model: Model | None = None,
    ) -> None:
        """Model instance constructor."""
        Object.__init__(self)
        self.altitude_mode = altitude_mode
        self.model = model
        self.elements = list[TrackElement]()
        if elements is not None:
            if isinstance(elements, TrackElement):
                self.elements.append(elements)
            else:
                self.elements.extend(elements)

    @property
    def children(self) -> Iterator[ObjectChild]:
        if self.model:
            yield ObjectChild(self, self.model)

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        super().build_kml(root, with_children)
        for e in self.elements:
            etree.SubElement(root, "when").text = e.when.isoformat()
        for e in self.elements:
            etree.SubElement(root, "gx:coord").text = str(e.coords)
        for e in self.elements:
            etree.SubElement(root, "gx:angles").text = str(e.angles)
        xdata = {
            schu: dict[str, list[str]]()
            for schu in sorted(
                {e.extended_data.schema_url for e in self.elements if e.extended_data}
            )
        }
        for txd in (e.extended_data for e in self.elements if e.extended_data):
            for txn, txv in txd.data.items():
                if txn not in xdata[txd.schema_url]:
                    xdata[txd.schema_url][txn] = list[str]()
                xdata[txd.schema_url][txn].append(txv)
        if not xdata:
            return
        xdroot = etree.SubElement(root, "ExtendedData")
        for xsch, xschd in xdata.items():
            xchroot = etree.SubElement(
                xdroot, "SchemaData", attrib={"schema_url": xsch}
            )
            for kn, kv in xschd.items():
                knroot = etree.SubElement(
                    xchroot, "gx:SimpleArrayData", attrib={"kml:name": kn}
                )
                for v in kv:
                    etree.SubElement(knroot, "gx:value").text = v
