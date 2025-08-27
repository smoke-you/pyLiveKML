"""Camera module."""

from typing import Sequence

from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import (
    GxViewerOption,
    Angle90,
    Angle180,
    AnglePos180,
    Angle360,
    AltitudeMode,
    ArgParser,
    NoParse,
    DumpDirect,
)
from pyLiveKML.KML.KMLObjects.AbstractView import AbstractView
from pyLiveKML.KML.KMLObjects.TimePrimitive import TimePrimitive


class Camera(AbstractView):
    """A KML 'Camera', per https://developers.google.com/kml/documentation/kmlreference#camera."""

    _kml_type = "Camera"
    _kml_fields = (
        ArgParser("longitude", Angle180, "longitude", DumpDirect),
        ArgParser("latitude", Angle90, "latitude", DumpDirect),
        ArgParser("altitude", NoParse, "altitude", DumpDirect),
        ArgParser("heading", Angle360, "heading", DumpDirect),
        ArgParser("tilt", AnglePos180, "tilt", DumpDirect),
        ArgParser("roll", Angle180, "roll", DumpDirect),
        ArgParser("altitude_mode", NoParse, "altitudeMode", DumpDirect),
    )

    def __init__(
        self,
        viewer_options: Sequence[GxViewerOption] | GxViewerOption | None = None,
        time_primitive: TimePrimitive | None = None,
        longitude: float = 0,
        latitude: float = 0,
        altitude: float = 0,
        heading: float = 0,
        tilt: float = 0,
        roll: float = 0,
        altitude_mode: AltitudeMode | None = None,
    ):
        """LookAt instance constructor."""
        AbstractView.__init__(self, viewer_options, time_primitive)
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = altitude
        self.heading = heading
        self.tilt = tilt
        self.roll = roll
        self.altitude_mode = (
            AltitudeMode.CLAMP_TO_GROUND if altitude_mode is None else altitude_mode
        )

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        etree.SubElement(root, "longitude").text = f"{self.longitude:0.6f}"
        etree.SubElement(root, "latitude").text = f"{self.latitude:0.6f}"
        etree.SubElement(root, "altitude").text = f"{self.altitude:0.1f}"
        etree.SubElement(root, "heading").text = f"{self.heading:0.3f}"
        etree.SubElement(root, "tilt").text = f"{self.tilt:0.3f}"
        etree.SubElement(root, "roll").text = f"{self.roll:0.1f}"
        etree.SubElement(root, "altitudeMode").text = self.altitude_mode.value
