==============================
Statistics on the Python C API
==============================

Line numbers
============

Number of C API line numbers per Python version:

=======  ==============  ===========  ============  =======
Python   Limited API     CPython API  Internal API  Total
=======  ==============  ===========  ============  =======
2.7      12,686 (100%)   0            0             12,686
3.6      16,011 (100%)   0            0             16,011
3.7      16,517 (96%)    0            705 (4%)      17,222
3.8      13,160 (70%)    3,417 (18%)  2,230 (12%)   18,807
3.9      12,264 (62%)    4,343 (22%)  3,066 (16%)   19,673
3.10     10,395 (51%)    4,584 (22%)  5,520 (27%)   20,499
3.11     9,721 (40%)     5,241 (22%)  9,293 (38%)   24,255
=======  ==============  ===========  ============  =======

Commands:

* Limited: ``wc -l Include/*.h``
* CPython: ``wc -l Include/cpython/*.h``
* Internal: ``wc -l Include/internal/*.h``

Header file numbers
===================

Number of header file numbers per Python version:

=======  ==============  ===========  ============  ==========
Python   Limited API     CPython API  Internal API  Total
=======  ==============  ===========  ============  ==========
2.7      91              0            0             91
3.6      99 (+8)         0            0             99 (+8)
3.7      99 (same)       0            11 (+11)      110 (+11)
3.8      97 (-2)         15 (+15)     21 (+10)      133 (+23)
3.9      98 (+1)         24 (+9)      33 (+12)      155 (+22)
3.10     81 (-17)        32 (+8)      48 (+15)      161 (+6)
3.11     72 (-9)         46 (+14)     66 (+18)      184 (+23)
=======  ==============  ===========  ============  ==========

Commands:

* Limited: ``ls Include/*.h|wc -l``
* CPython: ``ls Include/cpython/*.h|wc -l``
* Internal: ``ls Include/internal/*.h|wc -l``


Symbols
=======

Symbols exported with PyAPI_FUNC() and PyAPI_DATA():

=======  ============  ===========  ==========  ===========
Python   Public        Private      Internal    Total
=======  ============  ===========  ==========  ===========
2.7      891           207          0           1098
3.6      1041 (+150)   419 (+212)   0           1460 (+362)
3.7      1068 (+27)    479 (+60)    22          1569 (+109)
3.8      1105 (+37)    456 (-23)    91 (+69)    1652 (+83)
3.9      1115 (+10)    439 (-17)    124 (+33)   1678 (+26)
3.10     1080 (-35)    439 (same)   129 (+5)    1648 (-30)
3.11     1086 (+6)     381 (-58)    187 (+58)   1654 (+6)
=======  ============  ===========  ==========  ===========

Command (total)::

    grep -E 'PyAPI_(FUNC|DATA)' Include/*.h Include/cpython/*.h Include/internal/*.h|wc -l

Command (public)::

    grep -E 'PyAPI_(FUNC|DATA)' Include/*.h Include/cpython/*.h|grep -v ' _Py'|wc -l

Command (public + private)::

    grep -E 'PyAPI_(FUNC|DATA)' Include/*.h Include/cpython/*.h|wc -l

Command (internal)::

    grep -E 'PyAPI_(FUNC|DATA)' Include/internal/*.h|wc -l

Since Python 3.9, Python is now built with ``-fvisibility=hidden`` to avoid
exporting symbols which are not **explicitly** exported.

The ``make smelly`` command checks for public symbols of libpython and C
extension which are prefixed by ``Py`` or ``_Py``. See
the ``Tools/scripts/smelly.py`` script.

Functions defined as macros and static inline functions
=======================================================

Functions defined as macros (only public) and static inline functions (public
or private):

======  =====  =============  =====
Python  Macro  Static inline  Total
======  =====  =============  =====
2.7     396    0              396
3.6     394    0              394
3.7     403    0              403
3.8     399    14             413
3.9     406    30             436
3.10    412    36             448
3.11    399    54             453
======  =====  =============  =====

If a function is defined as a private static inline function and exposed as a
public macro, it is counted twice in this table. For example, the public
Py_INCREF() macro and the private _Py_INCREF() static inline functions are
counted as 2 functions, whereas only the "Py_INCREF" name is public.

Commands::

    grep -E 'define P[Yy][A-Za-z_]+ *\(' Include/*.h Include/cpython/*.h|wc -l
    grep 'static inline ' Include/*.h Include/cpython/*.h|grep -v pydtrace|grep -v 'define Py_LOCAL_INLINE'|wc -l


Structures
==========

Public structures in the Python C API:

======  ==========
Python  Structures
======  ==========
2.7     97
3.6     124 (+27)
3.7     137 (+13)
3.8     127 (-10)
3.9     125 (-2)
3.10    104 (-21)
3.11    106 (+2)
======  ==========

These numbers exclude opaque structures like PyInterpreterState (since Python
3.8). The grep command is not exact. For example, PyODictObject is seen as
public, whereas the structure is opaque::

    typedef struct _odictobject PyODictObject;

The _odictobject structure is only defined in Objects/odictobject.c.

Command::

    grep 'typedef struct' Include/*.h Include/cpython/*.h|wc -l
