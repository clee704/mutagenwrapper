from os import path
import tempfile

import pytest

from mutagenwrapper import enable_case_insensitive


here = path.abspath(path.dirname(__file__))
data_dir = lambda x: path.join(here, 'data', x)
bases = ['lame.mp3',
         'oggvorbis.ogg',
         'flac.flac',
         'alac.m4a']


@pytest.fixture(params=bases)
def path_basic(request):
    return data_dir('1_basic_{}'.format(request.param))


@pytest.fixture(params=bases)
def path_custom(request):
    return data_dir('2_custom_{}'.format(request.param))


@pytest.fixture
def tempcopy():
    def func(path):
        ext = path.rsplit('.', 1)[-1]
        tf = tempfile.NamedTemporaryFile(suffix='.' + ext)
        with open(path, 'rb') as f:
            tf.write(f.read())
        tf.seek(0, 0)
        return tf
    return func


@pytest.yield_fixture
def with_case_insensitive_enabled():
    enable_case_insensitive(True)
    yield
    enable_case_insensitive(False)
