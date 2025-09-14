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

"""TimeStamp module."""

from datetime import datetime

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import _FieldDef, _DateTimeParse
from pyLiveKML.objects.TimePrimitive import TimePrimitive


class TimeStamp(TimePrimitive):
    """A KML `<TimeStamp>` tag constructor.

    Represents a single moment in time. This is a simple element and contains no
    children. Its value is a `datetime`, specified in XML time. The precision of the
    `TimeStamp` is dictated by the value of `when`.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#style
    * http://www.w3.org/TR/xmlschema-2/#isoformats

    Parameters
    ----------
    when : datetime | str

    Attributes
    ----------
    when : datetime

    """

    _kml_tag = "TimeStamp"
    _kml_fields = TimePrimitive._kml_fields + (
        _FieldDef("when", parser=_DateTimeParse),
    )

    def __init__(
        self,
        when: datetime | str,
    ):
        """TimeStamp instance constructor."""
        TimePrimitive.__init__(self)
        self.when = when
