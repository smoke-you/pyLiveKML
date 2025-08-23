"""GeoEllipse module."""

import math
from typing import Optional, Iterator

from numpy import ndarray, array
from scipy.spatial.transform import Rotation
from pyLiveKML import GeoCoordinates, AltitudeMode

from .GeoShape import GeoShape


def ellipse_gen(
    x_rad: float,
    y_rad: float,
    rotation: Optional[Rotation] = None,
    num_vertices: int = 32,
) -> Iterator[ndarray]:
    """Construct an ellipse as a set of points."""
    step = 2 * math.pi / num_vertices
    angle = -step
    for i in range(0, num_vertices):
        angle += step
        point = array([x_rad * math.cos(angle), y_rad * math.sin(angle), 0])
        if rotation is not None:
            point = rotation.apply(point)
        yield point


class GeoEllipse(GeoShape):
    """The GeoEllipse class represents a simple ellipse."""

    def __init__(
        self,
        origin: GeoCoordinates,
        x_radius: float,
        y_radius: float,
        rotation: Optional[Rotation] = None,
        num_vertices: int = 32,
        border_width: float = 1.0,
        border_color: int = 0xFFFFFFFF,
        fill_color: int = 0xFFFFFFFF,
        name: Optional[str] = None,
        selected: bool = False,
        altitude_mode: AltitudeMode = AltitudeMode.CLAMP_TO_GROUND,
    ):
        """GeoEllipse instance constructor."""
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
