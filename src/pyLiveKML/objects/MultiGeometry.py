"""MultiGeometry module."""

from typing import Iterable, Iterator

from lxml import etree  # type: ignore

from pyLiveKML.objects.Geometry import Geometry
from pyLiveKML.objects.Object import _ChildDef, _DeletableMixin, _ListObject


class MultiGeometry(_DeletableMixin, _ListObject[Geometry], Geometry):
    """A KML `<MultiGeometry>` tag constructor.

    A container for zero or more geometry primitives associated with the same feature.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#multigeometry

    Parameters
    ----------
    contents : Geometry | Iterable[Geometry] | None, default = None
        The `Geometry` instances to be hosted under this `MultiGeometry`.

    Attributes
    ----------
    Nil

    """

    _kml_tag = "MultiGeometry"
    _kml_children = Geometry._kml_children + (_ChildDef("contents"),)
    _yield_self = True

    def __init__(self, contents: Geometry | Iterable[Geometry] | None = None):
        """MultiGeometry instance constructor."""
        _DeletableMixin.__init__(self)
        _ListObject[Geometry].__init__(self)
        Geometry.__init__(self)
        self.contents = contents

    @property
    def contents(self) -> Iterator[Geometry]:
        """Retrieve a generator over the `Geometry`s in this `MultiGeometry`.

        If the property setter is called, replaces the current list of contained
        `Geometry`s with those provided.

        Parameters
        ----------
        value : Geometry | Iterable[Geometry] | None
            The new `Geometry` elements for the `MultiGeometry`.

        :returns: A generator over the `Geometry`s in the `MultiGeometry`.
        :rtype: Iterator[Geometry]

        """
        yield from self

    @contents.setter
    def contents(self, value: Geometry | Iterable[Geometry] | None) -> None:
        self.clear()
        if value is not None:
            if isinstance(value, Geometry):
                self.append(value)
            else:
                self.extend(value)
