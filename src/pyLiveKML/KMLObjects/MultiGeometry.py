"""MultiGeometry module."""

from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML.KMLObjects.Geometry import Geometry
from pyLiveKML.KML.Object import _ListObject


class MultiGeometry(_ListObject[Geometry], Geometry):
    """A KML 'MultiGeometry', per https://developers.google.com/kml/documentation/kmlreference#multigeometry."""

    _kml_tag = "MultiGeometry"

    def __init__(self, contents: Geometry | Iterable[Geometry] | None = None):
        """Folder instance constructor."""
        Geometry.__init__(self)
        _ListObject[Geometry].__init__(self)
        if contents is not None:
            if isinstance(contents, Geometry):
                self.append(contents)
            else:
                self.extend(contents)
