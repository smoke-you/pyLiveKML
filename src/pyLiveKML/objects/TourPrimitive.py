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

"""TourPrimitive module."""

from abc import ABC
from typing import Any

from pyLiveKML.objects.Object import Object


class TourPrimitive(Object, ABC):
    """A KML `<TourPrimitive>` tag constructor.

    This is an abstract element and cannot be used directly in a KML file.

    Objects inheriting from `TourPrimitive` provide instructions to KML browsers during
    tours, including points to fly to and the duration of those flights, pauses, updates
    to KML features, and sound files to play.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#tourprimitive

    Parameters
    ----------
    Nil

    Attributes
    ----------
    Nil

    """

    def __init__(self, **kwargs: Any) -> None:
        """TourPrimitive instance constructor."""
        Object.__init__(self, **kwargs)
        ABC.__init__(self)
