import mutagen.flac
import mutagen.oggflac
import mutagen.oggspeex
import mutagen.oggtheora
import mutagen.oggvorbis

from ..bases import TagHandler, DefaultTagHandler, TagsWrapper, Format
from ..exceptions import ReservedTagNameError


class VorbisIntegerTagHandler(DefaultTagHandler):
    """Converts values to integers when reading.
    They are converted back to strings when writing,
    as everything is stored as a string in Vorbis comment.
    """

    def __get__(self, obj, type):
        value = obj.raw.get(self.name, [])
        value = map(int, value)
        return self._from_list(value)

    def __set__(self, obj, value):
        value = self._to_list(value)
        value = map(unicode, value)
        obj.raw[self.name] = value


# TODO ogg files don't have pictures but byte64-encoded metadata_block_picture
# in Vorbis comment.
class VorbisPictureTagHandler(TagHandler):

    def __get__(self, obj, type):
        value = [p.data for p in obj.raw.pictures]
        return self._from_list(value)

    # TODO add abstract picture class that unifies
    # mutagen.flac.Picture, mutagen.mp4.MP4Cover,
    # mutagen.id3.APIC. The code below works only if
    # value is an instance of mutagen.flac.Picture, breaking
    # the symmetry (__get__() returns the raw image data).
    # def __set__(self, obj, value):
    #     value = self._to_list(value)
    #     obj.raw.clear_pictures()
    #     for v in value:
    #         obj.raw.add_picture(v)

    def __delete__(self, obj):
        obj.raw.clear_pictures()


class VorbisTagsWrapper(TagsWrapper):
    case_insensitive = True

    album                = DefaultTagHandler('album')
    albumartist          = DefaultTagHandler('albumartist')
    albumartistsortorder = DefaultTagHandler('albumartistsortorder')
    albumsortorder       = DefaultTagHandler('albumsortorder')
    artist               = DefaultTagHandler('artist')
    artistsortorder      = DefaultTagHandler('artistsortorder')
    comment              = DefaultTagHandler('comment')
    composer             = DefaultTagHandler('composer')
    composersortorder    = DefaultTagHandler('composersortorder')
    conductor            = DefaultTagHandler('conductor')
    copyright            = DefaultTagHandler('copyright')
    date                 = DefaultTagHandler('date')
    discnumber           = VorbisIntegerTagHandler('discnumber')
    disctotal            = VorbisIntegerTagHandler('disctotal')
    encodedby            = DefaultTagHandler('encodedby')
    genre                = DefaultTagHandler('genre')
    grouping             = DefaultTagHandler('grouping')
    lyrics               = DefaultTagHandler('lyrics')
    picture              = VorbisPictureTagHandler()
    title                = DefaultTagHandler('title')
    titlesortorder       = DefaultTagHandler('titlesortorder')
    tracknumber          = VorbisIntegerTagHandler('tracknumber')
    tracktotal           = VorbisIntegerTagHandler('tracktotal')

    def get_tags(self):
        cls = self.__class__
        for name, value in self.raw.iteritems():
            if not value:
                continue
            if name in cls.__lut__:
                yield name
            else:
                yield cls.custom_prefix + name
        if hasattr(self.raw, 'pictures'):
            yield 'picture'

    def get_custom_tag_handler(self, name):
        cls = self.__class__
        name = name[len(cls.custom_prefix):]
        if name in cls.__lut__:
            raise ReservedTagNameError
        return DefaultTagHandler(name)


class VorbisFormat(Format):
    name = 'Vorbis'
    raw_classes = {
        'flac': mutagen.flac.FLAC,
        'ogg': mutagen.oggvorbis.OggVorbis,
        'oggflac': mutagen.oggflac.OggFLAC,
        'oggspeex': mutagen.oggspeex.OggSpeex,
        'oggtheora': mutagen.oggtheora.OggTheora,
    }
    wrapper_class = VorbisTagsWrapper
