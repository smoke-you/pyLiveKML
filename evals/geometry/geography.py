import numpy
from numpy import ndarray
from pyproj import Proj, Transformer
from scipy.spatial.transform import Rotation

from pyLiveKML.KML.GeoCoordinates import GeoCoordinates

ecef = Proj(proj='geocent', ellps='WGS84', datum='WGS84')
lla = Proj(proj='latlong', ellps='WGS84', datum='WGS84')
lla2ecef = Transformer.from_proj(lla, ecef)
ecef2lla = Transformer.from_proj(ecef, lla)


def project_shape(shape_3d: list[ndarray], origin: GeoCoordinates):
    p_org = lla2ecef.transform(origin.lon, origin.lat, origin.alt)
    r_geo = Rotation.from_euler('zyz', (90, 90 - origin.lat, origin.lon), degrees=True)
    for s in shape_3d:
        yield GeoCoordinates(*(ecef2lla.transform(*(numpy.add(r_geo.apply(s), p_org)))))
