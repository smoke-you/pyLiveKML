"""AbstractView module."""

from abc import ABC
from typing import Any, Iterable, Iterator

from lxml import etree  # type: ignore

from pyLiveKML.errors import ViewerOptionInvalidError
from pyLiveKML.objects.Object import _BaseObject, _ChildDef, _DependentDef, Object
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
        root.attrib["name"] = self.option.value
        root.attrib["enabled"] = str(int(self.enabled))


class _ViewerOptions(_BaseObject):
    """A KML `<gx:ViewerOptions>` tag constructor.

    Private class to manage viewer options in `AbstractView` subclasses.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-abstractview

    Parameters
    ----------
    disallowed_view_options : tuple[ViewerOptionEnum, ...]
        The viewer options that are not permitted for the owning concrete subclass of
        `AbstractView`.
    items : Iterable[ViewerOption] | ViewerOption | None, default = None
        The viewer options that are to be configured.

    """

    _kml_tag = "gx:ViewerOptions"
    _kml_dependents = _BaseObject._kml_dependents + (_DependentDef("items"),)
    _yield_self = True

    def __init__(
        self,
        disallowed_view_options: tuple[ViewerOptionEnum, ...],
        items: Iterable[ViewerOption] | ViewerOption | None = None,
    ) -> None:
        """ViewerOptions instance constructor."""
        super().__init__()
        self.disallowed_view_options = disallowed_view_options
        self._items = list[ViewerOption]()
        self.items = items

    @property
    def items(self) -> Iterator[ViewerOption]:

        yield from self._items

    @items.setter
    def items(self, value: Iterable[ViewerOption] | ViewerOption | None) -> None:
        self._items.clear()
        if value is not None:
            if isinstance(value, ViewerOption):
                if value.option in self.disallowed_view_options:
                    raise ViewerOptionInvalidError(value.option.value)
                self._items.append(value)
            else:
                final = {v.option: v.enabled for v in value}
                errors = [
                    k.value for k in final.keys() if k in self.disallowed_view_options
                ]
                if errors:
                    raise ViewerOptionInvalidError(errors)
                self._items.extend(ViewerOption(k, v) for k, v in final.items())

    def build_kml(
        self,
        root: etree.Element,
        with_children: bool = True,
        with_dependents: bool = True,
    ) -> None:
        return super().build_kml(root, with_children, with_dependents)


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
        `TimeStamp` or `TimeSpan` assigned to the object.

    Attributes
    ----------
    viewer_options : list[ViewerOption]
    time_primitive : TimePrimitive | None

    Raises
    ------
    ViewerOptionInvalidError
        If one of the viewer options assigned is not permitted for the concrete subclass.

    """

    _kml_children = Object._kml_children + (_ChildDef("time_primitive"),)
    _kml_dependents = Object._kml_dependents + (_DependentDef("viewer_options"),)
    _disallowed_view_options: tuple[ViewerOptionEnum, ...] = tuple()

    def __init__(
        self,
        viewer_options: Iterable[ViewerOption] | ViewerOption | None = None,
        time_primitive: TimePrimitive | None = None,
    ) -> None:
        """AbstractView instance constructor."""
        Object.__init__(self)
        ABC.__init__(self)
        self.viewer_options = _ViewerOptions(
            self._disallowed_view_options, viewer_options
        )
        self.time_primitive = time_primitive

    def __setattr__(self, name: str, value: Any) -> None:
        """Manipulate attribute assignments.

        Ensures that if a time primitive is assigned to an `AbstractView`, it's
        `_kml_tag` is prefixed with the "gx:" namespace.
        """
        if name == "time_primitive" and isinstance(value, TimePrimitive):
            value._kml_tag = f"gx:{type(value)._kml_tag}"
        return super().__setattr__(name, value)
