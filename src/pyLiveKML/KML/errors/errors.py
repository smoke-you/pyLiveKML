"""Definitions of exceptions/errors."""


class FeatureError(Exception):
    """Wrapper class for errors with :class:`~Feature` classes and subclasses."""

    pass


class FeatureInaccessibleError(FeatureError):
    """Indicates that a :class:`~Feature` was not able to be updated.

    This is typically because the :class:`~Feature` instance is visible in the UI. Only
    :class:`~Feature` instances that are not visible may be updated.
    """

    pass


class TrackError(FeatureError):
    """Wrapper class for errors with :class:`~Track` classes and subclasses."""

    pass


class TrackElementsMismatch(TrackError):
    """Indicates that there was a problem with the `elements` data passed to a :class:`~Track`.

    This typically occurs when the `elements` data has mismatched lengths for its
    `extended_data` fields.
    """

    pass


class NetworkLinkControlError(Exception):
    """Wrapper class for errors with :class:`~NetworkLinkControl` classes and subclasses."""

    pass


class NetworkLinkControlUpdateLimited(NetworkLinkControlError):
    """Indicates that the maximum permitted number of entries has been added to an <Update> tag.
    
    Primarily intended to be used to break out of a recursive loop in 
    `NetworkLinkControl.build_kml()` when the maximum update size has been reached.
    """
    pass
