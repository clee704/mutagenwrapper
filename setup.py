import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def getversion():
    with open('mutagenwrapper/version.py') as f:
        text = f.read()
        m = re.match("^__version__ = '(.*)'$", text)
        return m.group(1)

def readme():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
            return f.read()
    except Exception:
        return ''

setup(
    name = "mutagenwrapper",
    version = getversion(),
    description = "wrapper for mutagen that normalizes tags between various audio file formats",
    long_description = readme(),
    author = "Choongmin Lee",
    author_email = "choongmin@me.com",
    url = "https://github.com/clee704/mutagenwrapper",
    packages = ['mutagenwrapper'],
    install_requires = [
        'mutagen == 1.21',
    ],
    license = "MIT License",
    keywords = "audio metadata tags",
    classifiers = [
        # Full list is here: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Utilities",
    ]
)
