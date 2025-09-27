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

"""SoundCue module."""

from typing import Any

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import _FieldDef
from pyLiveKML.objects.TourPrimitive import TourPrimitive


class SoundCue(TourPrimitive):
    """A KML `<gx:SoundCue>` tag constructor.

    Notes
    -----
    There is no play duration. The sound file plays in parallel to the rest of the tour,
    meaning that the next tour primitive takes place immediately after the `SoundCue`
    tour primitive is reached. If another sound file is cued before the first has
    finished playing, the files are mixed.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#extended-by_8

    Parameters
    ----------
    href: str
        Specifies a sound file to play, in MP3, M4A, or AAC format.
    delayed_start: float, default = 0
        Specifies to delay the start of the sound for a given number of seconds before
        playing the file.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "gx:SoundCue"
    _kml_fields = TourPrimitive._kml_fields + (
        _FieldDef("href"),
        _FieldDef("delayed_start", "gx:delayedStart"),
    )

    def __init__(
        self,
        href: str,
        delayed_start: float = 0,
        **kwargs: Any,
    ) -> None:
        """SoundCue instance constructor."""
        TourPrimitive.__init__(self, **kwargs)
        self.href = href
        self.delayed_start = delayed_start
