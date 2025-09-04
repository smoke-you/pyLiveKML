"""utils module."""

from lxml import etree  # type: ignore


KML_UPDATE_CONTAINER_LIMIT_DEFAULT: int = 100
"""The default value for the container update limit.

The default maximum number of :class:`~pyLiveKML.KMLObjects.Feature` objects that 
will be included in each synchronization update emitted by a 
:class:`~pyLiveKML.NetworkLinkControl` object.
"""


KML_DOCTYPE: str = '<?xml version="1.0" encoding="UTF-8"?>'
"""The XML tag that opens any XML document, including any KML document."""

KML_HEADERS = {"Content-Type": "application/vnd.google-earth.kml+xml"}
"""The headers that should be included when a KML file is tranmitted via HTTP."""

__root_namespace_map = {
    "gx": "http://www.google.com/kml/ext/2.2",
    "kml": "http://www.opengis.net/kml/2.2",
    "atom": "http://www.w3.org/2005/Atom",
}
"""The namespace map that is to applied to all Google Earth KML files."""

__root_attributes = {"xmlns": "http://www.opengis.net/kml/2.2"}
"""The attributes that should be applied to all Google Earth KML files."""


def kml_root_tag() -> etree.Element:
    """Construct the opening <kml> tag, with namespaces, for a KML document.

    :return: The <kml> tag, with namespaces, that encloses the contents of a KML document.
    :rtype: etree.Element
    """
    return etree.Element("kml", nsmap=__root_namespace_map, attrib=__root_attributes)


def with_ns(tag: str) -> str:
    """Transform a Clark-notation XML string into a colon-notation XML string.

    If there is no colon in the text, just return the text. Otherwise, split the text
    into two parts at the first colon. Look up the first part as a key in
    `_root_namespace_map` and return the corresponding value, wrapped in {}, with the
    second part of the original text appended.

    For example, "gx:Track" would return "{http://www.google.com/kml/ext/2.2}Track".
    lxml publishes this as a <gx:Track> tag. Ridiculous double-entry nonsense, but it
    works.
    """
    parts = tag.split(":", 1)
    return (
        tag
        if len(parts) < 2
        else f"{{{__root_namespace_map[parts[0]]}}}{parts[1]}"
    )
