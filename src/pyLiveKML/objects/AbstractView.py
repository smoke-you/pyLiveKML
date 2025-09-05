"""AbstractView module."""

from abc import ABC
from typing import Iterable

from lxml import etree  # type: ignore

from pyLiveKML.types import ViewerOption
from pyLiveKML.utils import with_ns
from pyLiveKML.objects.Object import Object, _DependentDef
from pyLiveKML.objects.TimePrimitive import TimePrimitive


class AbstractView(Object, ABC):
    """A KML `<AbstractView>` tag constructor.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#abstractview

    Parameters
    ----------
    viewer_options : ViewerOption | Iterable[ViewerOption] | None, default = None
        Enable or disable one or more Google Earth view modes.
    time_primitive : TimePrimitive | None, default = None
        Timestamp or timespan assigned to the object.

    Attributes
    ----------
    viewer_options : list[ViewerOption]
    time_primitive : TimePrimitive | None

    """

    _kml_dependents = Object._kml_dependents + (_DependentDef("time_primitive"),)

    def __init__(
        self,
        viewer_options: Iterable[ViewerOption] | ViewerOption | None = None,
        time_primitive: TimePrimitive | None = None,
    ) -> None:
        """AbstractView instance constructor."""
        Object.__init__(self)
        ABC.__init__(self)
        self._viewer_options = list[ViewerOption]()
        if viewer_options is not None:
            if isinstance(viewer_options, ViewerOption):
                self._viewer_options.append(viewer_options)
            else:
                self._viewer_options.extend(viewer_options)
        self.time_primitive = time_primitive

    def build_kml(
        self,
        root: etree.Element,
        with_children: bool = True,
        with_dependents: bool = True,
    ) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children, with_dependents)
        if self._viewer_options:
            opts = etree.SubElement(root, with_ns("gx:ViewerOptions"))
            for v in self._viewer_options:
                v.build_kml(opts)
