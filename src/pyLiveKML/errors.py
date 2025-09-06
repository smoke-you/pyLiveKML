"""Definitions of exceptions and/or errors."""

##########################
#
# pyLiveKML base error class
#
##########################


class KMLError(Exception):
    """Wrapper class for all pyLiveKML errors."""


##########################
#
# Feature errors
#
##########################


class FeatureError(KMLError):
    """Wrapper class for errors with :class:`pyLiveKML.objects.Feature` classes and subclasses."""

    pass


class FeatureInaccessibleError(FeatureError):
    """Indicates that a :class:`pyLiveKML.objects.Feature` was not able to be updated.

    This is typically because the `Feature` instance is visible in the UI. Only `Feature`
    instances that are not visible may be updated.
    """

    pass


##########################
#
# LinearRing errors
#
##########################


class LinearRingError(KMLError):
    """Wrapper class for errors with :class:`pyLiveKML.objects.LinearRing`."""

    pass


class LinearRingCoordsError(LinearRingError):
    """Indicates that the :attr:`pyLiveKML.objects.LinearRing.coordinates` parameter was invalid.

    This is typically because less than the minimum of 3 coordinates were supplied.
    """


##########################
#
# LineString errors
#
##########################


class LineStringError(KMLError):
    """Wrapper class for errors with :class:`pyLiveKML.objects.LineString`."""

    pass


class LineStringCoordsError(LineStringError):
    """Indicates that the :attr:`pyLiveKML.objects.LineString.coordinates` parameter was invalid.

    This is typically because less than the minimum of 2 coordinates were supplied.
    """


##########################
#
# NetworkLinkControl errors
#
##########################


class NetworkLinkControlError(KMLError):
    """Wrapper class for errors with :class:`pyLiveKML.objects.NetworkLinkControl` classes and subclasses."""

    pass


class NetworkLinkControlUpdateLimited(NetworkLinkControlError):
    """Indicates that the maximum permitted number of entries has been added to a :class:`pyLiveKML.objects.Update` instance.

    Primarily intended to be used to break out of a recursive loop in
    :function:`pyLiveKML.objects.NetworkLinkControl.build_kml()` when the maximum update
    size has been reached.
    """

    pass


##########################
#
# Track errors
#
##########################


class TrackError(FeatureError):
    """Wrapper class for errors with :class:`pyLiveKML.objects.Track` classes and subclasses."""

    pass


class TrackElementsMismatch(TrackError):
    """Indicates that there was a problem with the `elements` data passed to a :class:`pyLiveKML.objects.Track`.

    This typically occurs when the `elements` data has mismatched lengths for the
    elements of its `extended_data` fields.
    """

    pass
