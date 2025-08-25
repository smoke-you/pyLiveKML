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
)
from pyLiveKML.KML.KMLObjects.AbstractView import AbstractView
from pyLiveKML.KML.KMLObjects.TimePrimitive import TimePrimitive


class Camera(AbstractView):
    """A KML 'Camera', per https://developers.google.com/kml/documentation/kmlreference#camera."""

    _kml_type = "Camera"

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
        self._longitude = Angle180(longitude)
        self._latitude = Angle90(latitude)
        self._altitude = altitude
        self._heading = Angle360(heading)
        self._tilt = AnglePos180(tilt)
        self._roll = Angle180(roll)
        self._altitude_mode = AltitudeMode.CLAMP_TO_GROUND
        self.altitude_mode = altitude_mode

    @property
    def longitude(self) -> float:
        """Longitude of the point the camera is looking at."""
        return float(self._longitude)

    @longitude.setter
    def longitude(self, value: float) -> None:
        if self._longitude != value:
            self._longitude = Angle180(value)
            self.field_changed()

    @property
    def latitude(self) -> float:
        """Latitude of the point the camera is looking at."""
        return float(self._latitude)

    @latitude.setter
    def latitude(self, value: float) -> None:
        if self._latitude != value:
            self._latitude = Angle90(value)
            self.field_changed()

    @property
    def altitude(self) -> float:
        """Distance from the earth's surface, in meters.

        Interpreted according to the LookAt's altitude mode.
        """
        return float(self._altitude)

    @altitude.setter
    def altitude(self, value: float) -> None:
        if self._altitude != value:
            self._altitude = value
            self.field_changed()

    @property
    def heading(self) -> float:
        """Direction (that is, North, South, East, West), in degrees."""
        return float(self._heading)

    @heading.setter
    def heading(self, value: float) -> None:
        if self._heading != value:
            self._heading = Angle360(value)
            self.field_changed()

    @property
    def tilt(self) -> float:
        """Angle between the direction of the LookAt position and the normal to the surface of the earth."""
        return float(self._tilt)

    @tilt.setter
    def tilt(self, value: float) -> None:
        if self._tilt != value:
            self._tilt = AnglePos180(value)
            self.field_changed()

    @property
    def roll(self) -> float:
        """Distance in meters from the point specified by <longitude>, <latitude>, and <altitude> to the LookAt position."""
        return float(self._roll)

    @roll.setter
    def roll(self, value: float) -> None:
        if self._roll != value:
            self._roll = Angle180(value)
            self.field_changed()

    @property
    def altitude_mode(self) -> AltitudeMode:
        """Specifies how the <altitude> specified for the LookAt point is interpreted."""
        return self._altitude_mode

    @altitude_mode.setter
    def altitude_mode(self, value: AltitudeMode | None) -> None:
        value = AltitudeMode.CLAMP_TO_GROUND if value is None else value
        if value != self._altitude_mode:
            self._altitude_mode = value
            self.field_changed()

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
