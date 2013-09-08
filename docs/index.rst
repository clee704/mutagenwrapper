.. mutagenwrapper documentation master file, created by
   sphinx-quickstart on Thu Jan 31 11:29:44 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to mutagenwrapper's documentation!
==========================================

mutagenwrapper is a wrapper for mutagen_ that uses consistent and human-readable
tag names among various tagging formats. The idea comes from foobar2000_, which
supports seamless tag management of various audio file formats.

Note that this module is still in its early development stage. Many features are
not supported like changing an album art. See `Mappings`_ for more details. There
may be undocumented limitations too.

You must backup your files if you are going to edit tags and make changes
with this module. There is no way to recover files without a backup if something
goes wrong.

mutagenwrapper can read tags with multiple values (e.g. multiple artists),
but due to the incompatibility of mutagen and foobar2000, the way it saves
tags makes them unreadable by foobar2000 in some cases,
especially for MP4 files. Hidden tags, if exist, may be lost when you make
another change and save tags in foobar2000.

.. _mutagen: http://code.google.com/p/mutagen/
.. _foobar2000: http://www.foobar2000.org/


Examples
--------

You can access tags via human-readable names. For the mappings between these
names and the actual, internal tag names, see `Mappings`_::

    >>> from mutagenwrapper import open_tags
    >>> mp3 = open_tags('test.mp3')
    >>> mp3['artist']
    [u'Holst, Gustav (1874-1934)']
    >>> mp3['album']
    [u'The Planets']
    >>> mp4 = open_tags('test.m4a')
    >>> mp4['artist']
    [u'Holst, Gustav (1874-1934)']
    >>> mp4['album']
    [u'The Planets']

You can also get album arts in binary::

    >>> mp3['pictures']
    ['\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x01,\x01,...']

Some tags return a single value, not a list.
You can use :meth:`~mutagenwrapper.TagsWrapper.find` to always get a single value
even for those tags that returns a list.
It will throw a :exc:`KeyError` if there is more than one value.
:meth:`~mutagenwrapper.TagsWrapper.find` returns *None* for non-existing names,
but you can set a default value::

    >>> mp4['compilation']
    False
    >>> mp4.find('compilation')
    False
    >>> mp4.find('artist')
    u'Holst, Gustav (1874-1934)'
    >>> mp4.find('date')
    >>> mp4.find('date', '1916')
    '1916'

Whenever you find the wrapper is not enough, you can access the internal
mutagen object::

    >>> mp3.raw_tags['TALB']
    TALB(encoding=3, text=[u'The Planets'])
    >>> mp4.raw_tags['\xa9alb']
    [u'The Planets']


Mappings
--------

Tag names in FLAC files are not mapped and the same name is used as the internal
name, except for ``pictures``, for which there is no corresponding Vorbis comment
(they are stored elsewhere, not as a comment).
A blank cell means there is no mapping and values may be hidden by the wrapper
(but they are still there and doesn't get lost when saving) or custom tags can
be used.

Custom tags (starting with ``TXXX:`` for ID3 and ``----:com.apple.iTunes:``
for MP4) have their name as the internal name without prefix and lowercased,
e.g. both ``TXXX:CUSTOM`` and ``----:com.apple.iTunes:CUSTOM`` are mapped to
``custom``.

In the current version, ``pictures``, ``tracknumber``, ``tracktotal``,
``discnumber``, and ``disctotal`` are read-only. You can read and write other
tags.

+----------------------+-------+------------+
| Name                 | ID3v2 | iTunes MP4 |
+======================+=======+============+
| album                | TALB  | ©alb       |
+----------------------+-------+------------+
| albumartist          | TPE2  | aART       |
+----------------------+-------+------------+
| albumartistsortorder | TSO2  | soaa       |
+----------------------+-------+------------+
| albumsortorder       | TSOA  | soal       |
+----------------------+-------+------------+
| artist               | TPE1  | ©ART       |
+----------------------+-------+------------+
| artistsortorder      | TSOP  | soar       |
+----------------------+-------+------------+
| comment              |       | ©cmt       |
+----------------------+-------+------------+
| composer             | TCOM  | ©wrt       |
+----------------------+-------+------------+
| composersortorder    | TSOC  | soco       |
+----------------------+-------+------------+
| conductor            | TPE3  |            |
+----------------------+-------+------------+
| copyright            | TCOP  | cprt       |
+----------------------+-------+------------+
| date                 | TDRC  | ©day       |
+----------------------+-------+------------+
| discnumber           | TPOS  | disk       |
+----------------------+-------+------------+
| disctotal            | TPOS  | disk       |
+----------------------+-------+------------+
| encodedby            | TENC  | ©too       |
+----------------------+-------+------------+
| genre                | TCON  | ©gen       |
+----------------------+-------+------------+
| grouping             | TIT1  | ©grp       |
+----------------------+-------+------------+
| lyrics               | TEXT  | ©lyr       |
+----------------------+-------+------------+
| pictures             | APIC: | covr       |
+----------------------+-------+------------+
| title                | TIT2  | ©nam       |
+----------------------+-------+------------+
| titlesortorder       | TSOT  | sonm       |
+----------------------+-------+------------+
| tracknumber          | TRCK  | trkn       |
+----------------------+-------+------------+
| tracktotal           | TRCK  | trkn       |
+----------------------+-------+------------+


API reference
-------------

.. automodule:: mutagenwrapper
   :members:

.. autoclass:: TagsWrapper
   :members:


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

