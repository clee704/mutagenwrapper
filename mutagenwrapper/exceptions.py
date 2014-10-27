class MutagenWrapperError(Exception):
    """An ambiguous exception occurred while handling the file."""


class UnsupportedFormatError(Exception):
    """Raised when an attempt is made to read tags in a file that is not
    supported.
    """


class ReservedTagNameError(MutagenWrapperError):
    """The specified custom tag name is reserved and cannot be used."""
