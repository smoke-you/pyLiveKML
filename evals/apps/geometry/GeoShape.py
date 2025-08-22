from abc import ABC
from typing import Optional, cast

import numpy
from pyproj import Geod
from pyLiveKML import (
    GeoCoordinates,
    AltitudeMode,
    LineStyle,
    LinearRing,
    Placemark,
    PolyStyle,
    Polygon,
    Style,
)
from scipy.spatial.transform import Rotation

from .geography import project_shape


class GeoShape(Placemark, ABC):

    def __init__(
        self,
        origin: GeoCoordinates,
        outer_bound: list[numpy.ndarray],
        inner_bounds: Optional[list[list[numpy.ndarray]]],
        border_width: float = 1.0,
        border_color: int = 0xFFFFFFFF,
        fill_color: int = 0xFFFFFFFF,
        name: Optional[str] = None,
        selected: bool = False,
        altitude_mode: AltitudeMode = AltitudeMode.CLAMP_TO_GROUND,
    ) -> None:
        self._origin = origin
        self._outer_bound_3d = outer_bound
        self._inner_bounds_3d = inner_bounds
        g_outer, g_inner = self.build()
        Placemark.__init__(
            self,
            name=name,
            inline_style=Style(
                line_style=LineStyle(width=border_width, color=border_color),
                poly_style=PolyStyle(color=fill_color),
            ),
            geometry=Polygon(
                outer_boundary=LinearRing(coordinates=g_outer),
                inner_boundaries=[LinearRing(coordinates=g) for g in g_inner],
                altitude_mode=altitude_mode,
            ),
        )
        ABC.__init__(self)
        self.select(selected)

    @property
    def polygon(self) -> Polygon:
        return cast(Polygon, self.geometry)

    def rotate_shape(self, r: Rotation) -> None:
        self._outer_bound_3d = r.apply(self._outer_bound_3d)
        if self._inner_bounds_3d:
            for b in self._inner_bounds_3d:
                b = r.apply(b)
        self._rebuild()

    def translate_on_surface(self, bearing: float, distance: float) -> None:
        self._origin.lon, self._origin.lat, _ = Geod(ellps="WGS84").fwd(
            self._origin.lon, self._origin.lat, bearing, distance
        )
        self._rebuild()

    @property
    def origin(self) -> GeoCoordinates:
        return self._origin

    @origin.setter
    def origin(self, coords: GeoCoordinates) -> None:
        self._origin.lon = coords.lon
        self._origin.lat = coords.lat
        self._origin.alt = coords.alt
        self._rebuild()

    def _rebuild(self) -> None:
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

    @property
    def fill_rgb(self) -> str:
        try:
            styles = [s for s in self.styles if isinstance(s, Style)]
            c = cast(int, cast(PolyStyle, styles[0].poly_style).color)
            r = c & 0xFF
            g = (c & 0xFF00) >> 8
            b = (c & 0xFF0000) >> 16
            return f"{r:02x}{g:02x}{b:02x}"
        except Exception:
            pass
        return "000000"

    @fill_rgb.setter
    def fill_rgb(self, val: str) -> None:
        try:
            c = int(val, 16)
            new_c = ((c & 0xFF0000) >> 16) + (c & 0xFF00) + ((c & 0xFF) << 16)
            styles = [s for s in self.styles if isinstance(s, Style)]
            for s in styles:
                cast(PolyStyle, s.poly_style).color = (
                    cast(int, cast(PolyStyle, s.poly_style).color) & 0xFF000000
                ) + new_c
        except Exception:
            pass

    @property
    def fill_alpha(self) -> int:
        try:
            styles = [s for s in self.styles if isinstance(s, Style)]
            if styles:
                return (
                    cast(int, cast(PolyStyle, styles[0].poly_style).color) & 0xFF000000
                ) >> 24
        except Exception:
            pass
        return 0

    @fill_alpha.setter
    def fill_alpha(self, val: int) -> None:
        try:
            a = int(val)
            a = 0 if val < 0 else 255 if val > 255 else val
            styles = [s for s in self.styles if isinstance(s, Style)]
            for s in styles:
                cast(PolyStyle, s.poly_style).color = (
                    cast(int, cast(PolyStyle, s.poly_style).color) & 0xFFFFFF
                ) + ((a & 0xFF) << 24)
        except Exception:
            pass

    @property
    def border_rgb(self) -> str:
        try:
            styles = [s for s in self.styles if isinstance(s, Style)]
            c = cast(int, cast(PolyStyle, styles[0].line_style).color)
            r = c & 0xFF
            g = (c & 0xFF00) >> 8
            b = (c & 0xFF0000) >> 16
            return f"{r:02x}{g:02x}{b:02x}"
        except Exception:
            pass
        return "000000"

    @border_rgb.setter
    def border_rgb(self, val: str) -> None:
        try:
            c = int(val, 16)
            new_c = ((c & 0xFF0000) >> 16) + (c & 0xFF00) + ((c & 0xFF) << 16)
            styles = [s for s in self.styles if isinstance(s, Style)]
            for s in styles:
                cast(PolyStyle, s.line_style).color = (
                    cast(int, cast(PolyStyle, s.line_style).color) & 0xFF000000
                ) + new_c
        except Exception:
            pass

    @property
    def border_alpha(self) -> int:
        try:
            styles = [s for s in self.styles if isinstance(s, Style)]
            return (
                cast(int, cast(PolyStyle, styles[0].line_style).color) & 0xFF000000
            ) >> 24
        except Exception:
            return 0

    @border_alpha.setter
    def border_alpha(self, val: int) -> None:
        try:
            a = int(val)
            a = 0 if val < 0 else 255 if val > 255 else val
            styles = [s for s in self.styles if isinstance(s, Style)]
            for s in styles:
                cast(PolyStyle, s.line_style).color = (
                    cast(int, cast(PolyStyle, s.line_style).color) & 0xFFFFFF
                ) + ((a & 0xFF) << 24)
        except Exception:
            pass
