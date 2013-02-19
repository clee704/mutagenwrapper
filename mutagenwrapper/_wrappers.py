import re

from .exceptions import ConflictError
from ._util import cutoff


class TagsWrapper(object):
    """A dictionary-like object that wraps the raw mutagen tags. You can
    access tags via mapped tag keys, like 'artist' or 'album'.

    Note that the implementation is rather inefficient. It iterates
    the internal keys and convert them everytime :meth:`iterkeys`
    is called. Since many methods rely on that method, it could be slow
    the performance especially when there are many inclusion tests using
    :meth:`__contains__`.

    .. attribute:: filename

       Path of the file

    """

    def __init__(self, filename):
        self.filename = filename
        self._init()

    def _init(self):
        self.raw_tags = self.__raw_class__(self.filename)

    def _get_handler(self, key):
        try:
            return self.__handlers__[key]
        except KeyError:
            return self.__general_tag_handler__(key)

    def save(self):
        return self.raw_tags.save()

    def reload(self):
        self._init()

    def pprint(self, raw=False):
        print self.filename
        tags = self if not raw else self.raw_tags
        for k in sorted(tags.iterkeys()):
            v = cutoff(repr(tags[k]))
            print u'  {0}: {1}'.format(repr(k), v)

    def iterkeys(self):
        raise NotImplementedError()

    def keys(self):
        return list(self.iterkeys())

    def __len__(self):
        return len(self.keys())

    def __getitem__(self, key):
        return self._get_handler(key).get(self.raw_tags)

    def __setitem__(self, key, value):
        self._get_handler(key).set(self.raw_tags, value)

    def __delitem__(self, key):
        self._get_handler(key).del_(self.raw_tags)

    def __contains__(self, key):
        return key in self.keys()

    def __iter__(self):
        return self.iterkeys()

    def clear(self):
        for key in self.iterkeys():
            del self[key]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def find(self, key, default=None):
        """Returns a single value associated with a given key.
        Raises :exc:`KeyError` if the key is not found or
        there is no or more than one value.
        """
        try:
            v = self[key]
        except KeyError:
            return default
        if not isinstance(v, list):
            return v
        elif len(v) == 1:
            return v[0]
        else:
            raise KeyError('zero or too many values')

    def iteritems(self):
        for key in self.iterkeys():
            yield (key, self[key])

    def items(self):
        return list(self.iteritems())

    def itervalues(self):
        for key in self.iterkeys():
            yield self[key]

    def values(self):
        return list(self.itervalues())


class FreeformTagsWrapper(TagsWrapper):

    def __init__(self, filename):
        super(FreeformTagsWrapper, self).__init__(filename)
        keymap = {}
        handlers = self.__handlers__.copy()
        original_keys = set(self.raw_tags.keys())
        for key, handler in self.__handlers__.items():
            original_key = handler.original_key
            if original_key in original_keys:
                keymap.setdefault(original_key, []).append(key)
        for original_key in original_keys - set(keymap):
            m = re.match(self.__freeform_pattern__, original_key)
            if not m:
                continue
            key = m.group(1).lower()
            keymap.setdefault(original_key, []).append(key)
            if key in handlers:
                raise ConflictError('Both {0} and {1} mapped to the same key {2}'.format(original_key, handlers[key].original_key, key))
            handlers[key] = self.__freeform_handler__(original_key)
        self._keymap = keymap
        self.__handlers__ = handlers

    def __general_tag_handler__(self, key):
        try:
            return self.__handlers__[key]
        except KeyError:
            original_key = self.__freeform_format__.format(key.upper())
            handler = self.__freeform_handler__(original_key)
            self.__handlers__[key] = handler
            return handler

    def iterkeys(self):
        for original_key in self.raw_tags:
            for key in self._keymap.get(original_key, []):
                yield key
