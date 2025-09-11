"""GeoShape module."""

from abc import ABC
from typing import Optional, cast

import numpy
from pyproj import Geod
from pyLiveKML import (
    GeoColor,
    GeoCoordinates,
    AltitudeModeEnum,
    LineStyle,
    LinearRing,
    PolyStyle,
    Polygon,
    Style,
    StyleMap,
)
from pyLiveKML.objects.Placemark import Placemark
from scipy.spatial.transform import Rotation

from .geography import project_shape


class GeoShape(Placemark, ABC):
    """Abstract class from which more specific geographical shapes may inherit."""

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
        altitude_mode: AltitudeModeEnum = AltitudeModeEnum.CLAMP_TO_GROUND,
    ) -> None:
        """GeoShape instance constructor."""
        self._origin = origin
        self._outer_bound_3d = outer_bound
        self._inner_bounds_3d = inner_bounds
        g_outer, g_inner = self.build()
        Placemark.__init__(
            self,
            name=name,
            inline_style=StyleMap(
                Style(
                    LineStyle(width=border_width, color=border_color),
                    PolyStyle(color=fill_color),
                ),
                Style(
                    LineStyle(width=border_width * 3, color=border_color),
                    PolyStyle(color=fill_color),
                ),
            ),
            geometry=Polygon(
                outer_boundary=LinearRing(coordinates=g_outer),
                inner_boundaries=[LinearRing(coordinates=g) for g in g_inner],
                altitude_mode=altitude_mode,
            ),
        )
        ABC.__init__(self)
        self.activate(selected)

    @property
    def normal_style(self) -> Style:
        """Retrieve the normal style of the `GeoShape`."""
        return cast(Style, cast(StyleMap, self._styles[0]).normal)

    @property
    def highlight_style(self) -> Style:
        """Retrieve the highlight style of the `GeoShape`."""
        return cast(Style, cast(StyleMap, self._styles[0]).highlight)

    @property
    def polygon(self) -> Polygon:
        """The polygon for the GeoShape instance."""
        return cast(Polygon, self.geometry)

    def rotate_shape(self, r: Rotation) -> None:
        """Roate the GeoShape instance about its origin on the surface of the geoid."""
        self._outer_bound_3d = r.apply(self._outer_bound_3d)
        if self._inner_bounds_3d:
            for b in self._inner_bounds_3d:
                b = r.apply(b)
        self._rebuild()

    def translate_on_surface(self, bearing: float, distance: float) -> None:
        """Translate the GeoShape instance across the surface of the geoid."""
        self._origin.lon, self._origin.lat, _ = Geod(ellps="WGS84").fwd(
            self._origin.lon, self._origin.lat, bearing, distance
        )
        self._rebuild()

    @property
    def origin(self) -> GeoCoordinates:
        """The origin of the GeoShape instance in the geoid."""
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
        for i, b in enumerate(self.polygon.inner_boundaries):
            b.coordinates = bi[i]

    def build(self) -> tuple[list[GeoCoordinates], list[list[GeoCoordinates]]]:
        """Construct the GeoShape instance."""
        g_outer = list(project_shape(self._outer_bound_3d, self._origin))
        g_inner = list[list[GeoCoordinates]]()
        if self._inner_bounds_3d:
            for b in self._inner_bounds_3d:
                g_inner.append(list(project_shape(b, self._origin)))
        return g_outer, g_inner

    @property
    def fill_rgb(self) -> str:
        """RGB-value of the fill of a polygon."""
        psc = cast(GeoColor, cast(PolyStyle, self.normal_style.poly_style).color)
        return f"{psc.rgb:06x}"

    @fill_rgb.setter
    def fill_rgb(self, val: str) -> None:
        c = int(val, 16)
        sn = cast(PolyStyle, self.normal_style.poly_style)
        cast(GeoColor, sn.color).rgb = c
        sn.field_changed()
        sh = cast(PolyStyle, self.highlight_style.poly_style)
        cast(GeoColor, sh.color).rgb = c
        sh.field_changed()

    @property
    def fill_alpha(self) -> int:
        """A-value of the fill of a polygon."""
        return cast(GeoColor, cast(PolyStyle, self.normal_style.poly_style).color).a

    @fill_alpha.setter
    def fill_alpha(self, val: int) -> None:
        a = int(val)
        a = 0 if val < 0 else 255 if val > 255 else val
        sn = cast(PolyStyle, self.normal_style.poly_style)
        cast(GeoColor, sn.color).a = a
        sn.field_changed()
        sh = cast(PolyStyle, self.highlight_style.poly_style)
        cast(GeoColor, sh.color).a = a
        sh.field_changed()

    @property
    def border_rgb(self) -> str:
        """RGB-value of the border of a polygon."""
        psc = cast(GeoColor, cast(LineStyle, self.normal_style.line_style).color)
        return f"{psc.rgb:06x}"

    @border_rgb.setter
    def border_rgb(self, val: str) -> None:
        c = int(val, 16)
        sn = cast(LineStyle, self.normal_style.line_style)
        cast(GeoColor, sn.color).rgb = c
        sn.field_changed()
        sh = cast(LineStyle, self.highlight_style.line_style)
        cast(GeoColor, sh.color).rgb = c
        sh.field_changed()

    @property
    def border_alpha(self) -> int:
        """A-value of the border of a polygon."""
        return cast(GeoColor, cast(LineStyle, self.normal_style.line_style).color).a

    @border_alpha.setter
    def border_alpha(self, val: int) -> None:
        a = int(val)
        a = 0 if val < 0 else 255 if val > 255 else val
        sn = cast(LineStyle, self.normal_style.line_style)
        cast(GeoColor, sn.color).a = a
        sn.field_changed()
        sh = cast(LineStyle, self.highlight_style.line_style)
        cast(GeoColor, sh.color).a = a
        sh.field_changed()
