"""AbstractView module."""

from abc import ABC
from typing import Any, Iterable

from lxml import etree  # type: ignore

from pyLiveKML.objects.Object import _BaseObject, _ChildDef, Object
from pyLiveKML.objects.TimePrimitive import TimePrimitive
from pyLiveKML.types import ViewerOptionEnum
from pyLiveKML.utils import with_ns


class ViewerOption(_BaseObject):
    """Enables or disables special viewing modes.

    Used only in conjunction with subclasses of :class:`pyLiveKML.objects.AbstractView`.

    Notes
    -----
    * Applies only to Google Earth 6.0 and later.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-abstractview.

    Parameters
    ----------
    option : ViewerOptionEnum
        The view option to be configured.
    enabled : bool
        Whether the view option is to be enabled or disabled.

    """

    _kml_tag = "gx:option"

    def __init__(self, option: ViewerOptionEnum, enabled: bool):
        """GxViewerOption instance constructor."""
        super().__init__()
        self.option = option
        self.enabled = enabled

    def build_kml(
        self,
        root: etree.Element,
        with_children: bool = True,
        with_dependents: bool = True,
    ) -> None:
        """Construct the KML content and append it to the provided etree.Element."""
        super().build_kml(root, with_children, with_dependents)
        etree.SubElement(
            root,
            with_ns(self._kml_tag),
            attrib={"name": self.option.value, "enabled": str(int(self.enabled))},
        )


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

    _kml_children = Object._kml_children + (_ChildDef("time_primitive"),)

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

    def __setattr__(self, name: str, value: Any) -> None:
        """Manipulate attribute assignments.

        Ensures that if a time primitive is assigned to an `AbstractView`, it's
        `_kml_tag` is prefixed with the "gx:" namespace.
        """
        if name == "time_primitive" and isinstance(value, TimePrimitive):
            value._kml_tag = f"gx:{type(value)._kml_tag}"
        return super().__setattr__(name, value)
