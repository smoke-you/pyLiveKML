from typing import Optional

from lxml import etree

from .ColorStyle import ColorStyle


class LineStyle(ColorStyle):
    """
    A KML 'LineStyle', per https://developers.google.com/kml/documentation/kmlreference#linestyle.  Specifies
    various properties of a :class:`~pyLiveKML.KML.KMLObjects.Geometry`, typically either a
    :class:`~pyLiveKML.KML.KMLObjects.LineString` or :class:`~pyLiveKML.KML.KMLObjects.LinearRing`, including
    the inner and outer boundaries of :class:`~pyLiveKML.KML.KMLObjects.Polygon` objects.

    :param Optional[float] width: The (optional) width of the line, in pixels.
    :param Optional[int] color: The (optional) color of the line, as a 32-bit ABGR value.
    """

    @property
    def kml_type(self) -> str:
        """Overridden from :attr:`~pyLiveKML.KML.KMLObjects.Object.Object.kml_type` to set the KML tag name to
        'LineStyle'"""
        return 'LineStyle'

    @property
    def width(self) -> Optional[float]:
        """The width of the line, in pixels.
        """
        return self._width

    @width.setter
    def width(self, value: Optional[float]):
        if self._width != value:
            self._width = value
            self.field_changed()

    @property
    def gx_outer_color(self) -> Optional[int]:
        """Color of the portion of the line defined by the :attr:`gx_outer_width` property. Note that both
        :attr:`gx_outer_color` and :attr:`gx_outer_width` apply only to :class:`~pyLiveKML.KML.KMLObjects.LineString`
        objects.
        """
        return self._gx_outer_color

    @gx_outer_color.setter
    def gx_outer_color(self, value: Optional[int]):
        val = 0 if value <= 0 else 0xffffffff if value >= 0xffffffff else value
        if self._gx_outer_color != val:
            self._gx_outer_color = val
            self.field_changed()

    @property
    def gx_outer_width(self) -> Optional[float]:
        """Width of an outer border around the line. Note that both :attr:`gx_outer_color` and :attr:`gx_outer_width`
        apply only to :class:`~pyLiveKML.KML.KMLObjects.LineString` objects.
        """
        return self._gx_outer_width

    @gx_outer_width.setter
    def gx_outer_width(self, value: Optional[float]):
        if self._gx_outer_width != value:
            self._gx_outer_width = value
            self.field_changed()

    @property
    def gx_physical_width(self) -> Optional[float]:
        """The physical width of the line, in metres.
        """
        return self._gx_physical_width

    @gx_physical_width.setter
    def gx_physical_width(self, value: Optional[float]):
        if self._gx_physical_width != value:
            self._gx_physical_width = value
            self.field_changed()

    @property
    def gx_label_visibility(self) -> Optional[bool]:
        """Selector to display a text label on a :class:`~pyLiveKML.KML.KMLObjects.LineString`. True if the label is to
        be displayed, False if it is not. None implies False.
        """
        return self._gx_label_visibility

    @gx_label_visibility.setter
    def gx_label_visibility(self, value: Optional[bool]):
        if self._gx_label_visibility != value:
            self._gx_label_visibility = value
            self.field_changed()

    def build_kml(self, root: etree.Element, with_children=True):
        if self._color is not None:
            etree.SubElement(root, 'color').text = f'{self._color:08x}'
        if self._color_mode is not None:
            etree.SubElement(root, 'colorMode').text = self._color_mode.value
        if self._width is not None:
            etree.SubElement(root, 'width').text = f'{self._width:0.1f}'
        if self._gx_outer_color is not None:
            etree.SubElement(root, 'gx:outerColor').text = f'{self._gx_outer_color:08x}'
        if self._gx_outer_width is not None:
            etree.SubElement(root, 'gx:outerWidth').text = f'{self._gx_outer_width:0.1f}'
        if self._gx_physical_width is not None:
            etree.SubElement(root, 'gx:physicalWidth').text = f'{self._gx_physical_width:0.1f}'
        if self._gx_label_visibility is not None:
            etree.SubElement(root, 'gx:labelVisibility').text = str(int(self._gx_label_visibility))

    def __init__(
            self,
            width: Optional[float] = None,
            color: Optional[int] = None,
    ):
        ColorStyle.__init__(self, color)
        self._width = width
        self._gx_outer_color: Optional[int] = None
        self._gx_outer_width: Optional[float] = None
        self._gx_physical_width: Optional[float] = None
        self._gx_label_visibility: Optional[bool] = None

    def __str__(self):
        return f'{self.kml_type}'

    def __repr__(self):
        return self.__str__()
