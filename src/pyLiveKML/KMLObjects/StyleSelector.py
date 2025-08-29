"""StyleSelector module."""

from abc import ABC

from pyLiveKML.KMLObjects.Object import Object


class StyleSelector(Object, ABC):
    """A KML 'StyleSelector', per https://developers.google.com/kml/documentation/kmlreference#styleselector.

    The :class:`~pyLiveKML.KMLObjects.StyleSelector` class is the abstract base class
    for KML :class:`~pyLiveKML.KMLObjects.Object` instances that represent display
    styles for :class:`~pyLiveKML.KMLObjects.Feature` instances.
    """

    def __init__(self) -> None:
        """StyleSelector instance constructor."""
        Object.__init__(self)
        ABC.__init__(self)
