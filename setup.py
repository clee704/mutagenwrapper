from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
exec(open(path.join(here, 'mutagenwrapper/version.py')).read())  # import __version__

def readme():
    try:
        with open(path.join(here, 'README'), encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ''

setup(
    name = 'mutagenwrapper',
    version = __version__,
    packages = find_packages(exclude=['docs', 'tests*']),
    description = 'a thin wrapper for mutagen, providing a unified interface for various tagging formats',
    long_description = readme(),
    url = 'https://github.com/clee704/mutagenwrapper',
    author = 'Choongmin Lee',
    author_email = 'choongmin@me.com',
    license = 'MIT',
    classifiers = [
        # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords = 'audio metadata tags',
    install_requires = [
        'mutagen == 1.24',
    ],
)
