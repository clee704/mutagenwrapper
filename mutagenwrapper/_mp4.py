from mutagen.mp4 import MP4, MP4Tags

from ._wrappers import FreeformTagsWrapper
from ._handlers import TextTagHandler, PairTagHandler


class MP4PairTagHandler(PairTagHandler):

    def get(self, tags):
        return [unicode(t[self.index]) for t in tags[self.original_key]]


class MP4FreeformTagHandler(TextTagHandler):

    def get(self, tags):
        values_utf8 = tags[self.original_key]
        return [s.decode('UTF-8', 'replace') for s in values_utf8]

    def _set_override_me(self, tags, value):
        tags[self.original_key] = [u.encode('UTF-8') for u in value]


class MP4TagsHack(MP4Tags):

    def __init__(self, *args, **kwargs):
        self._loading = False
        super(MP4TagsHack, self).__init__(*args, **kwargs)

    def load(self, *args, **kwargs):
        self._loading = True
        super(MP4TagsHack, self).load(*args, **kwargs)
        self._loading = False

    def __setitem__(self, key, value):
        sup = super(MP4Tags, self)
        if self._loading and key in self:
            try:
                self[key].extend(value)
            except AttributeError:
                sup.__setitem__(key, value)
        else:
            sup.__setitem__(key, value)


class MP4Hack(MP4):
    MP4Tags = MP4TagsHack


class MP4TagsWrapper(FreeformTagsWrapper):
    __raw_class__ = MP4Hack
    __handlers__ = {
        'album':                TextTagHandler('\xa9alb'),
        'albumartist':          TextTagHandler('aART'),
        'albumartistsortorder': TextTagHandler('soaa'),
        'albumsortorder':       TextTagHandler('soal'),
        'artist':               TextTagHandler('\xa9ART'),
        'artistsortorder':      TextTagHandler('soar'),
        'comment':              TextTagHandler('\xa9cmt'),
        'composer':             TextTagHandler('\xa9wrt'),
        'composersortorder':    TextTagHandler('soco'),
        'copyright':            TextTagHandler('cprt'),
        'date':                 TextTagHandler('\xa9day'),
        'discnumber':           MP4PairTagHandler('disk', 0),
        'disctotal':            MP4PairTagHandler('disk', 1),
        'encodedby':            TextTagHandler('\xa9too'),
        'genre':                TextTagHandler('\xa9gen'),
        'grouping':             TextTagHandler('\xa9grp'),
        'pictures':             TextTagHandler('covr'),
        'title':                TextTagHandler('\xa9nam'),
        'titlesortorder':       TextTagHandler('sonm'),
        'tracknumber':          MP4PairTagHandler('trkn', 0),
        'tracktotal':           MP4PairTagHandler('trkn', 1),
        'lyrics':               TextTagHandler('\xa9lyr'),
    }
    __freeform_pattern__ = '^----:com.apple.iTunes:(.*)$'
    __freeform_format__ = '----:com.apple.iTunes:{0}'
    __freeform_handler__ = MP4FreeformTagHandler
