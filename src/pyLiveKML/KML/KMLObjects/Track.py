"""Track module."""

from datetime import datetime
from typing import Iterator, Iterable

from lxml import etree  # type: ignore

from pyLiveKML import with_ns
from pyLiveKML.KML import GxAltitudeModeEnum
from pyLiveKML.KML._BaseObject import (
    _FieldDef,
    Angle180,
    Angle360,
    Angle90,
    AnglePos180,
)
from pyLiveKML.KML.KMLObjects.Model import Model
from pyLiveKML.KML.KMLObjects.Geometry import Geometry
from pyLiveKML.KML.KMLObjects.Object import ObjectChild


class TrackCoord:
    """Coordinates class, specific to the <gx:Track> KML tag."""

    def __init__(
        self,
        longitude: float = 0,
        latitude: float = 0,
        altitude: float = 0,
        empty: bool = False,
    ):
        """TrackCoord instance constructor."""
        super().__init__()
        self.longitude = Angle180.parse(longitude)
        self.latitude = Angle90.parse(latitude)
        self.altitude = altitude
        self.empty = empty

    def __str__(self) -> str:
        """Return a string representation."""
        return "" if self.empty else f"{self.longitude} {self.latitude} {self.altitude}"


class TrackAngles:
    """Angles (heading/tilt/roll) class, specific to the <gx:Track> KML tag."""

    def __init__(
        self,
        heading: float = 0,
        tilt: float = 0,
        roll: float = 0,
        empty: bool = False,
    ) -> None:
        """TrackAngles instance constructor."""
        super().__init__()
        self.heading = Angle360.parse(heading)
        self.tilt = AnglePos180.parse(tilt)
        self.roll = Angle180.parse(roll)
        self.empty = empty

    def __str__(self) -> str:
        """Return a string representation."""
        return "" if self.empty else f"{self.heading} {self.tilt} {self.roll}"


class TrackExtendedData:
    """Extended data class, specific to the <gx:Track> KML tag."""

    def __init__(self, schema_url: str, data: dict[str, str]) -> None:
        """TrackExtendedData instance constructor."""
        self.schema_url = schema_url
        self.data = data


class TrackElement:
    """Track element class, specific to the <gx:Track> KML tag.

    Used to collect the various components of each track point that are then distributed
    across the <gx:Track> tag.
    """

    def __init__(
        self,
        when: datetime,
        coords: TrackCoord,
        angles: TrackAngles,
        extended_data: TrackExtendedData | None = None,
    ) -> None:
        """TrackElement instance constructor."""
        super().__init__()
        self.when = when
        self.coords = coords
        self.angles = angles
        self.extended_data = extended_data


class GxTrack(Geometry):
    """A KML 'gx:Track', per https://developers.google.com/kml/documentation/kmlreference#gxtrack."""

    _kml_tag = "gx:Track"
    _kml_fields = Geometry._kml_fields + (
        _FieldDef("altitude_mode", "gx:altitudeMode"),
    )
    _direct_children = Geometry._direct_children + ("model",)

    def __init__(
        self,
        altitude_mode: GxAltitudeModeEnum | None = None,
        elements: TrackElement | Iterable[TrackElement] | None = None,
        model: Model | None = None,
    ) -> None:
        """Track instance constructor."""
        Geometry.__init__(self)
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
        """The children of the instance."""
        if self.model:
            yield ObjectChild(self, self.model)

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        for e in self.elements:
            etree.SubElement(root, with_ns("when")).text = e.when.isoformat()
        for e in self.elements:
            etree.SubElement(root, with_ns("gx:coord")).text = str(e.coords)
        for e in self.elements:
            etree.SubElement(root, with_ns("gx:angles")).text = str(e.angles)

        # TODO: fix this, just... fix it
        # Under each <SchemaData> tag, it needs to create one <gx:SimpleDataArray> tag
        # for each key in the TrackExtendedData.data dict.
        # Under each <gx:SimpleDataArray> tag, it needs to create one <gx:value> tag
        # for each TrackElement in self. The tags that have a corresponding schema and
        # array should contain the corresponding value from the TrackExtendedData.dict,
        # while the tags that do not have corresponding parents should contain empty
        # strings.
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
                    xchroot,
                    with_ns("gx:SimpleArrayData"),
                    attrib={with_ns("kml:name"): kn},
                )
                for v in kv:
                    etree.SubElement(knroot, with_ns("gx:value")).text = v
