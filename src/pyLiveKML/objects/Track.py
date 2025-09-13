"""Track module."""

from datetime import datetime
from typing import Any, Iterator, Iterable

from dateutil.parser import parse as dtparse
from lxml import etree  # type: ignore

from pyLiveKML.objects.Geometry import Geometry
from pyLiveKML.objects.Model import Model
from pyLiveKML.objects.Object import (
    _ChildDef,
    _FieldDef,
    _Angle180,
    _Angle360,
    _Angle90,
    _AnglePos180,
)
from pyLiveKML.types import AltitudeModeEnum
from pyLiveKML.utils import with_ns


class TrackCoord:
    """Track element coordinates class, specific to the `TrackElement` class.

    Used to collect the LLA (longitude/latitude/altitude) for a `TrackElement`.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-track

    Parameters
    ----------
    lon: float, default = 0
    lat: float, default = 0
    alt: float, default = 0

    Attributes
    ----------
    Same as parameters.

    """

    def __init__(
        self,
        lon: float = 0,
        lat: float = 0,
        alt: float = 0,
    ):
        """TrackCoord instance constructor."""
        super().__init__()
        self.lon = _Angle180.parse(lon)
        self.lat = _Angle90.parse(lat)
        self.alt = alt

    def __str__(self) -> str:
        """Return a string representation."""
        return f"{self.lon} {self.lat} {self.alt}"


class TrackAngles:
    """Track elements angles class, specific to the `TrackElement` class.

    Used to collect the rotation vector (heading/tilt/roll) for a `TrackElement`.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-track

    Parameters
    ----------
    heading: float, default = 0
    tilt: float, default = 0
    roll: float, default = 0

    Attributes
    ----------
    Same as parameters.

    """

    def __init__(
        self,
        heading: float = 0,
        tilt: float = 0,
        roll: float = 0,
    ) -> None:
        """TrackAngles instance constructor."""
        super().__init__()
        self.heading = _Angle360.parse(heading)
        self.tilt = _AnglePos180.parse(tilt)
        self.roll = _Angle180.parse(roll)

    def __str__(self) -> str:
        """Return a string representation."""
        return f"{self.heading} {self.tilt} {self.roll}"


class TrackElement:
    """Track element class, specific to the `Track` class.

    Used to collect the various components of each track point that are then distributed
    across the `<gx:Track>` tag when it is published.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-track

    Parameters
    ----------
    when : datetime | str | None, default = None
        The timestamp of the `TrackElement`. If a `str` is provided, it will be parsed
        with dateutils. Highly recommended to use an ISO format timestring.
    coords : TrackCoord | tuple[float, float, float] | tuple[float, float] | None, default = None
        The LLA coordinates of the track point, either a `TrackCoord` instance, or a
        tuple containing longitude, latitude and (optional) altitude, in that order.
    angles : TrackAngles | tuple[float, float, float] | tuple[float, float] | tuple[float] | float | None, default = None
        The rotational vector of the track point, either a `TrackAngles` instance, or a
        tuple containing heading, tilt and roll, in that order.
    extended_data: dict[str, dict[str, Any]] | None, default = None
        Extended data information. The key/s of the primary dict need to be # references
        for a `Schema` `id` in a `Document` hosting the `Track`. The sub-keys need to be
        fieldnames in their parent `Schema`. Technically, the

    Attributes
    ----------
    Same as parameters.

    """

    def __init__(
        self,
        when: datetime | str | None = None,
        coords: (
            TrackCoord | tuple[float, float, float] | tuple[float, float] | None
        ) = None,
        angles: (
            TrackAngles
            | tuple[float, float, float]
            | tuple[float, float]
            | tuple[float]
            | float
            | None
        ) = None,
        extended_data: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        """TrackElement instance constructor."""
        super().__init__()
        self.when: datetime | None
        if isinstance(when, str):
            self.when = dtparse(when)
        else:
            self.when = when
        self.coords: TrackCoord | None = None
        if coords is None or isinstance(coords, TrackCoord):
            self.coords = coords
        else:
            self.coords = TrackCoord(*coords)
        self.angles: TrackAngles | None = None
        if angles is None or isinstance(angles, TrackAngles):
            self.angles = angles
        elif isinstance(angles, tuple):
            self.angles = TrackAngles(*angles)
        else:
            self.angles = TrackAngles(angles)
        self.extended_data = extended_data


class Track(Geometry):
    """A KML `<gx:Track>` tag constructor.

    A `Track` describes how an object moves through the world over a given time period.
    This feature allows you to create one visible object in Google Earth (either a
    `Point` icon or a `Model`) that encodes multiple positions for the same object for
    multiple times. In Google Earth, the time slider allows the user to move the view
    through time, which animates the position of the object.

    A `MultiTrack` is used to collect multiple tracks into one conceptual unit with one
    associated icon (or `Model`) that moves along the track. This feature is useful if
    you have multiple tracks for the same real-world object. The `interpolate` attribute
    of a `MultiTrack` specifies whether to interpolate between the tracks in a
    `MultiTrack`. If this value is `False`, then the point or `Model` stops at the end of
    one track and jumps to the start of the next one. (For example, if you want a single
    `Placemark` to represent your travels on two days, and your GPS unit was turned off
    for four hours during this period, you would want to show a discontinuity between the
    points where the unit was turned off and then on again.) If the value for
    `interpolate` is `True`, the values between the end of the first track and the
    beginning of the next track are interpolated so that the track appears as one
    continuous path.

    Notes
    -----
    * Although Google's documentation states that "sparse" data, i.e. extended data with
    missing values, is handled smoothly, I have been unable to replicate this in
    practice. I have found that the data trace for any schema field with a "sparse"
    dataset does not appear in the elevation profile.
    * As far as I have been able to establish, extended data **must** be numeric (int or
    float), or it does not appear in the elevation profile.
    * As far as I have been able to establish, extended data does not appear **at all**
    in the elevation profile for `MultiTrack` instances.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#gxtrack

    Parameters
    ----------
    altitude_mode : AltitudeModeEnum | None, default = None
        Specifies how altitude components in the `coordinates` attribute of each element
        are interpreted.
    elements : TrackElement | Iterable[TrackElement] | None, default = None
        The elements (points) along the `Track`.
    model : Model | None, default = None
        If specified, the `Model` replaces the `Point` icon used to indicate the current
        position on the track. When a `Model` is specified within a `Track`, it's
        attributes behave as follows:
        * The `location` attribute is ignored.
        * The `altitude_mode` attribute is ignored.
        * The `orientation` attribute is combined with the orientation of the track as
        follows. First, the `orientation` rotation is applied, which brings the `Model`
        from its local (x, y, z) coordinate system to a right-side-up, north-facing
        orientation. Next, a rotation is applied that corresponds to the interpolation
        of the `angles` values that affect the heading, tilt, and roll of the model as
        it moves along the track. If no angles are specified, the heading and tilt are
        inferred from the movement of the model.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "gx:Track"
    _kml_fields = Geometry._kml_fields + (
        _FieldDef("altitude_mode", "gx:altitudeMode"),
    )
    _kml_children = Geometry._kml_children + (_ChildDef("model"),)

    def __init__(
        self,
        altitude_mode: AltitudeModeEnum | None = None,
        elements: TrackElement | Iterable[TrackElement] | None = None,
        model: Model | None = None,
    ) -> None:
        """Track instance constructor."""
        Geometry.__init__(self)
        self.altitude_mode = altitude_mode
        self.model = model
        self._schemas = dict[str, set[str]]()
        self._elements = list[TrackElement]()
        self.elements = elements

    @property
    def elements(self) -> Iterator[TrackElement]:
        """Retrieve a generator over the set of enclosed `TrackElements`."""
        yield from self._elements

    @elements.setter
    def elements(self, value: TrackElement | Iterable[TrackElement] | None) -> None:
        self._elements.clear()
        self._schemas.clear()
        if value is None:
            return
        if isinstance(value, TrackElement):
            self._elements.append(value)
        else:
            self._elements.extend(value)
            for xd in (
                e.extended_data for e in self._elements if e.extended_data is not None
            ):
                for schema, fields in xd.items():
                    if schema not in self._schemas:
                        self._schemas[schema] = set[str]()
                    self._schemas[schema].update(fields.keys())

    def build_kml(
        self,
        root: etree.Element,
        with_children: bool = True,
        with_dependents: bool = True,
    ) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children)
        value: str
        for e in self.elements:
            value = "" if e.when is None else e.when.isoformat()
            etree.SubElement(root, with_ns("when")).text = value
        for e in self.elements:
            value = "" if e.coords is None else str(e.coords)
            etree.SubElement(root, with_ns("gx:coord")).text = value
        for e in self.elements:
            value = "" if e.angles is None else str(e.angles)
            etree.SubElement(root, with_ns("gx:angles")).text = value
        if self._schemas:
            e_xd = etree.SubElement(root, "ExtendedData")
            for sch, fields in self._schemas.items():
                e_sch = etree.SubElement(e_xd, "SchemaData", attrib={"schemaUrl": sch})
                for f in sorted(fields):
                    e_field = etree.SubElement(
                        e_sch,
                        with_ns("gx:SimpleArrayData"),
                        attrib={with_ns("kml:name"): f},
                    )
                    for e in self.elements:
                        value = ""
                        if (
                            e.extended_data
                            and sch in e.extended_data
                            and f in e.extended_data[sch]
                            and e.extended_data[sch][f] is not None
                        ):
                            value = str(e.extended_data[sch][f])
                        etree.SubElement(e_field, with_ns("gx:value")).text = value
