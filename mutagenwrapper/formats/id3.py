import mutagen.id3
import mutagen.mp3
import mutagen.trueaudio

from ..bases import (TagHandler, DefaultTagHandler, PairTagHandler,
                     FreeformTagsWrapper, PrefixFreeformTagMixin, Format)


class ID3PairTagHandler(PairTagHandler):

    def _get_data(self, v):
        return v.text if v else []

    def _set_data(self, obj, v):
        obj.raw[self.name] = mutagen.id3.TRCK(encoding=3, text=v)

    def _decode_value(self, v):
        try:
            v = v.split('/')[self.index]
            try:
                v = int(v)
            except (TypeError, ValueError):
                pass
            return v
        except IndexError:
            return None

    def _update_value(self, v, old_v):
        # XXX foobar2000 uses TXXX:TOTALTRACKS when there is tracktotal
        # but no tracknumber. I think dealing with the problem that way
        # is too complicated than it's worth. I'll just set tracknumber
        # to 0 if it doesn't exist when tracktotal is being set,
        # and never read tracktotal from TXXX:TOTALTRACKS,
        # thus breaking the compatibility with foobar2000 when tags are
        # that clumsy.
        #
        # Anyway, obsessive-compulsive music geeks shouldn't let
        # their tags have tracktotal without tracknumber. That's insane.
        new_v = old_v.split('/') if old_v else [0, None]
        if len(new_v) == 1:
            new_v.append(None)
        new_v[self.index] = str(v)
        if new_v[1] == None:
            del new_v[1]
        return '/'.join(new_v)


class ID3PictureTagHandler(TagHandler):

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, type):
        value = obj.raw.get(self.name)
        if value:
            value = value.data
        return self._from_list(value)

    # TODO picture


class ID3TagSetterMixin(object):

    def __set__(self, obj, value):
        value = self._to_list(value)
        if self.name not in obj.raw:
            cls = getattr(mutagen.id3, self.name)
            frame = cls(encoding=3, text=value)
            obj.raw[self.name] = frame
        else:
            obj.raw[self.name].text = value


class ID3DateTagHandler(ID3TagSetterMixin, DefaultTagHandler):

    def __get__(self, obj, type):
        value = obj.raw.get(self.name)
        if not value:
            return
        value = [v.text for v in value.text]
        return self._from_list(value)

    def __set__(self, obj, value):
        value = self._to_list(value)
        value = [mutagen.id3.ID3TimeStamp(v) for v in value]
        super(ID3DateTagHandler, self).__set__(obj, value)


class ID3TextTagHandler(ID3TagSetterMixin, DefaultTagHandler):

    def __get__(self, obj, type):
        value = obj.raw.get(self.name)
        if value:
            value = value.text
        return self._from_list(value)


class ID3CustomTagHandler(PrefixFreeformTagMixin, ID3TextTagHandler):
    prefix = 'TXXX:'

    def __init__(self, name):
        self.name = self.__class__.encode_custom_name(name)

    def __set__(self, obj, value):
        value = self._to_list(value)
        if self.name not in obj.raw:
            desc = self.__class__.decode_custom_name(self.name)
            frame = mutagen.id3.TXXX(encoding=3, desc=desc, text=value)
            obj.raw[self.name] = frame
        else:
            obj.raw[self.name].text = value


class ID3TagsWrapper(FreeformTagsWrapper):
    freeform_tag_handler = ID3CustomTagHandler

    album                = ID3TextTagHandler('TALB')
    albumartist          = ID3TextTagHandler('TPE2')
    albumartistsortorder = ID3TextTagHandler('TSO2')
    albumsortorder       = ID3TextTagHandler('TSOA')
    artist               = ID3TextTagHandler('TPE1')
    artistsortorder      = ID3TextTagHandler('TSOP')
    # TODO id3 comment
    # comment              = ID3CommentTagHandler()
    composer             = ID3TextTagHandler('TCOM')
    composersortorder    = ID3TextTagHandler('TSOC')
    conductor            = ID3TextTagHandler('TPE3')
    copyright            = ID3TextTagHandler('TCOP')
    date                 = ID3DateTagHandler('TDRC')
    discnumber           = ID3PairTagHandler('TPOS', 0)
    disctotal            = ID3PairTagHandler('TPOS', 1)
    encodedby            = ID3TextTagHandler('TENC')
    genre                = ID3TextTagHandler('TCON')
    grouping             = ID3TextTagHandler('TIT1')
    lyrics               = ID3TextTagHandler('TEXT')
    picture              = ID3PictureTagHandler('APIC:')
    title                = ID3TextTagHandler('TIT2')
    titlesortorder       = ID3TextTagHandler('TSOT')
    tracknumber          = ID3PairTagHandler('TRCK', 0)
    tracktotal           = ID3PairTagHandler('TRCK', 1)


class ID3Format(Format):
    name = 'ID3'
    raw_classes = {
        'mp3': mutagen.mp3.MP3,
        'mp2': mutagen.mp3.MP3,
        'tta': mutagen.trueaudio.TrueAudio,
    }
    wrapper_class = ID3TagsWrapper
