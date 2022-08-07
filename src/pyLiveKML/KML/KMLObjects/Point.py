from typing import Optional
from lxml import etree

from ..GeoCoordinates import GeoCoordinates
from ..KML import AltitudeMode
from .Geometry import Geometry


class Point(Geometry):
    """A Point geometry, as per https://developers.google.com/kml/documentation/kmlreference#point.
    :class:`~pyLiveKML.KML.KMLObjects.Point` objects define a simple geographic location, described a longitude,
    latitude and optional altitude.

    :param GeoCoordinates coordinates: A :class:`~pyLiveKML.KML.GeoCoordinates` object that defines the longitude,
        latitude and optional altitude of the :class:`~pyLiveKML.KML.KMLObjects.Point`.
    :param Optional[bool] extrude: An (optional) flag to indicate whether the :class:`~pyLiveKML.KML.KMLObjects.Point`
        should be shown in GEP connected to the ground with a vertical line.
    :param Optional[bool] altitude_mode: The (optional) :class:`~pyLiveKML.KML.KML.AltitudeMode` that will be applied
        to the :class:`~pyLiveKML.KML.KMLObjects.Point` by GEP.
    """

    @property
    def kml_type(self) -> str:
        """Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set the KML tag name to
        'Point'
        """
        return 'Point'

    @property
    def extrude(self) -> Optional[bool]:
        """True if a vertical line (using the current :class:`~pyLiveKML.KML.KMLObjects.LineStyle`) connects the
        :class:`~pyLiveKML.KML.KMLObjects.Point` to the ground in GEP, False otherwise.  None implies False.
        """
        return self._extrude

    @extrude.setter
    def extrude(self, value: Optional[bool]):
        if self._extrude != value:
            self._extrude = value
            self.field_changed()

    @property
    def altitude_mode(self) -> Optional[AltitudeMode]:
        """An :class:`~pyLiveKML.KML.KML.AltitudeMode` instance that defines how GEP displays the
        :class:`~pyLiveKML.KML.KMLObjects.Point` and treats its' altitude.
        """
        return self._altitude_mode

    @altitude_mode.setter
    def altitude_mode(self, value: Optional[AltitudeMode]):
        if self._altitude_mode != value:
            self._altitude_mode = value
            self.field_changed()

    @property
    def coordinates(self) -> GeoCoordinates:
        """A :class:`~pyLiveKML.KML.GeoCoordinates` object that defines the longitude, latitude and optional altitude
        of the :class:`~pyLiveKML.KML.KMLObjects.Point`.
        """
        return self._coordinates

    @coordinates.setter
    def coordinates(self, value: GeoCoordinates):
        self._coordinates = value
        self.field_changed()

    def build_kml(self, root: etree.Element, with_children=True):
        if self.extrude is not None:
            etree.SubElement(root, 'visibility').text = str(int(self.extrude))
        if self.altitude_mode is not None:
            etree.SubElement(root, 'altitudeMode').text = self.altitude_mode.value
        etree.SubElement(root, 'coordinates').text = self.coordinates.__str__()

    def __init__(
        self,
        coordinates: GeoCoordinates,
        extrude: Optional[bool] = None,
        altitude_mode: Optional[AltitudeMode] = None
    ):
        Geometry.__init__(self)
        self._coordinates: GeoCoordinates = coordinates
        self._extrude = extrude
        self._altitude_mode = altitude_mode

    def __str__(self):
        return f'{self.kml_type}'

    def __repr__(self):
        return self.__str__()
