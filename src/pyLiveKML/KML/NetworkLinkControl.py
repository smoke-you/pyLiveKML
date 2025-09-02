"""NetworkLinkControl module."""

from datetime import datetime
from typing import cast, Iterable

from lxml import etree  # type: ignore

from pyLiveKML import KML_UPDATE_CONTAINER_LIMIT_DEFAULT
from pyLiveKML.KML.Object import _BaseObject, _FieldDef, ObjectState, _ChildDef, ObjectChild, _ListObject
from pyLiveKML.KML.Update import Update
from pyLiveKML.KMLObjects.AbstractView import AbstractView
from pyLiveKML.KMLObjects.Container import Container
from pyLiveKML.KMLObjects.Folder import Folder


class NetworkLinkControl(_BaseObject):
    """The NetworkLinkControl class synchronizes the internal state of a KML object tree rooted in its :attr:`container` attribute with GEP.

    :param str target_href: The URI of the KML document that will be synchronized by this
        :class:`~pyLiveKML.KML.NetworkLinkControl`. Note that the specified document *must* already have been created
        in GEP in order to be synchronized.
    :param Container|None container: The KML :class:`~pyLiveKML.KMLObjects.Container` that will be the
        root of the tree of KML :class:`~pyLiveKML.KMLObjects.Feature` instances managed and synchronized by this
        :class:`~pyLiveKML.KML.NetworkLinkControl`.  Note that if no :class:`~pyLiveKML.KMLObjects.Container`, or
        None, is specified then a :class:`~pyLiveKML.KMLObjects.Folder` instance named 'Root' will be instantiated
        for it.
    :param int update_limit: The (approximate) maximum number of Create, Change and/or Delete KML tags that will be
        generated as a result of any single synchronization update.
    :var Container container: The root of the tree of KML :class:`~pyLiveKML.KMLObjects.Feature` instances that this
        :class:`~pyLiveKML.KML.NetworkLinkControl` synchronizes.
    :var str target_href: The URI of the KML document that will be synchronized by this
        :class:`~pyLiveKML.KML.NetworkLinkControl`.
    :var int update_limit: The (approximate) maximum number of KML objects that will be synchronized by any single
        synchronization update.
    """

    _kml_tag = "NetworkLinkControl"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("min_refresh_period", "minRefreshPeriod"),
        _FieldDef("max_session_length", "maxSessionLength"),
        _FieldDef("cookie"),
        _FieldDef("message"),
        _FieldDef("link_name", "linkName"),
        _FieldDef("link_description", "linkDescription"),
        _FieldDef("link_snippet", "linkSnippet"),
        _FieldDef("link_expires", "linkExpires"),
    )
    _direct_children = _BaseObject._direct_children + (
        _ChildDef("update"),
    )

    def __init__(
        self,
        target_href: str = "",
        container: Container | None = None,
        update_limit: int = KML_UPDATE_CONTAINER_LIMIT_DEFAULT,
        min_refresh_period: float | None = None,
        max_session_length: float | None = None,
        cookie: str | None = None,
        message: str | None = None,
        link_name: str | None = None,
        link_description: str | None = None,
        link_snippet: str | None = None,
        link_expires: datetime | None = None,
        abstract_view: AbstractView | None = None,
    ):
        """NetworkLinkControl instance constructor."""
        self.target_href: str = target_href
        self.container: Container = (
            Folder("Root", is_open=True) if container is None else container
        )
        self.update_limit = update_limit
        self.min_refresh_period = min_refresh_period
        self.max_session_length = max_session_length
        self.cookie = cookie
        self.message = message
        self.link_name = link_name
        self.link_description = link_description
        self.link_snippet = link_snippet
        self.link_expires = link_expires
        self.abstract_view = abstract_view
        self.update = Update(target_href)


    def build_kml(self, root: etree.Element, with_children: bool = True) -> None:
        """Construct the KML content and append it to the provided etree.Element."""

        # The real work gets done here.
        # Walk the tree under the `container`, looking at each object's state, and 
        # create, update or delete it as necessary.

        self._sync_child_objects(self.container)
        super().build_kml(root, with_children)


    def _sync_child_objects(self, obj: _BaseObject) -> None:
        for dc in obj._direct_children:
            dcobj = getattr(obj, dc.name, None)
            if isinstance(dcobj, _BaseObject):
                if dcobj.state == ObjectState.CREATING:
                    self.update.creates.append(ObjectChild(obj, dcobj))
                elif dcobj.state == ObjectState.CHANGING:
                    self.update.changes.append(ObjectChild(obj, dcobj))
                elif dcobj.state in (ObjectState.DELETE_CHANGED, ObjectState.DELETE_CREATED):
                    self.update.deletes.append(ObjectChild(obj, dcobj))
                dcobj.update_generated()
                self._sync_child_objects(dcobj)
            elif isinstance(dcobj, Iterable):
                for iobj in dcobj:
                    if isinstance(iobj, _BaseObject):
                        self._sync_child_objects(iobj)
        if isinstance(obj, _ListObject):
            for lcobj in (cast(_BaseObject, lc) for lc in obj):
                if lcobj._state == ObjectState.CREATING:
                    self.update.creates.append(ObjectChild(obj, lcobj))
                elif lcobj.state == ObjectState.CHANGING:
                    self.update.changes.append(ObjectChild(obj, lcobj))
                elif lcobj.state in (ObjectState.DELETE_CHANGED, ObjectState.DELETE_CREATED):
                    self.update.deletes.append(ObjectChild(obj, lcobj))
                lcobj.update_generated()
                self._sync_child_objects(lcobj)
