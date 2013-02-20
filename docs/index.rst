.. mutagenwrapper documentation master file, created by
   sphinx-quickstart on Thu Jan 31 11:29:44 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to mutagenwrapper's documentation!
==========================================

mutagenwrapper is a wrapper for mutagen_ that uses consistent and human-readable
tag keys among various tagging formats.

Note that this module is still in development. Many features are not supported
like writing an album art. See `Mappings`_ for more details. There may be
undocumented limitations too.

You must backup your files if you are going to edit tags in files with this
module. Data loss does occur, and there is no way to recover files without a
backup.

mutagenwrapper can read tags with multiple values (e.g. multiple artists),
but due to the incompatibility of mutagen and foobar2000_, the way it saves
tags to files makes those tags unreadable by foobar2000 in some cases,
especially for MP4 files. It could lead to data loss if you edit tags in such
files and save the changes in foobar2000.

.. _mutagen: http://code.google.com/p/mutagen/
.. _foobar2000: http://www.foobar2000.org/


Examples
--------

You can access tags via human-readable names. For the mappings, see `Mappings`_::

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

If you want get album arts, you cat get binary data::

    >>> mp3['pictures']
    ['\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x01,\x01,...']

Some tags return a single value, not a list.
You can use :meth:`~mutagenwrapper.TagsWrapper.find` to always get a single value.
It will throw a :exc:`KeyError` if there is more than one value.
:meth:`~mutagenwrapper.TagsWrapper.find` returns *None* for non-existing keys,
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

Access the internal mutagen object::

    >>> mp3.raw_tags['TALB']
    TALB(encoding=3, text=[u'The Planets'])
    >>> mp4.raw_tags['\xa9alb']
    [u'The Planets']


Mappings
--------

Tag keys in FLAC files are not mapped and the same key is used as the name,
except for *pictures*. A blank cell means there is no mapping and values
may be hidden by the wrapper (but they are not lost when saving) or custom
tags can be used.

Custom tags (starting with ``TXXX:`` for ID3 and ``----:com.apple.iTunes:``
for MP4) have their name as the key without prefix and lowercased, e.g.
both ``TXXX:CUSTOM`` and ``----:com.apple.iTunes:CUSTOM`` are mapped to
*custom*.

Currently you cannot change values for pictures, tracknumber, tracktotal,
discnumber, and disctotal.

+-----------------+-------+------------+
| Name            | ID3v2 | iTunes MP4 |
+=================+=======+============+
| album           | TALB  | ©alb       |
+-----------------+-------+------------+
| albumartist     | TPE2  | aART       |
+-----------------+-------+------------+
| albumartistsort | TSO2  | soaa       |
+-----------------+-------+------------+
| albumsort       | TSOA  | soal       |
+-----------------+-------+------------+
| artist          | TPE1  | ©ART       |
+-----------------+-------+------------+
| artistsort      | TSOP  | soar       |
+-----------------+-------+------------+
| comment         |       | ©cmt       |
+-----------------+-------+------------+
| composer        | TCOM  | ©wrt       |
+-----------------+-------+------------+
| composersort    | TSOC  | soco       |
+-----------------+-------+------------+
| conductor       | TPE3  |            |
+-----------------+-------+------------+
| copyright       | TCOP  | cprt       |
+-----------------+-------+------------+
| date            | TDRC  | ©day       |
+-----------------+-------+------------+
| discnumber      | TPOS  | disk       |
+-----------------+-------+------------+
| disctotal       | TPOS  | disk       |
+-----------------+-------+------------+
| encodedby       | TENC  | ©too       |
+-----------------+-------+------------+
| genre           | TCON  | ©gen       |
+-----------------+-------+------------+
| grouping        | TIT1  | ©grp       |
+-----------------+-------+------------+
| pictures        | APIC: | covr       |
+-----------------+-------+------------+
| title           | TIT2  | ©nam       |
+-----------------+-------+------------+
| titlesort       | TSOT  | sonm       |
+-----------------+-------+------------+
| tracknumber     | TRCK  | trkn       |
+-----------------+-------+------------+
| tracktotal      | TRCK  | trkn       |
+-----------------+-------+------------+


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

