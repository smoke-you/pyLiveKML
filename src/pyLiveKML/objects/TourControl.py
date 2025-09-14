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

"""TourControl module."""

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import _FieldDef
from pyLiveKML.objects.TourPrimitive import TourPrimitive
from pyLiveKML.types import PlayModeEnum


class TourControl(TourPrimitive):
    """A KML `<gx:TourControl>` tag constructor.

    Allows a `Tour` to be paused, until the user takes action to continue the `Tour`.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#extended-by_8

    Parameters
    ----------
    play_mode : PlayModeEnum, default = PlayModeEnum.PAUSE

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "gx:TourControl"
    _kml_fields = TourPrimitive._kml_fields + (_FieldDef("play_mode", "gx:playMode"),)

    def __init__(
        self,
        play_mode: PlayModeEnum = PlayModeEnum.PAUSE,
    ) -> None:
        """GxTourControl instance constructor."""
        TourPrimitive.__init__(self)
        self.play_mode = play_mode
