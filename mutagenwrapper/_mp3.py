import re

from mutagen.mp3 import MP3
from mutagen.id3 import TextFrame
import mutagen.mp3

from ._wrappers import FreeformTagsWrapper
from ._handlers import TagHandler, TextTagHandler, PairTagHandler


class MP3PairTagHandler(PairTagHandler):

    def get(self, tags):
        values = []
        for t in tags[self.original_key]:
            try:
                values.append(t.split('/')[self.index])
            except IndexError:
                values.append(None)
        return values


class MP3PictureTagHandler(TagHandler):

    def get(self, tags):
        return [tags[self.original_key].data]


class MP3TagSetter(object):

    def _set_id3(self, tags, value):
        if self.original_key not in tags:
            cls = getattr(mutagen.id3, self.original_key)
            frame = cls(encoding=3, text=value)
            tags[self.original_key] = frame
        else:
            tags[self.original_key].text = value


class MP3DateTagHandler(TextTagHandler, MP3TagSetter):

    def get(self, tags):
        return [s.text for s in tags[self.original_key].text]

    def _set_override_me(self, tags, value):
        self._set_id3(tags, [mutagen.id3.ID3TimeStamp(v) for v in value])


class MP3TextTagHandler(TextTagHandler, MP3TagSetter):

    def get(self, tags):
        return tags[self.original_key].text

    def _set_override_me(self, tags, value):
        self._set_id3(tags, value)


class MP3FreeformTagHandler(MP3TextTagHandler):
    __freeform_pattern__ = '^TXXX:(.*)$'

    def _set_override_me(self, tags, value):
        if self.original_key not in tags:
            desc = re.match(self.__freeform_pattern__, self.original_key).group(1)
            frame = mutagen.id3.TXXX(encoding=3, desc=desc, text=value)
            tags[self.original_key] = frame
        else:
            tags[self.original_key].text = value


class ID3Hack(MP3):

    def loaded_frame(self, tag):
        key = tag.HashKey
        if key in self and isinstance(tag, TextFrame):
            self[key].extend(tag.text)
        else:
            self[key] = tag


class MP3TagsWrapper(FreeformTagsWrapper):
    __raw_class__ = ID3Hack
    __handlers__ = {
        'album':                MP3TextTagHandler('TALB'),
        'albumartist':          MP3TextTagHandler('TPE2'),
        'albumartistsortorder': MP3TextTagHandler('TSO2'),
        'albumsortorder':       MP3TextTagHandler('TSOA'),
        'artist':               MP3TextTagHandler('TPE1'),
        'artistsortorder':      MP3TextTagHandler('TSOP'),
        'composer':             MP3TextTagHandler('TCOM'),
        'composersortorder':    MP3TextTagHandler('TSOC'),
        'conductor':            MP3TextTagHandler('TPE3'),
        'copyright':            MP3TextTagHandler('TCOP'),
        'date':                 MP3DateTagHandler('TDRC'),
        'discnumber':           MP3PairTagHandler('TPOS', 0),
        'disctotal':            MP3PairTagHandler('TPOS', 1),
        'encodedby':            MP3TextTagHandler('TENC'),
        'genre':                MP3TextTagHandler('TCON'),
        'grouping':             MP3TextTagHandler('TIT1'),
        'pictures':             MP3PictureTagHandler('APIC:'),
        'title':                MP3TextTagHandler('TIT2'),
        'titlesortorder':       MP3TextTagHandler('TSOT'),
        'tracknumber':          MP3PairTagHandler('TRCK', 0),
        'tracktotal':           MP3PairTagHandler('TRCK', 1),
        'lyrics':               MP3TextTagHandler('TEXT'),
    }
    __freeform_pattern__ = '^TXXX:(.*)$'
    __freeform_format__ = 'TXXX:{0}'
    __freeform_handler__ = MP3FreeformTagHandler
