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

"""PolyStyle module."""

from lxml import etree  # type: ignore

from pyLiveKML.objects.ColorStyle import ColorStyle
from pyLiveKML.objects.Object import _FieldDef
from pyLiveKML.types import ColorModeEnum, GeoColor


class PolyStyle(ColorStyle):
    """A KML `<PolyStyle>` tag constructor.

    Specifies the drawing style for all polygons, including polygon extrusions (which
    look like the walls of buildings) and line extrusions (which look like solid fences).

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#polystyle

    Parameters
    ----------
    color: GeoColor | int | None, default = None
    color_mode: ColorModeEnum | None, default = None
    fill: bool | None, default = None
        Specifies whether to fill the polygon.
    outline: bool | None, default = None
        Specifies whether to outline the polygon. `Polygon` outlines use the current
        `LineStyle`.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "PolyStyle"
    _kml_fields = ColorStyle._kml_fields + (
        _FieldDef("fill"),
        _FieldDef("outline"),
    )

    def __init__(
        self,
        color: GeoColor | int | None = None,
        color_mode: ColorModeEnum | None = None,
        fill: bool | None = None,
        outline: bool | None = None,
    ):
        """PolyStyle instance constructor."""
        ColorStyle.__init__(self, color, color_mode)
        self.fill = fill
        self.outline = outline
