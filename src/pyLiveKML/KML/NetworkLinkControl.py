"""NetworkLinkControl module."""

from lxml import etree  # type: ignore

from pyLiveKML.KML.KML import KML_UPDATE_CONTAINER_LIMIT_DEFAULT
from pyLiveKML.KML.KMLObjects.Feature import Container
from pyLiveKML.KML.KMLObjects.Folder import Folder


class NetworkLinkControl:
    """The NetworkLinkControl class synchronizes the internal state of a KML object tree rooted in its :attr:`container` attribute with GEP.

    :param str target_href: The URI of the KML document that will be synchronized by this
        :class:`~pyLiveKML.KML.NetworkLinkControl`. Note that the specified document *must* already have been created
        in GEP in order to be synchronized.
    :param Container|None container: The KML :class:`~pyLiveKML.KML.KMLObjects.Container` that will be the
        root of the tree of KML :class:`~pyLiveKML.KML.KMLObjects.Feature` instances managed and synchronized by this
        :class:`~pyLiveKML.KML.NetworkLinkControl`.  Note that if no :class:`~pyLiveKML.KML.KMLObjects.Container`, or
        None, is specified then a :class:`~pyLiveKML.KML.KMLObjects.Folder` instance named 'Root' will be instantiated
        for it.
    :param int update_limit: The (approximate) maximum number of Create, Change and/or Delete KML tags that will be
        generated as a result of any single synchronization update.
    :var Container container: The root of the tree of KML :class:`~pyLiveKML.KML.KMLObjects.Feature` instances that this
        :class:`~pyLiveKML.KML.NetworkLinkControl` synchronizes.
    :var str target_href: The URI of the KML document that will be synchronized by this
        :class:`~pyLiveKML.KML.NetworkLinkControl`.
    :var int update_limit: The (approximate) maximum number of KML objects that will be synchronized by any single
        synchronization update.
    """

    def __init__(
        self,
        target_href: str = "",
        container: Container | None = None,
        update_limit: int = KML_UPDATE_CONTAINER_LIMIT_DEFAULT,
    ):
        """NetworkLinkControl instance constructor."""
        # TODO: All of these should be included in the update_kml method, but they're not terribly important ATM.
        # self.min_refresh_period: float|None = None
        # self.max_session_length: float|None = None
        # self.cookie: str|None = None
        # self.message: str|None = None
        # self.link_name: str|None = None
        # self.link_description: str|None = None
        # self.link_snippet: str|None = None
        # self.expires: datetime|None = None
        self.target_href: str = target_href
        self.container: Container = (
            Folder("Root", is_open=True) if container is None else container
        )
        self.update_limit = update_limit

    def update_kml(self) -> etree.Element:
        """Generate a synchronization update by parsing the :attr:`container`.

        :return: The synchronization update.
        :rtype: etree.Element
        """
        root = etree.Element("NetworkLinkControl")
        update = etree.SubElement(root, "Update")
        etree.SubElement(update, "targetHref").text = self.target_href

        for f in self.container.containers:
            f.feature.update_kml(f.container, update)
            for c in f.feature.children:
                c.child.update_kml(c.parent, update)
            if isinstance(f.feature, Container):
                for d in f.feature.flush:
                    d.delete_kml(update)

        for f in self.container.features:
            if len(update) >= self.container.update_limit:
                break
            f.feature.update_kml(f.container, update)
            for c in f.feature.children:
                c.child.update_kml(c.parent, update)
        return root
