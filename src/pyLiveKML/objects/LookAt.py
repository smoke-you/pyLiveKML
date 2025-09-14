# pyLiveKML: A python library that streams geospatial data using the KML protocol.
# Copyright (C) 2022 smoke-you

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""LookAt module."""

from typing import Any, Iterable, cast

from lxml import etree  # type: ignore

from pyLiveKML.objects.AbstractView import AbstractView, ViewerOption
from pyLiveKML.objects.Object import (
    _FieldDef,
    _Angle180,
    _Angle360,
    _Angle90,
    _AnglePos90,
    _NoParse,
)
from pyLiveKML.objects.TimePrimitive import TimePrimitive
from pyLiveKML.types import AltitudeModeEnum, GeoCoordinates, ViewerOptionEnum


class LookAt(AbstractView):
    """A KML `<LookAt>` tag constructor.

    Defines a virtual camera that is associated with any element derived from `Feature`.
    The `LookAt` element positions the "camera" in relation to the object that is being
    viewed. In Google Earth, the view "flies to" this `LookAt` viewpoint when the user
    double-clicks an item in the "Places" panel or double-clicks an icon in the 3D
    viewer.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#lookat

    Parameters
    ----------
    lla : GeoCoordinates | tuple[float, float, float|None] | tuple[float, float] | None, default = None
        The longitude, latitude and altitude (in that order, in decimal degrees) of the
        `LookAt` target. If `None`, `lon` and `lat` must be supplied or an exception will
        be thrown.
    heading : float, default = 0
        The heading (in decimal degrees) of the `LookAt` facing.
    tilt : float, default = 0
        The tilt (in decimal degrees) of the `LookAt` facing.
    range : float, default = 0
        Distance in meters from the point specified by `longitude`, `latitude` and
        `altitude` to the `LookAt` position.
    altitude_mode : AltitudeModeEnum | None, default = None
    lon : float | None, default = None
        The longitude (in decimal degrees) of the the `LookAt` target. If `None`, `lla`
        must be supplied.
    lat : float | None, default = None
        The latitude (in decimal degrees) of the the `LookAt` target. If `None`, `lla`
        must be supplied.
    alt : float | None, default = None
        The altitude (in metres, with respect to `altitude_mode`) of the the `LookAt`
        target.
    viewer_options : ViewerOption | Iterable[ViewerOption] | None, default = None
        Enable or disable one or more Google Earth view modes.
    time_primitive : TimePrimitive | None, default = None
        `TimeStamp` or `TimeSpan` assigned to the object.

    Attributes
    ----------
    viewer_options : list[ViewerOption]
    time_primitive : TimePrimitive | None
    lla : tuple[float, float, float]
        The longitude, latitude (respectively, in decimal degrees) and altitude (in
        metres) of the `LookAt` target.
    lon : float
        The longitude of the `LookAt` target, in decimal degrees.
    lat : float
        The latitude of the `LookAt` target, in decimal degrees.
    alt : float
        The altitude of the `LookAt` target, in metres, with respect to `altitude_mode`.
    heading : float
        The heading of the `LookAt` facing, in decimal degrees.
    tilt : float
        The tilt of the `LookAt` facing, in decimal degrees.
    range : float
        Distance in meters from the `LookAt` position to the target point specified by
        `lla`.
    altitude_mode : AltitudeModeEnum | None

    Raises
    ------
    ValueError
        If `lla` is None, and either `lat` or `lon` is also `None`, a `ValueError` will
        be raised by the constructor.
    ViewerOptionInvalidError
        If the `GROUND_NAVIGATION` viewer option is assigned.

    """

    _kml_tag = "LookAt"
    _kml_fields = AbstractView._kml_fields + (
        _FieldDef("lon", "longitude", parser=_Angle180),
        _FieldDef("lat", "latitude", parser=_Angle90),
        _FieldDef("alt", "altitude"),
        _FieldDef("heading", parser=_Angle360),
        _FieldDef("tilt", parser=_AnglePos90),
        _FieldDef("range", parser=_NoParse),
        _FieldDef("altitude_mode", "gx:altitudeMode"),
    )
    _disallowed_view_options = AbstractView._disallowed_view_options + (
        ViewerOptionEnum.GROUND_NAVIGATION,
    )

    def __init__(
        self,
        lla: (
            GeoCoordinates
            | tuple[float, float, float | None]
            | tuple[float, float]
            | None
        ) = None,
        heading: float = 0,
        tilt: float = 0,
        range: float = 0,
        altitude_mode: AltitudeModeEnum | None = None,
        lon: float | None = None,
        lat: float | None = None,
        alt: float | None = None,
        viewer_options: ViewerOption | Iterable[ViewerOption] | None = None,
        time_primitive: TimePrimitive | None = None,
    ):
        """LookAt instance constructor."""
        AbstractView.__init__(self, viewer_options, time_primitive)
        self.lon: float
        self.lat: float
        self.alt: float
        if lla is None and (lon is None or lat is None):
            raise ValueError(
                "You must supply either `lla` or `lon` and `lat` (and optionally `alt`)."
            )
        if lla is None:
            self.lon = cast(float, lon)
            self.lat = cast(float, lat)
            self.alt = cast(float, alt)
        else:
            self.lla = lla
        self.heading = heading
        self.tilt = tilt
        self.range = range
        self.altitude_mode = altitude_mode

    @property
    def lla(self) -> tuple[float, float, float]:
        """Get or set the longitude, latitude and altitude as a tuple.

        Parameters
        ----------
        value : GeoCoordinates | tuple[float, float, float|None] | tuple[float, float])
            The longitude, latitude and altitude as a tuple with optional altitude, or as
            `GeoCoordinates`.

        Returns
        -------
        tuple[float, float, float]
            The longitude, latitude and altitude as a tuple of floats.

        """
        return (self.lon, self.lat, self.alt)

    @lla.setter
    def lla(
        self,
        value: GeoCoordinates | tuple[float, float, float | None] | tuple[float, float],
    ) -> None:
        if isinstance(value, GeoCoordinates):
            v = value.values
            self.lon, self.lat = v[:2]
            self.alt = 0 if v[2] is None else v[2]
        elif len(value) >= 3:
            v = value[:3]
            self.lon, self.lat = v[:2]
            self.alt = 0 if v[2] is None else v[2]
        else:
            self.lon, self.lat = value
            self.alt = 0
