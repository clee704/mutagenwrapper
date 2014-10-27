from .exceptions import (MutagenWrapperError, UnsupportedFormatError,
                         ReservedTagNameError)
from .formats.id3 import ID3Format, ID3TagsWrapper
from .formats.mp4 import MP4Format, MP4TagsWrapper
from .formats.vorbis import VorbisFormat
from .version import __version__


_formats = []
_extensions = {}


def supported_formats():
    """Returns a list of supported formats. The list contains tuples,
    each representing a metadata format name followed by file extensions.
    """
    return [(f.name, tuple(f.raw_classes)) for f in _formats]


def register_format(format):
    _formats.append(format)
    for ext in format.raw_classes:
        _extensions[ext] = format


def enable_case_insensitive(enable):
    """Enable or disable the feature that lowercases names for custom tags
    in ID3 and MP4 formats. This setting takes effect for newly created
    `MediaFile` instances. Existing `MediaFile` instances become unstable
    and should not be used once this setting is changed.
    """
    ID3TagsWrapper.case_insensitive = enable
    MP4TagsWrapper.case_insensitive = enable


class MediaFile(object):
    """A wrapper for the raw mutagen object. You can use the same names
    such as "artist" or "album" to access tags in files in different formats.
    Custom tag names are prefixed by `custom_prefix`, which is three
    underscores "___" by default.

    .. attribute:: raw

       The underlying mutagen object

    """

    def __init__(self, path):
        super(MediaFile, self).__setattr__('path', path)
        super(MediaFile, self).__setattr__('extension', path.rsplit('.', 1)[-1])
        self._init()

    def _init(self):
        if self.extension in _extensions:
            format = _extensions[self.extension]
            wrapper = format.get_wrapper(self.path, self.extension)
            super(MediaFile, self).__setattr__('wrapper', wrapper)
        else:
            raise UnsupportedFormatError

    def save(self, reload=False):
        """Save changes to the file."""
        self.wrapper.raw.save()
        if reload:
            self.reload()

    def reload(self):
        """Reload the file."""
        self._init()

    def pprint(self, raw=False):
        """Print the metadata in a human-friendly form.
        if *raw* is *True*, print the unmodified keys and values.
        """
        tags = self.wrapper if not raw else self.wrapper.raw
        print u'{}:'.format(self.path)
        names = tags.keys()
        names.sort()
        w = max(len(k) for k in names)
        fmt = u'    {{:<{}}} : {{}}'.format(w)
        for k in names:
            v = tags[k]
            try:
                v = unicode(v)
            except UnicodeDecodeError:
                v = repr(v)
            print fmt.format(k, cutoff(v, 100))

    def __getattr__(self, key):
        return getattr(self.wrapper, key)

    def __setattr__(self, key, value):
        setattr(self.wrapper, key, value)

    def __delattr__(self, key):
        delattr(self.wrapper, key)

    def __getitem__(self, key):
        return self.wrapper[key]

    def __setitem__(self, key, value):
        self.wrapper[key] = value

    def __delitem__(self, key):
        del self.wrapper[key]

    def __iter__(self):
        return iter(self.wrapper)

    def __len__(self):
        return len(self.wrapper)

    def __contains__(self, key):
        return key in self.wrapper


def cutoff(s, length=120):
    """Cuts a given string if it is longer than a given length."""
    if length < 5:
        raise ValueError('length must be >= 5')
    if len(s) <= length:
        return s
    else:
        i = (length - 2) / 2
        j = (length - 3) / 2
        return s[:i] + '...' + s[-j:]


register_format(ID3Format)
register_format(MP4Format)
register_format(VorbisFormat)
