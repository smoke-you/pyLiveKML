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

"""Wait module."""

from typing import Any

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import _FieldDef
from pyLiveKML.objects.TourPrimitive import TourPrimitive


class Wait(TourPrimitive):
    """A KML `<gx:Wait>` tag constructor.

    The camera remains still, at the last-defined `AbstractView`, for the number of
    seconds specified before playing the next `TourPrimitive`.

    Notes
    -----
    * A `Wait` does not pause the tour timeline - currently-playing sound files and
    animated updates will continue to play while the camera is waiting.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#gxwait

    Parameters
    ----------
    duration : float, default = 0
        The time in seconds to wait.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "gx:Wait"
    _kml_fields = TourPrimitive._kml_fields + (_FieldDef("duration", "gx:duration"),)

    def __init__(
        self,
        duration: float = 0,
        **kwargs: Any,
    ) -> None:
        """Wait instance constructor."""
        TourPrimitive.__init__(self, **kwargs)
        self.duration = duration
