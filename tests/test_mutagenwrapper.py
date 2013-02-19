# -*- coding: UTF-8 -*-
import os
import shutil
import sys

import pytest

__dir__ = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(__dir__, '..'))
import mutagenwrapper


os.chdir(__dir__)


_read_memoize = {}
def read(name):
    if name in _read_memoize:
        return _read_memoize[name]
    with open(name) as f:
        rv = f.read()
        _read_memoize[name] = rv
        return rv


def open_tags(tmpdir, name):
    p = tmpdir.join(os.path.basename(name))
    p.write(read(name), 'wb')
    return mutagenwrapper.open_tags(p.strpath)


@pytest.fixture(params=['flac', 'm4a', 'mp3'])
def tags(tmpdir, request):
    return open_tags(tmpdir, 'data/silence.{0}'.format(request.param))


@pytest.fixture
def cover():
    with open('data/cover.jpg') as f:
        return f.read()


@pytest.fixture(params=['m4a'])
def conflict_tags(tmpdir, request):
    with pytest.raises(mutagenwrapper.ConflictError):
        open_tags(tmpdir, 'data/conflict.{0}'.format(request.param))


@pytest.fixture(params=['m4a'])
def multiframe_tags(tmpdir, request):
    return open_tags(tmpdir, 'data/multiframe.{0}'.format(request.param))


class TestTagsWrapper(object):

    def test_reload(self, tags):
        tags['title'] = 'Temporary Title'
        del tags['composer']
        tags.reload()
        assert tags['title'] != 'Temporary Title'
        assert 'composer' in tags

    def test_iter(self, tags):
        keys = []
        for k in tags:
            keys.append(k)
        assert sorted(keys) == sorted(tags.keys())

    def test_get_picture(self, tags, cover):
        assert tags['pictures'] == [cover]

    def test_get_text(self, tags):
        assert tags['title'] == [u'Hello, world!']

    def test_get_text_many(self, tags):
        assert tags['composer'] == [u'Bach', u'Beethoven']

    def test_get_text_freeform(self, tags):
        assert tags['freeform'] == [u'Freeform Text']

    def test_get_text_freeform_many(self, tags):
        assert tags['colors'] == [u'red', u'blue', u'green']

    def test_get_text_tuple(self, tags):
        assert tags['tracknumber'] == [u'1', u'2']

    def test_get_text_unicode(self, tags):
        assert tags['uni'] == [u'Frédéric Chopin']

    def test_find_text(self, tags):
        assert tags.find('title') == u'Hello, world!'

    def test_find_text_many(self, tags):
        with pytest.raises(KeyError):
            tags.find('composer')

    def test_find_text_not_present(self, tags):
        assert tags.find('abcdef', 'default') == 'default'

    def test_set_text(self, tags):
        tags['title'] = 'New Title'
        tags.save()
        tags.reload()
        assert tags['title'] == [u'New Title']

    def test_set_text_overwrite(self, tags):
        tags['title'] = 'New Title'
        tags.save()
        tags.reload()
        assert tags['title'] == [u'New Title']

        tags['title'] = 'New Title 2'
        tags.save()
        tags.reload()
        assert tags['title'] == [u'New Title 2']

    def test_set_text_unicode(self, tags):
        tags['title'] = u"12 Études d'exécution transcendante"
        tags.save()
        tags.reload()
        assert tags['title'] == [u"12 Études d'exécution transcendante"]

    def test_set_text_many(self, tags):
        tags['composer'] = ['Shostakovich', 'Khachaturian', 'Puccini']
        tags.save()
        tags.reload()
        assert tags['composer'] == [u'Shostakovich', u'Khachaturian', u'Puccini']

    def test_set_text_new(self, tags):
        tags['date'] = '1928'
        tags.save()
        tags.reload()
        assert tags['date'] == [u'1928']

    def test_set_text_freeform(self, tags):
        tags['hello'] = ['world']
        tags.save()
        tags.reload()
        assert tags['hello'] == [u'world']

    def test_set_text_many_freeform(self, tags):
        tags['foo'] = ['x', 'y', 'z']
        tags.save()
        tags.reload()
        assert tags['foo'] == [u'x', u'y', u'z']

    def test_set_text_unicode_freeform(self, tags):
        tags['foo'] = [u'x', u'y', u'z']
        tags.save()
        tags.reload()
        assert tags['foo'] == [u'x', u'y', u'z']

    def test_set_text_overwrite(self, tags):
        tags['freeform'] = ['world']
        tags.save()
        tags.reload()
        assert tags['freeform'] == [u'world']

    def test_del_text(self, tags):
        del tags['title']
        tags.save()
        tags.reload()
        assert 'title' not in tags

    def test_conflict(self, conflict_tags):
        pass

    def test_multiframe(self, multiframe_tags):
        assert multiframe_tags['performer'] == [u'performer1', u'performer2']
