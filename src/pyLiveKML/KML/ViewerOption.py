"""ViewerOption module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML import ViewerOptionEnum
from pyLiveKML.KML.utils import with_ns
from pyLiveKML.KML.Object import _BaseObject


class ViewerOption(_BaseObject):
    """Enables special viewing modes in Google Earth 6.0 and later.

    Refer https://developers.google.com/kml/documentation/kmlreference#elements-specific-to-abstractview.

    :param GxViewerOptionEnum option: The view option to be configured.
    :param bool enabled: Whether the view option is to be enabled.
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
