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

"""ColorStyle module."""

from abc import ABC
from typing import Any

from pyLiveKML.objects.Object import _ColorParse, _FieldDef
from pyLiveKML.objects.SubStyle import SubStyle
from pyLiveKML.types import ColorModeEnum, GeoColor


class ColorStyle(SubStyle, ABC):
    """A KML `<ColorStyle>` tag constructor.

    This is an abstract element and cannot be used directly in a KML file. It provides
    elements for specifying the color and color mode of extended style types.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#colorstyle

    Parameters
    ----------
    color: GeoColor | int | None, default = None
    color_mode: ColorModeEnum | None, default = None

    Attributes
    ----------
    Same as parameters.

    """

    _kml_fields: tuple[_FieldDef, ...] = SubStyle._kml_fields + (
        _FieldDef("color", parser=_ColorParse),
        _FieldDef("color_mode", "colorMode"),
    )

    def __init__(
        self,
        color: GeoColor | int | None = None,
        color_mode: ColorModeEnum | None = None,
        **kwargs: Any,
    ):
        """ColorStyle instance constructor."""
        SubStyle.__init__(self, **kwargs)
        ABC.__init__(self)
        self.color_mode = color_mode
        self.color = GeoColor(color) if isinstance(color, int) else color
