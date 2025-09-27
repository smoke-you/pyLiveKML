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

"""TimePrimitive module."""

from abc import ABC
from typing import Any

from pyLiveKML.objects.Object import Object


class TimePrimitive(Object, ABC):
    """A KML `<TimePrimitive>` tag constructor.

    This is an abstract class and cannot be used directly in a KML file. Extended by the
    `TimeSpan` and `TimeStamp` (and `GxTimeSpan` and `GxTimeStamp`) classes.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference

    Parameters
    ----------
    Nil

    Attributes
    ----------
    Nil

    """

    def __init__(self, **kwargs: Any) -> None:
        """TimePrimitive instance constructor."""
        Object.__init__(self, **kwargs)
        ABC.__init__(self)
