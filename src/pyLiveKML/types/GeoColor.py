"""GeoColor module."""


class GeoColor:
    """The GeoColor type describes an ABGR-format color, as used throughout GEP.

    Notes
    -----
    * The GeoColor type is *not* explicitly referenced by the KML specification; rather, it
    is a construct of convenience for the pyLiveKML package.
    * When constructing a GeoColor instance, either the value or _all_ of r, g, b, a
    _must_ be supplied or a `ValueError` will be raised.

    Parameters
    ----------
    value : int | None
        The integral (32-bit) numeric value of the color.
    r : int | None
        The integral (8-bit) numeric value of the red component of the color.
    g : int | None
        The integral (8-bit) numeric value of the green component of the color.
    b : int | None
        The integral (8-bit) numeric value of the blue component of the color.
    a : int | None
        The integral (8-bit) numeric value of the alpha component of the color.

    """

    def __init__(
        self,
        value: int | None = None,
        r: int | None = None,
        g: int | None = None,
        b: int | None = None,
        a: int | None = None,
    ):
        """GeoColor instance constructor."""
        self._r: int = 0
        self._g: int = 0
        self._b: int = 0
        self._a: int = 0
        if value is not None:
            self.value = value
        elif not all(map(lambda x: x is not None, (r, g, b, a))):
            raise ValueError("Either value, or all of (r,g,b,a), must be non-None.")
        else:
            self.r = r
            self.g = g
            self.b = b
            self.a = a

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
        return f"{self._a:02x}{self._b:02x}{self._g:02x}{self._r:02x}"

    def __eq__(self, other: object) -> bool:
        """Check equality."""
        return isinstance(other, GeoColor) and self.value == other.value
