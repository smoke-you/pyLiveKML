from abc import ABC

from .Object import Object


class StyleSelector(Object, ABC):
    """A KML 'StyleSelector', per https://developers.google.com/kml/documentation/kmlreference#styleselector. The
    :class:`~pyLiveKML.KML.KMLObjects.StyleSelector` class is the abstract base class for KML
    :class:`~pyLiveKML.KML.KMLObjects.Object` instances that represent display styles for
    :class:`~pyLiveKML.KML.KMLObjects.Feature` instances.
    """
    def __init__(self):
        Object.__init__(self)
        ABC.__init__(self)
