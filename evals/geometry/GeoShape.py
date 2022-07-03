from abc import ABC
from typing import Optional

import numpy
from pyproj import Geod
from scipy.spatial.transform import Rotation

from geography import project_shape
from pyLiveKML.KML.GeoCoordinates import GeoCoordinates
from pyLiveKML.KML.KML import AltitudeMode
from pyLiveKML.KML.KMLObjects.LineStyle import LineStyle
from pyLiveKML.KML.KMLObjects.LinearRing import LinearRing
from pyLiveKML.KML.KMLObjects.Placemark import Placemark
from pyLiveKML.KML.KMLObjects.PolyStyle import PolyStyle
from pyLiveKML.KML.KMLObjects.Polygon import Polygon
from pyLiveKML.KML.KMLObjects.Style import Style


class GeoShape(Placemark, ABC):

    @property
    def polygon(self) -> Polygon:
        return self.geometry

    def rotate_shape(self, r: Rotation):
        self._outer_bound_3d = r.apply(self._outer_bound_3d)
        if self._inner_bounds_3d:
            for b in self._inner_bounds_3d:
                b = r.apply(b)
        self._rebuild()

    def translate_on_surface(self, bearing: float, distance: float):
        self._origin.lon, self._origin.lat, _ = Geod(ellps='WGS84')\
            .fwd(self._origin.lon, self._origin.lat, bearing, distance)
        self._rebuild()

    def _rebuild(self):
        bo, bi = self.build()
        """It's not possible to change the boundary LinearRing objects, but changing their coordinates is OK"""
        self.polygon.outer_boundary.coordinates = bo
        # self.polygon.outer_boundary.field_changed()
        for i, b in enumerate(self.polygon.inner_boundaries):
            b.coordinates = bi[i]
            # b.field_changed()

    def build(self) -> tuple[list[GeoCoordinates], list[list[GeoCoordinates]]]:
        g_outer = list(project_shape(self._outer_bound_3d, self._origin))
        g_inner = list[list[GeoCoordinates]]()
        if self._inner_bounds_3d:
            for b in self._inner_bounds_3d:
                g_inner.append(list(project_shape(b, self._origin)))
        return g_outer, g_inner

    def __init__(
            self,
            origin: GeoCoordinates,
            outer_bound: list[numpy.ndarray],
            inner_bounds: Optional[list[list[numpy.ndarray]]],
            border_width: float = 1.0,
            border_color: int = 0xffffffff,
            fill_color: int = 0xffffffff,
            name: str = None,
            selected: bool = False,
            altitude_mode: AltitudeMode = AltitudeMode.CLAMP_TO_GROUND,
    ):
        self._origin = origin
        self._outer_bound_3d = outer_bound
        self._inner_bounds_3d = inner_bounds
        g_outer, g_inner = self.build()
        Placemark.__init__(
            self,
            name=name,
            inline_style=Style(
                line_style=LineStyle(width=border_width, color=border_color),
                poly_style=PolyStyle(color=fill_color)
            ),
            geometry=Polygon(
                outer_boundary=LinearRing(coordinates=g_outer),
                inner_boundaries=[LinearRing(coordinates=g) for g in g_inner],
                altitude_mode=altitude_mode,
            ),
        )
        ABC.__init__(self)
        self.select(selected)
