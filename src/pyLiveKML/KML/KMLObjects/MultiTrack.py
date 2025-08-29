"""MultiTrack module."""

from typing import Iterator, Iterable

from lxml import etree  # type: ignore

from pyLiveKML.KML import AltitudeMode
from pyLiveKML.KML._BaseObject import _FieldDef, DumpDirect, NoParse
from pyLiveKML.KML.KMLObjects.Geometry import Geometry
from pyLiveKML.KML.KMLObjects.Object import ObjectChild
from pyLiveKML.KML.KMLObjects.Track import GxTrack


class MultiTrack(Geometry, list[GxTrack]):
    """A KML 'gx:MultiTrack', per https://developers.google.com/kml/documentation/kmlreference#gxmultitrack."""

    _kml_type = "gx:MultiTrack"
    _kml_fields = Geometry._kml_fields + (
        _FieldDef("altitude_mode", NoParse, "altitudeMode", DumpDirect),
        _FieldDef("interpolate", NoParse, "gx:interpolate", DumpDirect),
    )

    def __init__(
        self,
        altitude_mode: AltitudeMode | None = None,
        interpolate: bool = False,
        tracks: GxTrack | Iterable[GxTrack] | None = None,
    ) -> None:
        """Track instance constructor."""
        Geometry.__init__(self)
        self.altitude_mode = altitude_mode
        self.interpolate = interpolate
        if tracks is not None:
            if isinstance(tracks, GxTrack):
                self.append(tracks)
            else:
                self.extend(tracks)

    @property
    def children(self) -> Iterator[ObjectChild]:
        """The children of the instance."""
        for t in self:
            yield ObjectChild(parent=self, child=t)

    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        if with_children:
            for t in self:
                root.append(t.construct_kml())
