class MutagenWrapperError(Exception):
    """An ambiguous exception occurred while handling the file."""
    pass


class ConflictError(MutagenWrapperError):
    """A custom tag key in your file has the same name as one of
    the mapped tag keys."""
    pass
