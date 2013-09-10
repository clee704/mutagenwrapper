from .exceptions import MutagenWrapperError, ConflictError, UnsupportedFormatError
from .version import __version__ as version
from ._wrappers import TagsWrapper
from ._flac import FLACTagsWrapper
from ._mp4 import MP4TagsWrapper
from ._mp3 import MP3TagsWrapper


def read_tags(name, raw=False, format=None):
    """
    Returns tags in the audio file as a :class:`TagsWrapper`, a dictionary-like
    object with mapped tag keys and values. If *raw* is *True*, returns a raw
    mutagen object with non-mapped keys and values.

    Currently it supports FLAC, MP3, iTunes MP4 (.m4a) files. File format is
    determined by extension, but you can specify it by `format` (possible
    values: 'flac', 'mp3', 'm4a').

    """
    wrappers = {
        'flac': FLACTagsWrapper,
        'mp3': MP3TagsWrapper,
        'm4a': MP4TagsWrapper,
    }
    if format is None: format = name.rsplit('.', 1)[-1]
    if format in wrappers:
        cls = wrappers[format]
        return cls(name) if not raw else cls.__raw_class__(name)
    else:
        raise UnsupportedFormatError()
