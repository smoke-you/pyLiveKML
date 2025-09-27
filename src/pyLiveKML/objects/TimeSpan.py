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

"""TimeSpan module."""

from datetime import datetime
from typing import Any

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import _DateTimeParse, _FieldDef
from pyLiveKML.objects.TimePrimitive import TimePrimitive


class TimeSpan(TimePrimitive):
    """A KML `<TimeSpan>` tag constructor.

    Represents an extent in time bounded by begin and end `datetime`s.

    Notes
    -----
    If `begin` or `end` is `None`, then that end of the period is unbounded.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#style

    Parameters
    ----------
    begin: datetime | str | None, default = None
    end: datetime | str | None, default = None

    Attributes
    ----------
    begin: datetime | None
    end: datetime | None

    """

    _kml_tag = "TimeSpan"
    _kml_fields = TimePrimitive._kml_fields + (
        _FieldDef("begin", parser=_DateTimeParse),
        _FieldDef("end", parser=_DateTimeParse),
    )

    def __init__(
        self,
        begin: datetime | str | None = None,
        end: datetime | str | None = None,
        **kwargs: Any,
    ):
        """TimeSpan instance constructor."""
        TimePrimitive.__init__(self, **kwargs)
        self.begin = begin
        self.end = end
