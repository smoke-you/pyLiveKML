"""ViewerOption module."""

from lxml import etree  # type: ignore

from pyLiveKML.types.types import ViewerOptionEnum
from pyLiveKML.utils import with_ns
from pyLiveKML.objects.Object import _BaseObject


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
