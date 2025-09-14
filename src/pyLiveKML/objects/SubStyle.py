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

"""SubStyle module."""

from abc import ABC

from pyLiveKML.objects.Object import _FieldDef, Object


class SubStyle(Object, ABC):
    """A KML `<SubStyle>` tag constructor.

    This is an abstract element and cannot be used directly in a KML file.

    Notes
    -----
    There is no description of the `SubStyle` class in the Google KML documentation,
    although it is include in the inheritance tree at the top of the page.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference.

    Parameters
    ----------
    Nil

    Attributes
    ----------
    Nil

    """

    _kml_fields: tuple[_FieldDef, ...] = tuple()

    def __init__(self) -> None:
        """SubStyle instance constructor."""
        Object.__init__(self)
        ABC.__init__(self)
