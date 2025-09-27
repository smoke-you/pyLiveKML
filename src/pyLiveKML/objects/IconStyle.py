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

"""IconStyle module."""

from typing import Any

from lxml import etree  # type: ignore

from pyLiveKML.objects.ColorStyle import ColorStyle
from pyLiveKML.objects.Icon import Icon
from pyLiveKML.objects.Object import _ChildDef, _DependentDef, _FieldDef, _NoDump
from pyLiveKML.types import ColorModeEnum, GeoColor, HotSpot


class IconStyle(ColorStyle):
    """A KML `<IconStyle>` tag constructor.

    Specifies how icons for `Point` placemarks are drawn, both in the "Places" panel and
    in the 3D viewer of Google Earth. The `icon` attribute specifies the icon image. The
    `scale` attribute specifies the x, y scaling of the icon. The color specified in the
    `color` attribute of `IconStyle` is blended with the color of the `Icon`.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#iconstyle

    Parameters
    ----------
    icon: str | Icon | None, default = None
        An HTTP address, or a local file specification, or an `Icon`, used to load an
        icon for display.
    scale: float, default = 1.0
        Resizes the icon.
    heading: float | None, default = None
        Direction in decimal degrees. If not specified, defaults to 0. Values range from
        0 to 360 degrees.
    color: GeoColor | int | None, default = None
    color_mode: ColorModeEnum | None, default = None
    hot_spot: HotSpot | None, default = None
        Specifies the position within the icon that is "anchored" to the `Point` to which
        the style is applied.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "IconStyle"
    _kml_fields = ColorStyle._kml_fields + (
        _FieldDef("icon", dumper=_NoDump),
        _FieldDef("hot_spot", dumper=_NoDump),
        _FieldDef("scale"),
        _FieldDef("heading"),
    )
    _kml_dependents = ColorStyle._kml_dependents + (_DependentDef("hot_spot"),)
    _kml_children = ColorStyle._kml_children + (_ChildDef("icon"),)

    def __init__(
        self,
        icon: str | Icon | None = None,
        scale: float = 1.0,
        heading: float | None = None,
        color: GeoColor | int | None = None,
        color_mode: ColorModeEnum | None = None,
        hot_spot: HotSpot | None = None,
        **kwargs: Any,
    ):
        """IconStyle instance constructor."""
        ColorStyle.__init__(self, color=color, color_mode=color_mode, **kwargs)
        self.scale = scale
        self.heading = heading
        self.icon: Icon | None = Icon(href=icon) if isinstance(icon, str) else icon
        self.hot_spot = hot_spot
