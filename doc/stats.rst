++++++++++++++++++++++++++++++
Statistics on the Python C API
++++++++++++++++++++++++++++++

Line Numbers
============

Number of C API line numbers per Python version:

======  =============  ===========  ============  ======
Python  Limited API    CPython API  Internal API  Total
======  =============  ===========  ============  ======
2.7     12,686 (100%)  0 (0%)       0 (0%)        12,686
3.6     15,984 (100%)  0 (0%)       0 (0%)        15,984
3.7     16,517 (96%)   0 (0%)       717 (4%)      17,234
3.8     13,166 (70%)   3,417 (18%)  2,242 (12%)   18,825
3.9     12,265 (62%)   4,358 (22%)  3,093 (16%)   19,716
3.10    10,396 (51%)   4,613 (22%)  5,533 (27%)   20,542
3.11    9,255 (37%)    5,387 (22%)  10,107 (41%)  24,749
3.12    9,189 (37%)    5,246 (21%)  10,176 (41%)  24,611
======  =============  ===========  ============  ======

File Numbers
============

Number of header file numbers per Python version:

======  ===========  ===========  ============  =========
Python  Limited API  CPython API  Internal API  Total
======  ===========  ===========  ============  =========
2.7     91           0            0             91
3.6     99 (+8)      0 (same)     0 (same)      99 (+8)
3.7     99 (same)    0 (same)     11 (+11)      110 (+11)
3.8     97 (-2)      15 (+15)     21 (+10)      133 (+23)
3.9     98 (+1)      24 (+9)      33 (+12)      155 (+22)
3.10    81 (-17)     32 (+8)      48 (+15)      161 (+6)
3.11    72 (-9)      46 (+14)     68 (+20)      186 (+25)
3.12    72 (same)    46 (same)    69 (+1)       187 (+1)
======  ===========  ===========  ============  =========

Symbols
=======

Symbols exported with PyAPI_FUNC() and PyAPI_DATA():

======  ============  ==========  =========  ============
Python  Public        Private     Internal   Total
======  ============  ==========  =========  ============
2.7     891           207         0          1,098
3.6     1,041 (+150)  419 (+212)  0 (same)   1,460 (+362)
3.7     1,068 (+27)   479 (+60)   22 (+22)   1,569 (+109)
3.8     1,105 (+37)   456 (-23)   91 (+69)   1,652 (+83)
3.9     1,115 (+10)   439 (-17)   124 (+33)  1,678 (+26)
3.10    1,080 (-35)   439 (same)  129 (+5)   1,648 (-30)
3.11    1,087 (+7)    381 (-58)   188 (+59)  1,656 (+8)
3.12    1,081 (-6)    378 (-3)    192 (+4)   1,651 (-5)
======  ============  ==========  =========  ============

Since Python 3.9, Python is now built with ``-fvisibility=hidden`` to avoid
exporting symbols which are not **explicitly** exported.

The ``make smelly`` command checks for public symbols of libpython and C
extension which are prefixed by ``Py`` or ``_Py``. See
the ``Tools/scripts/smelly.py`` script.

Functions defined as macros and static inline functions
=======================================================

Functions defined as macros (only public) and static inline functions (public or private):

======  =========  =============  =========
Python  Macro      Static inline  Total
======  =========  =============  =========
2.7     396        0              396
3.6     394 (-2)   0 (same)       394 (-2)
3.7     403 (+9)   0 (same)       403 (+9)
3.8     399 (-4)   14 (+14)       413 (+10)
3.9     406 (+7)   30 (+16)       436 (+23)
3.10    412 (+6)   36 (+6)        448 (+12)
3.11    400 (-12)  66 (+30)       466 (+18)
3.12    385 (-15)  75 (+9)        460 (-6)
======  =========  =============  =========

If a function is defined as a private static inline function and exposed as a
public macro, it is counted twice in this table. For example, the public
Py_INCREF() macro and the private _Py_INCREF() static inline functions are
counted as 2 functions, whereas only the "Py_INCREF" name is public.

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
3.12    111 (+5)
======  ==========

These numbers exclude opaque structures like PyInterpreterState (since Python
3.8). The grep command is not exact. For example, PyODictObject is seen as
public, whereas the structure is opaque::

    typedef struct _odictobject PyODictObject;

The _odictobject structure is only defined in Objects/odictobject.c.

