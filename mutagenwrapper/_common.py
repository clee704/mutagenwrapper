class TagHandler(object):

    def __init__(self, original_key):
        self.original_key = original_key

    def get(self, tags):
        raise NotImplementedError()

    def set(self, tags, value):
        raise NotImplementedError()

    def del_(self, tags):
        raise NotImplementedError()


class SimpleTagHandler(TagHandler):

    def get(self, tags):
        return tags[self.original_key]

    def set(self, tags, value):
        tags[self.original_key] = value

    def del_(self, tags):
        del tags[self.original_key]


class TextTagHandler(SimpleTagHandler):

    def set(self, tags, value):
        if isinstance(value, basestring):
            value = [value]
        self._set_override_me(tags, value)

    def _set_override_me(self, tags, value):
        tags[self.original_key] = value


class PairTagHandler(TagHandler):

    def __init__(self, original_key, index):
        self.original_key = original_key
        self.index = index
