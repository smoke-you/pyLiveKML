import math
from typing import Optional, Iterator

from numpy import ndarray, array
from scipy.spatial.transform import Rotation

from .GeoShape import GeoShape
from src.pyLiveKML.KML.GeoCoordinates import GeoCoordinates
from src.pyLiveKML.KML.KML import AltitudeMode


def ellipse_gen(
    x_rad: float, y_rad: float, rotation: Rotation = None, num_v: int = 32
) -> Iterator[ndarray]:
    step = 2 * math.pi / num_v
    angle = -step
    for i in range(0, num_v):
        angle += step
        point = array([x_rad * math.cos(angle), y_rad * math.sin(angle), 0])
        if rotation is not None:
            point = rotation.apply(point)
        yield point


class GeoEllipse(GeoShape):
    def __init__(
        self,
        origin: GeoCoordinates,
        x_radius: float,
        y_radius: float,
        rotation: Rotation = None,
        num_vertices: int = 32,
        border_width: float = 1.0,
        border_color: int = 0xFFFFFFFF,
        fill_color: int = 0xFFFFFFFF,
        name: Optional[str] = None,
        selected: bool = False,
        altitude_mode: AltitudeMode = AltitudeMode.CLAMP_TO_GROUND,
    ):
        GeoShape.__init__(
            self,
            origin=origin,
            outer_bound=list(ellipse_gen(x_radius, y_radius, rotation, num_vertices)),
            inner_bounds=None,
            border_width=border_width,
            border_color=border_color,
            fill_color=fill_color,
            name=name,
            selected=selected,
            altitude_mode=altitude_mode,
        )
