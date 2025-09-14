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

"""GeoColor module."""


class GeoColor:
    """The GeoColor type describes an ABGR-format color, as used throughout GEP.

    Notes
    -----
    * The GeoColor type is *not* explicitly referenced by the KML specification; rather,
    it is a construct of convenience for the pyLiveKML package.
    * When constructing a GeoColor instance, at least *one* of the parameters must be
    supplied.
    * Parameter values less than the lower bound (0) of the target component (r, g, b, a)
    will be set to the lower bound. Any positive value will be bit-masked with 0xff to
    constrain it to an 8-bit range (0-255).

    Parameters
    ----------
    value : int | tuple[int, int, int, int] | None, default = None
        The integral (32-bit) numeric value of the color, or a 4-tuple of integers in
        ABGR order.
    rgba : tuple[int, int, int, int] | None, default = None
        The color as a 4-tuple of integers, in RGBA order, i.e. reversed from `value`.

    Raises
    ------
    ValueError
        If all of the parameters are `None`.

    """

    def __init__(
        self,
        value: int | tuple[int, int, int, int] | None = None,
        rgba: tuple[int, int, int, int] | None = None,
    ):
        """GeoColor instance constructor."""
        self._r: int = 0
        self._g: int = 0
        self._b: int = 0
        self._a: int = 0
        if value is not None:
            if isinstance(value, int):
                self.value = value
            else:
                self.a, self.b, self.g, self.r = value
        elif rgba is not None:
            self.r, self.g, self.b, self.a = rgba
        else:
            raise ValueError("At least one of the parameters must not be `None`")

    @property
    def value(self) -> int:
        """Combined ABGR components (32 bits, in that order, MSB to LSB)."""
        return self._r | (self._g << 8) | (self._b << 16) | (self._a << 24)

    @value.setter
    def value(self, value: int) -> None:
        value = 0 if value is None else value
        value = 0 if value < 0 else value
        value = 0xFFFFFFFF if value > 0xFFFFFFFF else value
        self._r = value & 0xFF
        self._g = (value >> 8) & 0xFF
        self._b = (value >> 16) & 0xFF
        self._a = (value >> 24) & 0xFF

    @property
    def bgr(self) -> int:
        """BGR portion (24 bits)."""
        return self._r + (self._g << 8) + (self._b << 16)

    @bgr.setter
    def bgr(self, value: int | None) -> None:
        value = 0 if value is None else value
        value = 0 if value < 0 else 0xFFFFFF if value > 0xFFFFFF else value
        self._r = value & 0xFF
        self._g = (value >> 8) & 0xFF
        self._b = (value >> 16) & 0xFF

    @property
    def rgb(self) -> int:
        """RGB (24 bits, reversed from GEP format!) portion."""
        return self._b + (self._g << 8) + (self._r << 16)

    @rgb.setter
    def rgb(self, value: int | None) -> None:
        value = 0 if value is None else value
        value = 0 if value < 0 else 0xFFFFFF if value > 0xFFFFFF else value
        self._b = value & 0xFF
        self._g = (value >> 8) & 0xFF
        self._r = (value >> 16) & 0xFF

    @property
    def r(self) -> int:
        """Red component (8 bits)."""
        return self._r

    @r.setter
    def r(self, value: int | None) -> None:
        value = 0 if value is None else value
        value = 0 if value < 0 else 0xFF if value > 0xFF else value
        self._r = value

    @property
    def g(self) -> int:
        """Green component (8 bits)."""
        return self._g

    @g.setter
    def g(self, value: int | None) -> None:
        value = 0 if value is None else value
        value = 0 if value < 0 else 0xFF if value > 0xFF else value
        self._g = value

    @property
    def b(self) -> int:
        """Blue component (8 bits)."""
        return self._b

    @b.setter
    def b(self, value: int | None) -> None:
        value = 0 if value is None else value
        value = 0 if value < 0 else 0xFF if value > 0xFF else value
        self._b = value

    @property
    def a(self) -> int:
        """Alpha component (8 bits)."""
        return self._a

    @a.setter
    def a(self, value: int | None) -> None:
        value = 0 if value is None else value
        value = 0 if value < 0 else 0xFF if value > 0xFF else value
        self._a = value

    def __str__(self) -> str:
        """Return a string representation."""
        return f"{self.value:08x}"

    def __eq__(self, other: object) -> bool:
        """Check equality."""
        return isinstance(other, GeoColor) and self.value == other.value
