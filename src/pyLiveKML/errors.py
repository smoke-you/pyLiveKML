"""Definitions of exceptions and/or errors."""


class FeatureError(Exception):
    """Wrapper class for errors with :class:`pyLiveKML.objects.Feature` classes and subclasses."""

    pass


class FeatureInaccessibleError(FeatureError):
    """Indicates that a :class:`pyLiveKML.objects.Feature` was not able to be updated.

    This is typically because the `Feature` instance is visible in the UI. Only `Feature`
    instances that are not visible may be updated.
    """

    pass


class TrackError(FeatureError):
    """Wrapper class for errors with :class:`pyLiveKML.objects.Track` classes and subclasses."""

    pass


class TrackElementsMismatch(TrackError):
    """Indicates that there was a problem with the `elements` data passed to a :class:`pyLiveKML.objects.Track`.

    This typically occurs when the `elements` data has mismatched lengths for the
    elements of its `extended_data` fields.
    """

    pass


class NetworkLinkControlError(Exception):
    """Wrapper class for errors with :class:`pyLiveKML.objects.NetworkLinkControl` classes and subclasses."""

    pass


class NetworkLinkControlUpdateLimited(NetworkLinkControlError):
    """Indicates that the maximum permitted number of entries has been added to a :class:`pyLiveKML.objects.Update` instance.

    Primarily intended to be used to break out of a recursive loop in
    :function:`pyLiveKML.objects.NetworkLinkControl.build_kml()` when the maximum update
    size has been reached.
    """

    pass
