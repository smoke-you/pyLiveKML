"""Model module."""

from typing import Iterator, Iterable

from lxml import etree  # type: ignore

from pyLiveKML.objects.Geometry import Geometry
from pyLiveKML.objects.Link import Link
from pyLiveKML.objects.Object import (
    _BaseObject,
    _ChildDef,
    _FieldDef,
    _ListObject,
    _Angle90,
    _Angle180,
    _AnglePos180,
    _Angle360,
    Object,
)
from pyLiveKML.types import AltitudeModeEnum


class Location(_BaseObject):
    """A KML `<Location>` tag constructor.

    Specific to :class:`pyLiveKML.objects.Model.Model`.

    Specifies the exact coordinates of the `Model`'s origin in latitude, longitude, and
    altitude. Latitude and longitude measurements are standard lat-lon projection with
    WGS84 datum. Altitude is distance above the earth's surface, in meters, and is
    interpreted according to the `Model`'s `altitude_mode`.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-model

    Parameters
    ----------
    longitude : float, default = 0
    latitude : float, default = 0
    altitude : float, default = 0

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "Location"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("longitude", parser=_Angle180),
        _FieldDef("latitude", parser=_Angle90),
        _FieldDef("altitude"),
    )

    def __init__(self, longitude: float = 0, latitude: float = 0, altitude: float = 0):
        """Location instance constructor."""
        super().__init__()
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = altitude


class Orientation(_BaseObject):
    """A KML `<Orientation>` tag constructor.

    Specific to :class:`pyLiveKML.objects.Model.Model`.

    Describes rotation of a 3D model's coordinate system to position the object in Google
    Earth.

    Rotations are applied to a Model in the following order:
    * roll
    * tilt
    * heading

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-model

    Parameters
    ----------
    heading : float, default = 0
    tilt : float, default = 0
    roll : float, default = 0

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "Orientation"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("heading", parser=_Angle360),
        _FieldDef("tilt", parser=_AnglePos180),
        _FieldDef("roll", parser=_Angle180),
    )

    def __init__(self, heading: float = 0, tilt: float = 0, roll: float = 0):
        """Location instance constructor."""
        super().__init__()
        self.heading = heading
        self.tilt = tilt
        self.roll = roll


class Scales(_BaseObject):
    """A KML `<Scale>` tag constructor.

    Specific to :class:`pyLiveKML.objects.Model.Model`.

    Scales a model along the x, y, and z axes in the model's coordinate space.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-model

    Parameters
    ----------
    x : float, default = 0
    y : float, default = 0
    z : float, default = 0

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "Scale"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("x"),
        _FieldDef("y"),
        _FieldDef("z"),
    )

    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        """Scale instance constructor."""
        super().__init__()
        self.x = x
        self.y = y
        self.z = z


class Alias(_BaseObject):
    """A KML `<Alias>` tag constructor.

    Specific to :class:`pyLiveKML.objects.Model.Model`.

    A mapping for the texture file paths from the original COLLADA file to the KML file
    that contains the owning `Model`. Allows texture files to be moved and/or renamed
    without having to update the original COLLADA file that references those textures.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-model

    Parameters
    ----------
    target_href : str
        Specifies the texture file to be fetched by Google Earth. This reference can be a
        relative reference to an image file within the .kmz archive, or it can be an
        absolute reference to the file (for example, a URL).
    source_href : str
        Is the path specified for the texture file in the Collada .dae file.

    Attributes
    ----------
    Same as parameters.

    """

    _kml_tag = "Alias"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("target_href", "targetHref"),
        _FieldDef("source_href", "sourceHref"),
    )

    def __init__(self, target_href: str, source_href: str):
        """Alias instance constructor."""
        super().__init__()
        self.target_href = target_href
        self.source_href = source_href


class ResourceMap(_ListObject[Alias], _BaseObject):
    """A KML `<ResourceMap>` tag constructor.

    Specific to :class:`pyLiveKML.objects.Model.Model`.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-model

    Parameters
    ----------
    resources : Alias | Sequence[Alias] | None, default = None
        The `Alias` objects to be contained in the `ResourceMap`

    Attributes
    ----------
    Nil

    """

    _kml_tag = "ResourceMap"
    _kml_children = _BaseObject._kml_children + (_ChildDef("resources"),)

    def __init__(self, resources: Alias | Iterable[Alias] | None = None) -> None:
        """ResourceMap instance constructor."""
        super().__init__()
        self.resources = resources

    @property
    def resources(self) -> Iterator[Alias]:
        """Retrieve a generator over the `Alias`es in this `ResourceMap`.

        If the property setter is called, replaces the current list of contained
        `Alias`es with those provided.

        Parameters
        ----------
        value : Alias | Iterable[Alias] | None
            The new `Alias` elements for the `ResourceMap`.

        :returns: A generator over the `Alias`es in the `ResourceMap`.
        :rtype: Iterator[Alias]

        """
        yield from self

    @resources.setter
    def resources(self, value: Alias | Iterable[Alias] | None) -> None:
        if value is not None:
            if isinstance(value, Alias):
                self.append(value)
            else:
                self.extend(value)


class Model(Geometry):
    """A KML `<Model>` tag constructor.

    A 3D object described in a COLLADA file (referenced in the `link` attribute). COLLADA
    files have a .dae file extension. Models are created in their own coordinate space
    and then located, positioned, and scaled in Google Earth. See the "Topics in KML" page
    on Models (link in References, below) for more detail.

    Google Earth supports the COLLADA common profile, with the following exceptions:
    * Google Earth supports only triangles and lines as primitive types. The maximum
    number of triangles allowed is 21845.
    * Google Earth does not support animation or skinning.
    * Google Earth does not support external geometry references.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#model
    * https://developers.google.com/kml/documentation/models

    Parameters
    ----------
    link : Link
        Specifies the file to load and optional refresh parameters.
    altitude_mode : AltitudeModeEnum | None, default = None
    location : tuple[float, float, float], default = (0, 0, 0)
        The location of the model, as a tuple of (longitude, latitude, altitude).
    orientation : tuple[float, float, float], default = (0, 0, 0)
        The orientation of the model, as a tuple of (heading, tilt, roll).
    scales : tuple[float, float, float], default = (0, 0, 0)
        The scaling of the model, as a tuple of (x, y, z).
    resources : Sequence[Alias] | Alias | None, default = None
        Mappings for the texture file paths from the original COLLADA file to the KML
        file that contains the `Model`.

    Attributes
    ----------
    link : Link
        Specifies the file to load and optional refresh parameters.
    altitude_mode : AltitudeModeEnum | None, default = None
    location : Location
        The location of the model.
    orientation : Orientation
        The orientation of the model.
    scales : Scales
        The scaling of the model.
    resources : ResourceMap
        Mappings for the texture file paths from the original COLLADA file to the KML
        file that contains the `Model`.

    """

    _kml_tag = "Model"
    _kml_fields = Object._kml_fields + (_FieldDef("altitude_mode", "gx:altitudeMode"),)
    _kml_children = Object._kml_children + (
        _ChildDef("link"),
        _ChildDef("location"),
        _ChildDef("orientation"),
        _ChildDef("scale"),
        _ChildDef("resources"),
    )

    def __init__(
        self,
        link: Link,
        altitude_mode: AltitudeModeEnum | None = None,
        location: tuple[float, float, float] = (0, 0, 0),
        orientation: tuple[float, float, float] = (0, 0, 0),
        scales: tuple[float, float, float] = (0, 0, 0),
        resources: Alias | Iterable[Alias] | None = None,
    ) -> None:
        """Model instance constructor."""
        Object.__init__(self)
        self.link = link
        altitude_mode = (
            AltitudeModeEnum.CLAMP_TO_GROUND if altitude_mode is None else altitude_mode
        )
        self.altitude_mode = altitude_mode
        self.location = Location(*location)
        self.orientation = Orientation(*orientation)
        self.scales = Scales(*scales)
        self.resources = ResourceMap(resources)
