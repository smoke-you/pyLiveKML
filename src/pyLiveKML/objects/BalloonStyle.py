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

"""BalloonStyle module."""

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import _FieldDef, _ColorParse
from pyLiveKML.objects.SubStyle import SubStyle
from pyLiveKML.types import DisplayModeEnum, GeoColor


class BalloonStyle(SubStyle):
    """A KML `<BalloonStyle>` tag constructor.

    Specifies how the description balloon for placemarks is drawn. The `bgColor`, if
    specified, is used as the background color of the balloon.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#balloonstyle

    Parameters
    ----------
    bg_color : GeoColor | int | None, default = None
        Background color of the balloon.
    text_color : GeoColor | int | None, default = None
    text : str | None, default = None
        Text displayed in the balloon. If no text is specified, Google Earth draws the
        default balloon (with the `Feature` `<name>` in boldface, the `Feature`
        `<description>`, links for driving directions, a white background, and a tail
        that is attached to the point coordinates of the `Feature`, if specified).
    display_mode : DisplayModeEnum | None, default = None
        If `<displayMode>` is "default", Google Earth uses the information supplied in
        `<text>` to create a balloon. If `<displayMode>` is "hide", Google Earth does not
        display the balloon. In Google Earth, clicking the List View icon for a
        `Placemark` whose balloon's `<displayMode>` is "hide" causes Google Earth to fly
        to the `Placemark`.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "BalloonStyle"
    _kml_fields = SubStyle._kml_fields + (
        _FieldDef("bg_color", "bgColor", _ColorParse),
        _FieldDef("text_color", "textColor", _ColorParse),
        _FieldDef("text"),
        _FieldDef("display_mode", "displayMode"),
    )

    def __init__(
        self,
        bg_color: GeoColor | int | None = None,
        text_color: GeoColor | int | None = None,
        text: str | None = None,
        display_mode: DisplayModeEnum | None = None,
    ):
        """BalloonStyle instance constructor."""
        SubStyle.__init__(self)
        self.bg_color = bg_color
        self.text_color = text_color
        self.text = text
        self.display_mode = display_mode
