==============================
Statistics on the Python C API
==============================

Line numbers
============

Number of C API line numbers per Python version:

=======  =============  ===========  ============  =======
Python   Public         CPython      Internal      Total
=======  =============  ===========  ============  =======
2.7      12686 (100%)   0            0             12686
3.6      16011 (100%)   0            0             16011
3.7      16517 (96%)    0            705 (4%)      17222
3.8      13160 (70%)    3417 (18%)   2230 (12%)    18807
3.9      12264 (62%)    4343 (22%)   3066 (16%)    19673
3.10     10305 (52%)    4513 (23%)   5092 (26%)    19910
=======  =============  ===========  ============  =======

Comands:

* public: ``wc -l Include/*.h``
* cpython: ``wc -l Include/cpython/*.h``
* internal: ``wc -l Include/internal/*.h``

Symbols
=======

Symbols exported with PyAPI_FUNC() and PyAPI_DATA():

=======  ===========
Python   Symbols
=======  ===========
2.7      1098
3.6      1460
3.7      1547 (+87)
3.8      1561 (+14)
3.9      1552 (-9)
3.10     1495 (-57)
=======  ===========

Command::

    grep -E 'PyAPI_(FUNC|DATA)' Include/*.h Include/cpython/*.h|wc -l

Since Python 3.9, Python is now built with ``-fvisibility=hidden`` to avoid
exporting symbols which are not **explicitly** exported.

The ``make smelly`` command checks for public symbols of libpython and C
extension which are prefixed by ``Py`` or ``_Py``. See
``Tools/scripts/smelly.py`` script.
