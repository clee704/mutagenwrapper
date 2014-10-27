import mutagen.mp4

from ..bases import (TagHandler, DefaultTagHandler, PairTagHandler,
                     FreeformTagsWrapper, PrefixFreeformTagMixin, Format)


class MP4PairTagHandler(PairTagHandler):

    def _decode_value(self, v):
        return v[self.index]

    def _update_value(self, v, old_v):
        new_v = list(old_v) if old_v else [0, 0]
        new_v[self.index] = v
        return tuple(new_v)


class MP4CustomTagHandler(PrefixFreeformTagMixin, DefaultTagHandler):
    prefix = '----:com.apple.iTunes:'

    def __init__(self, name):
        self.name = self.__class__.encode_custom_name(name)

    def __get__(self, obj, type):
        value = obj.raw.get(self.name, [])
        value = [v.decode('utf-8', 'replace') for v in value]
        return self._from_list(value)

    def __set__(self, obj, value):
        value = self._to_list(value)
        obj.raw[self.name] = [v.encode('utf-8') for v in value]


class MP4TagsWrapper(FreeformTagsWrapper):
    freeform_tag_handler = MP4CustomTagHandler

    album                = DefaultTagHandler('\xa9alb')
    albumartist          = DefaultTagHandler('aART')
    albumartistsortorder = DefaultTagHandler('soaa')
    albumsortorder       = DefaultTagHandler('soal')
    artist               = DefaultTagHandler('\xa9ART')
    artistsortorder      = DefaultTagHandler('soar')
    comment              = DefaultTagHandler('\xa9cmt')
    composer             = DefaultTagHandler('\xa9wrt')
    composersortorder    = DefaultTagHandler('soco')
    conductor            = MP4CustomTagHandler('conductor')
    copyright            = DefaultTagHandler('cprt')
    date                 = DefaultTagHandler('\xa9day')
    discnumber           = MP4PairTagHandler('disk', 0)
    disctotal            = MP4PairTagHandler('disk', 1)
    encodedby            = DefaultTagHandler('\xa9too')
    genre                = DefaultTagHandler('\xa9gen')
    grouping             = DefaultTagHandler('\xa9grp')
    lyrics               = DefaultTagHandler('\xa9lyr')
    # XXX mutagen cannot read different types of covers
    # written by foobar2000. Note that foobar2000 ignores
    # multiple values written by mutagen for any tag, not just covr,
    # and uses just the last value.
    picture              = DefaultTagHandler('covr')
    title                = DefaultTagHandler('\xa9nam')
    titlesortorder       = DefaultTagHandler('sonm')
    tracknumber          = MP4PairTagHandler('trkn', 0)
    tracktotal           = MP4PairTagHandler('trkn', 1)


class MP4Format(Format):
    name = 'MP4'
    raw_classes = {
        'm4a': mutagen.mp4.MP4,
        'm4b': mutagen.mp4.MP4,
        'm4p': mutagen.mp4.MP4,
        'm4v': mutagen.mp4.MP4,
        'mp4': mutagen.mp4.MP4,
    }
    wrapper_class = MP4TagsWrapper
