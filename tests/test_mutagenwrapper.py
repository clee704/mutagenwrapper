# -*- coding: utf-8 -*-
import pytest

from mutagenwrapper import MediaFile, ReservedTagNameError


basic_ref = {
    'artist': 'Daft Punk',
    'title': 'Get Lucky',
    'album': 'Random Access Memories',
    'date': '2013',
    'genre': 'Electronic',
    'composer': 'Guy-Manuel de Homem-Christo, Nile Rodgers, Pharrell Williams, Thomas Bangalter',
    'tracknumber': 8,
    'tracktotal': 13,
    'discnumber': 1,
    'disctotal': 1,
}


def test_basic_read(path_basic):
    m = MediaFile(path_basic)
    assert m.artist == basic_ref['artist']
    assert m['artist'] == basic_ref['artist']
    for k in sorted(basic_ref.iterkeys()):
        assert getattr(m, k) == basic_ref[k]
        assert m[k] == basic_ref[k]


def test_basic_write(path_basic, tempcopy):
    with tempcopy(path_basic) as tf:
        m = MediaFile(tf.name)
        assert m.artist == basic_ref['artist']

        m.artist = 'DAFT PUNK'
        assert m.artist == 'DAFT PUNK'
        m.save(reload=True)
        assert m.artist == 'DAFT PUNK'

        m.album = ['Foo', 'Bar']
        assert m.album == ['Foo', 'Bar']
        m.save(reload=True)
        assert m.album == ['Foo', 'Bar']

        # XXX Appending values are NOT supported (e.g. m.album.append(...))
        # and should not used (behaviors vary for different formats,
        # or even different tags in the same format).

        m.date = '2014-08-15'
        assert m.date == '2014-08-15'
        m.save(reload=True)
        assert m.date == '2014-08-15'

        m.tracknumber = 1
        assert m.tracknumber == 1
        assert m.tracktotal == 13
        m.save(reload=True)
        assert m.tracknumber == 1
        assert m.tracktotal == 13

        del m.artist
        assert m.artist is None
        m.save(reload=True)
        assert m.artist is None

        del m.date
        assert m.date is None
        m.save(reload=True)
        assert m.date is None

        del m.tracknumber
        assert m.tracknumber is None
        m.save(reload=True)
        assert m.tracknumber is None

        m.tracknumber = 9
        assert m.tracknumber == 9
        m.save(reload=True)
        assert m.tracknumber == 9

        m.tracktotal = 42
        assert m.tracknumber == 9
        assert m.tracktotal == 42
        m.save(reload=True)
        assert m.tracknumber == 9
        assert m.tracktotal == 42


def test_basic_write_reserved(path_basic, tempcopy):
    with tempcopy(path_basic) as tf:
        m = MediaFile(tf.name)
        if m.wrapper.__class__.__name__ == 'ID3TagsWrapper':
            # conductor is a regular tag in ID3
            return
        with pytest.raises(ReservedTagNameError):
            m.___conductor = 'Abbado'


def test_basic_write_unicode(path_basic, tempcopy):
    with tempcopy(path_basic) as tf:
        m = MediaFile(tf.name)

        m.artist = u'Frédéric François Chopin'
        m.save(reload=True)
        assert m.artist == u'Frédéric François Chopin'

        m.album = [u'Études', u'Klavierstück']
        m.save(reload=True)
        assert m.album == [u'Études', u'Klavierstück']


def test_basic_read_picture(path_basic):
    m = MediaFile(path_basic)
    #assert m.picture == ''
