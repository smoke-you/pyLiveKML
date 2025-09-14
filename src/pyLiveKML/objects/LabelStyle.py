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

from lxml import etree  # type: ignore

from pyLiveKML.objects.ColorStyle import ColorStyle
from pyLiveKML.objects.Object import _FieldDef
from pyLiveKML.types import ColorModeEnum, GeoColor


class LabelStyle(ColorStyle):
    """A KML `<LabelStyle>` tag constructor.

    Specifies how the `name` of a `Feature` is drawn in the 3D viewer.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#labelstyle

    Parameters
    ----------
    scale: float, default = 1.0
        Resizes the label.
    color: GeoColor | int | None, default = None
    color_mode: ColorModeEnum | None, default = None

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "LabelStyle"
    _kml_fields = ColorStyle._kml_fields + (_FieldDef("scale"),)

    def __init__(
        self,
        scale: float | None = None,
        color: GeoColor | int | None = None,
        color_mode: ColorModeEnum | None = None,
    ):
        """ColorStyle instance constructor."""
        super().__init__(color=color, color_mode=color_mode)
        self.scale = scale
