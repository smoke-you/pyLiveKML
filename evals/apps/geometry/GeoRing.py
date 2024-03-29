from numpy import ndarray, array
from scipy.spatial.transform import Rotation

from .GeoShape import GeoShape
from src.pyLiveKML.KML.GeoCoordinates import GeoCoordinates
from src.pyLiveKML.KML.KML import AltitudeMode


def circle_gen(radius: float, rotation: Rotation = None, num_v: int = 32) -> ndarray:
    point = array([radius, 0, 0])
    r = Rotation.from_euler('z', 360.0 / num_v, degrees=True)
    for i in range(0, num_v):
        yield rotation.apply(point) if rotation is not None else point
        point = r.apply(point)


class GeoRing(GeoShape):
    def __init__(
        self,
        origin: GeoCoordinates,
        outer_radius: float,
        inner_radius: float,
        num_vertices: int = 32,
        border_width: float = 1.0,
        border_color: int = 0xFFFFFFFF,
        fill_color: int = 0xFFFFFFFF,
        name: str = None,
        selected: bool = False,
        altitude_mode: AltitudeMode = AltitudeMode.CLAMP_TO_GROUND,
    ):
        GeoShape.__init__(
            self,
            origin=origin,
            outer_bound=list(circle_gen(outer_radius, None, num_vertices)),
            inner_bounds=[
                list(circle_gen(inner_radius, None, num_vertices)),
            ],
            border_width=border_width,
            border_color=border_color,
            fill_color=fill_color,
            name=name,
            selected=selected,
            altitude_mode=altitude_mode,
        )
