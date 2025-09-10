"""NetworkLinkControl module."""

from datetime import datetime
from itertools import islice

from lxml import etree  # type: ignore

from pyLiveKML import KML_UPDATE_CONTAINER_LIMIT_DEFAULT
from pyLiveKML.errors import NetworkLinkControlUpdateLimited
from pyLiveKML.objects.AbstractView import AbstractView
from pyLiveKML.objects.Container import Container
from pyLiveKML.objects.Folder import Folder
from pyLiveKML.objects.Object import (
    _BaseObject,
    _DeletableMixin,
    _DependentDef,
    _FieldDef,
    ObjectChild,
    ObjectState,
)
from pyLiveKML.objects.Update import Update


class NetworkLinkControl(_BaseObject):
    """A KML `<NetworkLinkControl>` tag constructor.

    Controls the behavior of files fetched by a `NetworkLink`.

    References
    ----------
    * https://developers.google.com/kml/documentation/kmlreference#networklinkcontrol

    Parameters
    ----------
    target_href : str
        Used to construct an embedded `Update` instance.
    container : Container | None, default = None
        The root `Container` for synchronization. If `None`, a `Folder` named "root" will
        be created.
    update_limit : int, default = KML_UPDATE_CONTAINER_LIMIT_DEFAULT
        The maximum number of entries per synchronization update.
    min_refresh_period : float | None, default = None
        Specified in seconds, `min_refresh_period` is the minimum allowed time between
        fetches of the file. This parameter allows servers to throttle fetches of a
        particular file and to tailor refresh rates to the expected rate of change to the
        data.
    max_session_length : float | None, default = None
        Specified in seconds, `max_session_length` is the maximum amount of time for
        which the client `NetworkLink` can remain connected. The default value of -1
        indicates not to terminate the session explicitly.
    cookie : str | None, default = None
        Use this element to append a string to the URL query on the next refresh of the
        network link. You can use this data in your script to provide more intelligent
        handling on the server side, including version querying and conditional file
        delivery.
    message : str | None, default = None
        You can deliver a pop-up message, such as usage guidelines for your
        `NetworkLink`. The message appears when the `NetworkLink` is first loaded into
        Google Earth, or when it is changed in the `NetworkLink` control.
    link_name : str | None, default = None
        You can control the name of the `NetworkLink` from the server, so that changes
        made to the name on the client side are overridden by the server.
    link_description : str | None, default = None
        You can control the description of the `NetworkLink` from the server, so that
        changes made to the description on the client side are overridden by the server.
    link_snippet : str | None, default = None
        You can control the snippet for the network link from the server, so that changes
        made to the snippet on the client side are overridden by the server.
    link_snippet_max_lines : int, default = 2
        An integer that specifies the maximum number of snippet lines to display.
    link_expires : datetime | None, default = None
        You can specify a `datetime` at which the link should be refreshed. This
        specification takes effect only if the `refresh_mode` in `Link` has a value of
        `ON_EXPIRE`.
    abstract_view : AbstractView | None, default = None
        A `Camera` or `LookAt` that will set the viewing point when the `NetworkLink`
        loads.

    Attributes
    ----------
    container : Container | None
    update_limit : int
    min_refresh_period : float | None
    max_session_length : float | None
    cookie : str | None
    message : str | None
    link_name : str | None
    link_description : str | None
    link_snippet : str | None
    link_snippet_max_lines : int
    link_expires : datetime | None
    abstract_view : AbstractView | None
    update : Update
        An embedded `Update` instance that is used for synchronization.


    """

    _kml_tag = "NetworkLinkControl"
    _kml_fields = _BaseObject._kml_fields + (
        _FieldDef("min_refresh_period", "minRefreshPeriod"),
        _FieldDef("max_session_length", "maxSessionLength"),
        _FieldDef("cookie"),
        _FieldDef("message"),
        _FieldDef("link_name", "linkName"),
        _FieldDef("link_description", "linkDescription"),
        _FieldDef("link_expires", "linkExpires"),
    )
    _kml_dependents = _BaseObject._kml_dependents + (
        _DependentDef("abstract_view"),
        _DependentDef("update"),
    )
    _suppress_id = True

    def __init__(
        self,
        target_href: str,
        container: Container | None = None,
        update_limit: int = KML_UPDATE_CONTAINER_LIMIT_DEFAULT,
        min_refresh_period: float | None = None,
        max_session_length: float | None = None,
        cookie: str | None = None,
        message: str | None = None,
        link_name: str | None = None,
        link_description: str | None = None,
        link_snippet: str | None = None,
        link_snippet_max_lines: int = 2,
        link_expires: datetime | None = None,
        abstract_view: AbstractView | None = None,
    ):
        """NetworkLinkControl instance constructor."""
        super().__init__()
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
        self.link_snippet_max_lines = link_snippet_max_lines
        self.link_expires = link_expires
        self.abstract_view = abstract_view
        self.update = Update(target_href)

    def construct_sync(
        self,
        with_children: bool = True,
        with_dependents: bool = True,
    ) -> etree.Element:
        """Construct a KML synchronization update.

        The real work gets done here.

        Walks the tree under `container`, looking at each object's state, and create,
        update or delete it as necessary.

        Parameters
        ----------
        with_children : bool, default = True
            Whether the `children` of the `NetworkLinkControl`, or any child or
            dependents objects, should be constructed as sub-tags.
        with_dependents : bool, default = True
            Whether the `dependents` of the `NetworkLinkControl`, or any child or
            dependent objects, should be constructed as sub-tags.

        :returns: A `<NetworkLinkControl>` tag, including the synchronization update.
        :rtype: `etree.Element`

        """
        root = etree.Element(self.kml_tag)
        self.build_kml(root, with_children, with_dependents)
        try:
            self._sync_child_objects(self.container)
        except NetworkLinkControlUpdateLimited:
            pass
        return root

    def _sync_child_objects(self, obj: _BaseObject) -> None:
        update_generated: bool
        for d_obj in obj.dependents:
            update_generated = False
            if d_obj.child.state == ObjectState.CREATING:
                self.update.creates.append(d_obj)
                update_generated = True
            elif d_obj.child.state == ObjectState.CHANGING:
                self.update.changes.append(d_obj)
                update_generated = True
            elif d_obj.child.state in (
                ObjectState.DELETE_CHANGED,
                ObjectState.DELETE_CREATED,
            ):
                self.update.deletes.append(d_obj)
                update_generated = True
            if update_generated:
                d_obj.child.synchronized()
            if len(self.update) >= self.update_limit:
                raise NetworkLinkControlUpdateLimited
            if isinstance(d_obj.child, _BaseObject):
                self._sync_child_objects(d_obj.child)

        for c_obj in obj.children:
            update_generated = False
            if c_obj.child.state == ObjectState.CREATING:
                self.update.creates.append(c_obj)
                update_generated = True
            elif c_obj.child.state == ObjectState.CHANGING:
                self.update.changes.append(c_obj)
                update_generated = True
            elif c_obj.child.state in (
                ObjectState.DELETE_CHANGED,
                ObjectState.DELETE_CREATED,
            ):
                self.update.deletes.append(c_obj)
                update_generated = True
            if update_generated:
                c_obj.child.synchronized()
            if len(self.update) >= self.update_limit:
                raise NetworkLinkControlUpdateLimited
            if isinstance(c_obj.child, _BaseObject):
                self._sync_child_objects(c_obj.child)

        if isinstance(obj, _DeletableMixin):
            limit = self.update_limit - len(self.update)
            deletes = [
                ObjectChild(obj, delobj) for delobj in islice(obj._deleted, limit)
            ]
            self.update.deletes.extend(deletes)
            obj._deleted = obj._deleted[len(deletes) :]

    def build_kml(
        self,
        root: etree.Element,
        with_children: bool = True,
        with_dependents: bool = True,
    ) -> None:
        """Build the KML sub-tags for this `NetworkLinkControl` and append it to the provided `etree.Element`.

        Overridden from :class:`pyLiveKML.objects.Object.Object` to perform some
        additional build steps.

        Parameters
        ----------
        root : etree.Element
            The tag into which the sub-tags are to be inserted.
        with_children : bool, default = True
            Whether the `children` of the `NetworkLinkControl`, or any child or
            dependents objects, should be constructed as sub-tags.
        with_dependents : bool, default = True
            Whether the `dependents` of the `NetworkLinkControl`, or any child or
            dependent objects, should be constructed as sub-tags.

        """
        super().build_kml(root, with_children, with_dependents)
        if self.link_snippet is not None:
            attribs = {}
            if self.link_snippet_max_lines is not None:
                attribs["maxLines"] = str(self.link_snippet_max_lines)
            etree.SubElement(root, "linkSnippet", attribs).text = self.link_snippet
