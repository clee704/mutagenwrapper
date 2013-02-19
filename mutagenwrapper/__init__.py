from .exceptions import MutagenWrapperError, ConflictError
from ._wrappers import TagsWrapper
from ._flac import FLACTagsWrapper
from ._mp4 import MP4TagsWrapper
from ._mp3 import MP3TagsWrapper


version = '0.0.1'


def open_tags(name, raw=False):
    """Opens the audio file and returns a :class:`TagsWrapper`,
    a dictionary-like object with mapped tag keys and values.
    If *raw* is *True*, returns a raw mutagen object with
    non-mapped keys and values.

    Currently it supports FLAC, MP3, iTunes MP4 (.m4a) files.
    """
    ext = name.rsplit('.', 1)[-1]
    classes = {
        'flac': FLACTagsWrapper,
        'mp3': MP3TagsWrapper,
        'm4a': MP4TagsWrapper,
    }
    if ext in classes:
        cls = classes[ext]
        return cls(name) if not raw else cls.__raw_class__(name)
    else:
        raise NotImplementedError()
