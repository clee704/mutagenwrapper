from mutagen.flac import FLAC

from ._wrappers import TagsWrapper
from ._common import TagHandler, TextTagHandler


class FLACPictureTagHandler(TagHandler):

    def get(self, tags):
        return [p.data for p in tags.pictures]


class FLACTagsWrapper(TagsWrapper):
    __raw_class__ = FLAC
    __general_tag_handler__ = TextTagHandler
    __handlers__ = {
        'pictures': FLACPictureTagHandler('pictures'),
    }

    def iterkeys(self):
        for key in self.raw_tags:
            yield key
        if self.raw_tags.pictures:
            yield 'pictures'
