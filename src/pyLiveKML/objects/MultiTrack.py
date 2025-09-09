"""MultiTrack module."""

from typing import Iterator, Iterable

from lxml import etree  # type: ignore

from pyLiveKML.objects.Geometry import Geometry
from pyLiveKML.objects.Object import _ChildDef, _DeletableMixin, _FieldDef, _ListObject
from pyLiveKML.objects.Track import Track
from pyLiveKML.types.types import AltitudeModeEnum


# TODO: As with MultiGeometry, MultiTrack is in practice a Container, so it must be
# possible to add and delete its contents.


class MultiTrack(_DeletableMixin, _ListObject[Track], Geometry):
    """A KML `<MultiTrack>` tag constructor.

    A multi-track element is used to combine multiple track elements into a single
    conceptual unit. For example, suppose you collect GPS data for a day's bike ride that
    includes several rest stops and a stop for lunch. Because of the interruptions in
    time, one bike ride might appear as four different tracks when the times and
    positions are plotted. Grouping these `Track` elements into one `MultiTrack`
    container causes them to be displayed in Google Earth as sections of a single path.
    When the icon reaches the end of one segment, it moves to the beginning of the next
    segment. The `interpolate` attribute specifies whether to stop at the end of one
    track and jump immediately to the start of the next one, or to interpolate the
    missing values between the two tracks.

    Notes
    -----
    * As far as I have been able to establish, extended data does not appear **at all**
    in the elevation profile for `MultiTrack` instances.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#multitrack

    Parameters
    ----------
    tracks : Track | Iterable[Track] | None, default = None
        The `Track` instances to be hosted under this `MultiTrack`.

    Attributes
    ----------
    Nil

    """

    _kml_tag = "gx:MultiTrack"
    _kml_fields = Geometry._kml_fields + (
        _FieldDef("altitude_mode", "gx:altitudeMode"),
        _FieldDef("interpolate", "gx:interpolate"),
    )
    _kml_children = Geometry._kml_children + (_ChildDef("tracks"),)
    _yield_self = True

    def __init__(
        self,
        altitude_mode: AltitudeModeEnum | None = None,
        interpolate: bool = False,
        tracks: Track | Iterable[Track] | None = None,
    ) -> None:
        """MultiTrack instance constructor."""
        _DeletableMixin.__init__(self)
        _ListObject[Track].__init__(self)
        Geometry.__init__(self)
        self.altitude_mode = altitude_mode
        self.interpolate = interpolate
        self.tracks = tracks

    @property
    def tracks(self) -> Iterator[Track]:
        """The `Tracks` contained by this `MultiTrack` instance.

        Parameters
        ----------
        value : Track | Iterable[Track] | None

        :return: The `Tracks` contained by this `MultiTrack` instance.
        :rtype: Iterator[Track]

        """
        yield from self

    @tracks.setter
    def tracks(self, value: Track | Iterable[Track] | None) -> None:
        self.clear()
        if value is not None:
            if isinstance(value, Track):
                self.append(value)
            else:
                self.extend(value)
