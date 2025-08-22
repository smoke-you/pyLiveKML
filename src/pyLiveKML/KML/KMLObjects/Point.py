"""Point module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML.GeoCoordinates import GeoCoordinates
from pyLiveKML.KML.KML import AltitudeMode
from pyLiveKML.KML.KMLObjects.Geometry import Geometry


class Point(Geometry):
    """A Point geometry, as per https://developers.google.com/kml/documentation/kmlreference#point.

    :class:`~pyLiveKML.KML.KMLObjects.Point` objects define a simple geographic location, described a longitude,
    latitude and optional altitude.

    :param GeoCoordinates coordinates: A :class:`~pyLiveKML.KML.GeoCoordinates` object that defines the longitude,
        latitude and optional altitude of the :class:`~pyLiveKML.KML.KMLObjects.Point`.
    :param bool|None extrude: An (optional) flag to indicate whether the :class:`~pyLiveKML.KML.KMLObjects.Point`
        should be shown in GEP connected to the ground with a vertical line.
    :param bool|None altitude_mode: The (optional) :class:`~pyLiveKML.KML.KML.AltitudeMode` that will be applied
        to the :class:`~pyLiveKML.KML.KMLObjects.Point` by GEP.
    """

    def __init__(
        self,
        coordinates: GeoCoordinates,
        extrude: bool | None = None,
        altitude_mode: AltitudeMode | None = None,
    ):
        """Point instance constructor."""
        Geometry.__init__(self)
        self._coordinates: GeoCoordinates = coordinates
        self._extrude: bool | None = extrude
        self._altitude_mode: AltitudeMode | None = altitude_mode

    @property
    def kml_type(self) -> str:
        """The class' KML type string.

        Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set
        the KML tag name to 'Point'
        """
        return "Point"

    @property
    def extrude(self) -> bool | None:
        """Flag to indicate whether there should be a Point should be displayed with a line joining it to the ground.

        True if a vertical line (using the current :class:`~pyLiveKML.KML.KMLObjects.LineStyle`) connects the
        :class:`~pyLiveKML.KML.KMLObjects.Point` to the ground in GEP, False otherwise.  None implies False.
        """
        return self._extrude

    @extrude.setter
    def extrude(self, value: bool | None) -> None:
        if self._extrude != value:
            self._extrude = value
            self.field_changed()

    @property
    def altitude_mode(self) -> AltitudeMode | None:
        """The altitude mode of the Point instance.

        An :class:`~pyLiveKML.KML.KML.AltitudeMode` instance that defines how GEP displays the
        :class:`~pyLiveKML.KML.KMLObjects.Point` and treats its' altitude.
        """
        return self._altitude_mode

    @altitude_mode.setter
    def altitude_mode(self, value: AltitudeMode | None) -> None:
        if self._altitude_mode != value:
            self._altitude_mode = value
            self.field_changed()

    @property
    def coordinates(self) -> GeoCoordinates:
        """The latitude, longitude and (optionally) altitude of the Point instance.

        A :class:`~pyLiveKML.KML.GeoCoordinates` object that defines the longitude, latitude and optional altitude
        of the :class:`~pyLiveKML.KML.KMLObjects.Point`.
        """
        return self._coordinates

    @coordinates.setter
    def coordinates(self, value: GeoCoordinates) -> None:
        self._coordinates = value
        self.field_changed()

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        if self.extrude is not None:
            etree.SubElement(root, "visibility").text = str(int(self.extrude))
        if self.altitude_mode is not None:
            etree.SubElement(root, "altitudeMode").text = self.altitude_mode.value
        etree.SubElement(root, "coordinates").text = self.coordinates.__str__()

    def __str__(self) -> str:
        """Return a string representation."""
        return f"{self.kml_type}"

    def __repr__(self) -> str:
        """Return a debug representation."""
        return self.__str__()
