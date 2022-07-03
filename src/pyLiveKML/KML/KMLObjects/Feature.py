from abc import ABC
from typing import Optional, Iterable, Iterator

from pyLiveKML.KML.KML import State
from pyLiveKML.KML.KMLObjects.Object import Object
from pyLiveKML.KML.KMLObjects.StyleSelector import StyleSelector


class Feature(Object, ABC):
    """A KML 'Feature', per https://developers.google.com/kml/documentation/kmlreference#feature. Note that while
    Features are explicitly abstract in the KML specification, :class:`~pyLiveKML.KML.KMLObjects.Feature` is the base
    class for KML :class:`~pyLiveKML.KML.KMLObjects.Object` instances that have an "existence" in GEP, i.e. that are
    (potentially) user-editable because they appear in the GEP user List View.

    :param Optional[str] name: The (optional) name for this :class:`~pyLiveKML.KML.KMLObjects.Feature` that will be
        displayed in GEP.
    :param Optional[str] description: The (optional) description for this :class:`~pyLiveKML.KML.KMLObjects.Feature`
        that will be displayed in GEP as a text balloon if the :class:`~pyLiveKML.KML.KMLObjects.Feature` is clicked.
    :param Optional[bool] visibility: The (optional) initial visibility for this
        :class:`~pyLiveKML.KML.KMLObjects.Feature` in GEP.
    :param Optional[Feature] container: The (optional) :class:`~pyLiveKML.KML.KMLObjects.Feature` (generally, a
        :class:`~pyLiveKML.KML.KMLObjects.Container`) that encloses this
        :class:`~pyLiveKML.KML.KMLObjects.Feature`.
    :param Optional[str] style_url: An (optional) style URL, typically a reference to a global
        :class:`~pyLiveKML.KML.KMLObjects.StyleSelector` in a :class:`~pyLiveKML.KML.KMLObjects.Container` that
        encloses this :class:`~pyLiveKML.KML.KMLObjects.Feature`.
    :param Optional[Iterable[StyleSelector]] styles: An iterable of :class:`~pyLiveKML.KML.KMLObjects.StyleSelector`
        objects that are local to this :class:`~pyLiveKML.KML.KMLObjects.Feature`.
    """

    @property
    def container(self) -> Optional['Container']:
        """The :class:`~pyLiveKML.KML.KMLObjects.Container` that immediately encloses this
        :class:`~pyLiveKML.KML.KMLObjects.Feature` in an ownership tree.

        :warning: The :attr:`container` property cannot be altered if the :class:`~pyLiveKML.KML.KMLObjects.Feature` is
            visible in GEP. Doing so would break GEP synchronization. Failure to observe this constraint will cause a
            :class:`ValueError` to be raised.
        """
        return self._container

    @container.setter
    def container(self, value: 'Container'):
        if self._state == State.IDLE or self._state == State.CREATING:
            self._container = value
        else:
            raise ValueError('If a Feature is visible in GEP, you cannot change its\' \'container\' property.')

    @property
    def name(self) -> Optional[str]:
        """The text that will be displayed as the name of the :class:`~pyLiveKML.KML.KMLObjects.Feature` in GEP.
        """
        return self._name

    @name.setter
    def name(self, value: Optional[str]):
        if self._name != value:
            self._name = value
            self.field_changed()

    @property
    def visibility(self) -> Optional[bool]:
        """True if the :class:`~pyLiveKML.KML.KMLObjects.Feature` will (initially) be checked (visible) in GEP, False
        otherwise.
        """
        return self._visibility

    @visibility.setter
    def visibility(self, value: Optional[bool]):
        if self._visibility != value:
            self._visibility = value
            self.field_changed()

    @property
    def description(self) -> Optional[str]:
        """The text description for this :class:`~pyLiveKML.KML.KMLObjects.Feature`, that will be displayed in a
        balloon in GEP if the :class:`~pyLiveKML.KML.KMLObjects.Feature` is clicked.

        :note: HTML and (some) JavaScript are permissible (in GEP > 5.0) for the :attr:`description` property. Refer to
            the KML specification at https://developers.google.com/kml/documentation/kmlreference for details.
        """
        return self._description

    @description.setter
    def description(self, value: Optional[str]):
        if self._description != value:
            self._description = value
            self.field_changed()

    @property
    def styles(self) -> Iterator[StyleSelector]:
        """A generator to retrieve references to any :class:`~pyLiveKML.KML.KMLObjects.Style` or
        :class:`~pyLiveKML.KML.KMLObjects.StyleMap` objects that are children of this
        :class:`~pyLiveKML.KML.KMLObjects.Feature`.

        :returns: A generator of :class:`~pyLiveKML.KML.KMLObjects.StyleSelector` objects.
        """
        for s in self._styles:
            yield s

    # override Object.select() to enable upwards cascade, i.e. if a Feature contained in an unselected parent Feature
    # is selected, the parent Feature must also be selected in order for GEP synchronization to work correctly.
    def select(self, value: bool, cascade: bool = False):
        """Overrides :func:`~pyLiveKML.KML.KMLObjects.Object.Object.select` to implement upwards cascade of selection.
        That is, if a :class:`~pyLiveKML.KML.KMLObjects.Feature` enclosed in the object tree depending from an
        unselected  parent :class:`~pyLiveKML.KML.KMLObjects.Feature` is selected, the reverse tree's parents must also
        be selected in order for GEP synchronization to work correctly.
        """
        Object.select(self, value, cascade)
        # Cascade Select *upwards* for Features, but *do not* cascade Deselect upwards
        if value and self._container:
            self._container.select(True, False)

    def __init__(
            self,
            name: Optional[str] = None,
            description: Optional[str] = None,
            visibility: Optional[bool] = None,
            container: Optional['Feature'] = None,
            style_url: Optional[str] = None,
            styles: Optional[Iterable[StyleSelector]] = None,
    ):
        Object.__init__(self)
        ABC.__init__(self)
        self._container = container
        self._name = name
        self._visibility = visibility
        self._description = description
        self._style_url = style_url
        self._styles = list[StyleSelector]()
        if styles:
            self._styles.extend(styles)

    def __str__(self):
        return f'{self.kml_type}:{self.name}'

    def __repr__(self):
        return self.__str__()
