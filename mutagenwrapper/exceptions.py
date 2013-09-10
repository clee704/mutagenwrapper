class MutagenWrapperError(Exception):
    """An ambiguous exception occurred while handling the file."""
    pass


class ConflictError(MutagenWrapperError):
    """A custom tag key in your file has the same name as one of
    the mapped tag keys."""
    pass


class UnsupportedFormatError(Exception):
    """Raised when an attempt is made to read tags in a file that is not
    supported."""
    pass
