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
