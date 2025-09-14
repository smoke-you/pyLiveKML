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

"""FlyTo module."""

from lxml import etree  # type: ignore

from pyLiveKML.objects.AbstractView import AbstractView
from pyLiveKML.objects.Object import _ChildDef, _FieldDef
from pyLiveKML.objects.TourPrimitive import TourPrimitive
from pyLiveKML.types import FlyToModeEnum


class FlyTo(TourPrimitive):
    """A KML `<gx:FlyTo>` tag constructor.

    Specifies a point in space to which the browser will fly during a tour. It must
    contain one `<AbstractView>`, and should contain `<gx:duration>` and `<gx:flyToMode>`
    elements.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#gxflyto.

    Parameters
    ----------
    duration : float
        The time (in seconds) it takes to fly to the defined point from the current point.
    fly_to_mode : FlyToModeEnum
        The method of flight to the defined point from the current point.
    abstract_view : AbstractView
        A concrete `AbstractView` subclass that describes the view while transitioning to
        the defined point from the current point.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "gx:FlyTo"
    _kml_fields = TourPrimitive._kml_fields + (
        _FieldDef("duration", "gx:duration"),
        _FieldDef("fly_to_mode", "gx:flyToMode"),
    )
    _kml_children = TourPrimitive._kml_children + (_ChildDef("abstract_view"),)

    def __init__(
        self,
        duration: float,
        fly_to_mode: FlyToModeEnum,
        abstract_view: AbstractView,
    ) -> None:
        """Track instance constructor."""
        TourPrimitive.__init__(self)
        self.duration = duration
        self.fly_to_mode = fly_to_mode
        self.abstract_view = abstract_view
