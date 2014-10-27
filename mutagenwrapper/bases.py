from .exceptions import ReservedTagNameError


class TagHandler(object):

    def __get__(self, obj, type):
        raise NotImplementedError(self._niemsg('get'))

    def __set__(self, obj, value):
        raise NotImplementedError(self._niemsg('set'))

    def __delete__(self, obj):
        raise NotImplementedError(self._niemsg('delete'))

    def _niemsg(self, meth):
        cls_name = self.__class__.__name__
        return "{} doesn't implement __{}__()".format(cls_name, meth)

    def _from_list(self, value):
        if isinstance(value, list):
            if len(value) == 1:
                value = value[0]
            elif len(value) == 0:
                value = None
        return value

    def _to_list(self, value):
        if value is None:
            value = []
        elif not isinstance(value, list):
            value = [value]
        return value


class DefaultTagHandler(TagHandler):

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, type):
        value = obj.raw.get(self.name, [])
        return self._from_list(value)

    def __set__(self, obj, value):
        value = self._to_list(value)
        obj.raw[self.name] = value

    def __delete__(self, obj):
        try:
            del obj.raw[self.name]
        except KeyError:
            pass


class PairTagHandler(TagHandler):

    def __init__(self, name, index):
        self.name = name
        self.index = index

    def __get__(self, obj, type):
        value = []
        for v in obj.raw.get(self.name, []):
            value.append(self._decode_value(v))
        return self._from_list(value)

    def __set__(self, obj, value):
        # XXX When the number of values being set is smaller than
        # the existing pairs, the extra pairs are deleted.
        # For example, if (tracknumber, tracktotal) pairs are
        # [(1, 10), (2, 13)], set tracknumber to 5, then the
        # results will be [(5, 10)], without the second pair.
        # This might be undesirable, but who cares multiple values?
        value = self._to_list(value)
        old_value = self._get_data(obj.raw.get(self.name, []))
        new_value = []
        n = min(len(value), len(old_value))
        for i in xrange(n):
            new_value.append(self._update_value(value[i], old_value[i]))
        for i in xrange(n, len(value)):
            new_value.append(self._update_value(value[i], None))
        self._set_data(obj, new_value)

    def __delete__(self, obj):
        # XXX When one of a pair is deleted, the whole pair is deleted.
        # For example, if you delete x.tracknumber,
        # x.tracktotal is also deleted. it is arguably not the best behavior,
        # and should be documented for users. But there is no easy way to
        # actually delete the tag otherwise...
        try:
            del obj.raw[self.name]
        except KeyError:
            pass

    def _get_data(self, v):
        return v

    def _set_data(self, obj, v):
        obj.raw[self.name] = v

    def _decode_value(self, v):
        raise NotImplementedError

    def _update_value(self, v, old_v):
        raise NotImplementedError


class TagsWrapperMeta(type):

    def __new__(cls, name, bases, attrs):
        handlers = {}
        lut = {}
        for attrname, attr in attrs.iteritems():
            if isinstance(attr, TagHandler):
                handlers[attrname] = attr
                if hasattr(attr, 'name'):
                    lut.setdefault(attr.name, []).append(attrname)
        attrs['__handlers__'] = handlers
        attrs['__custom_handlers__'] = {}
        attrs['__lut__'] = lut
        return super(TagsWrapperMeta, cls).__new__(cls, name, bases, attrs)


class TagsWrapper(object):
    __metaclass__ = TagsWrapperMeta

    # Class variables set by metaclass
    __handlers__ = {}
    __custom_handlers__ = {}
    __lut__ = {}

    case_insensitive = False
    custom_prefix = '___'

    def __init__(self, raw):
        super(TagsWrapper, self).__setattr__('raw', raw)
        cls = self.__class__
        custom_handlers = cls.__custom_handlers__
        prefix = cls.custom_prefix
        for name in self.get_tags():
            if name.startswith(prefix) and name not in custom_handlers:
                custom_handlers[name] = self.get_custom_tag_handler(name)
                setattr(cls, name, custom_handlers[name])

    def get_tags(self):
        """Iterates the names of tags in the file."""
        raise NotImplementedError

    def get_custom_tag_handler(self, name):
        """Returns a descriptor that handles the custom tag."""
        raise NotImplementedError

    def __setattr__(self, key, value):
        cls = self.__class__
        if cls.case_insensitive:
            key = key.lower()
        try:
            getattr(self, key)
            super(TagsWrapper, self).__setattr__(key, value)
        except AttributeError:
            custom_handlers = cls.__custom_handlers__
            if key.startswith(cls.custom_prefix) and key not in custom_handlers:
                custom_handlers[key] = self.get_custom_tag_handler(key)
                setattr(cls, key, custom_handlers[key])
                setattr(self, key, value)
            else:
                raise

    # Dictionary-compatible methods
    #
    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __delitem__(self, key):
        return delattr(self, key)

    def __iter__(self):
        return iter(self.get_tags())

    def __len__(self):
        return len(list(self.get_tags()))

    def __contains__(self, key):
        for k in self.get_tags():
            if k == key:
                return True
        return False

    def get(self, key, default=None):
        try:
            return getattr(self, key)
        except KeyError:
            return default

    def keys(self):
        return list(self.get_tags())

    def iterkeys(self):
        return iter(self.get_tags())

    def values(self):
        return list(self.itervalues())

    def itervalues(self):
        for key in self.get_tags():
            yield getattr(self, key)

    def items(self):
        return list(self.iteritems())

    def iteritems(self):
        for key in self.get_tags():
            yield (key, getattr(self, key))


class FreeformTagsWrapper(TagsWrapper):

    freeform_tag_handler = None

    def get_tags(self):
        ret = set()
        cls = self.__class__
        h = cls.freeform_tag_handler
        for name, value in self.raw.iteritems():
            if not value:
                continue
            if name in cls.__lut__:
                ret.update(cls.__lut__[name])
            elif h.is_encoded_custom_name(name):
                name = h.decode_custom_name(name)
                if cls.case_insensitive:
                    name = name.lower()
                ret.add(cls.custom_prefix + name)
            else:
                # XXX not-yet-mapped non-freeform tags are ignored here
                pass
        return ret

    def get_custom_tag_handler(self, name):
        cls = self.__class__
        name = name[len(cls.custom_prefix):]
        if cls.freeform_tag_handler.encode_custom_name(name) in cls.__lut__:
            raise ReservedTagNameError
        return cls.freeform_tag_handler(name)


class PrefixFreeformTagMixin(object):

    prefix = None

    @classmethod
    def encode_custom_name(cls, name):
        return cls.prefix + name

    @classmethod
    def decode_custom_name(cls, name):
        return name[len(cls.prefix):]

    @classmethod
    def is_encoded_custom_name(cls, name):
        return name.startswith(cls.prefix)


class Format(object):

    @classmethod
    def get_wrapper(cls, path, extension):
        return cls.wrapper_class(cls.raw_classes[extension](path))
