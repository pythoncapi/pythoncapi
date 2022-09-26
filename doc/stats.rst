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
3.6     16,051 (100%)  0 (0%)       0 (0%)        16,051
3.7     16,517 (96%)   0 (0%)       772 (4%)      17,289
3.8     13,166 (70%)   3,417 (18%)  2,295 (12%)   18,878
3.9     12,265 (62%)   4,358 (22%)  3,146 (16%)   19,769
3.10    10,396 (51%)   4,616 (22%)  5,572 (27%)   20,584
3.11    9,232 (37%)    5,495 (22%)  10,046 (41%)  24,773
3.12    9,227 (29%)    5,308 (17%)  17,633 (55%)  32,168
======  =============  ===========  ============  ======

File Numbers
============

Number of header file numbers per Python version:

======  ===========  ===========  ============  =========
Python  Limited API  CPython API  Internal API  Total
======  ===========  ===========  ============  =========
2.7     91           0            0             91
3.6     99 (+8)      0 (same)     0 (same)      99 (+8)
3.7     99 (same)    0 (same)     12 (+12)      111 (+12)
3.8     97 (-2)      15 (+15)     22 (+10)      134 (+23)
3.9     98 (+1)      24 (+9)      34 (+12)      156 (+22)
3.10    81 (-17)     32 (+8)      48 (+14)      161 (+5)
3.11    72 (-9)      48 (+16)     68 (+20)      188 (+27)
3.12    72 (same)    48 (same)    71 (+3)       191 (+3)
======  ===========  ===========  ============  =========

Symbols
=======

Symbols exported with PyAPI_FUNC() and PyAPI_DATA():

======  ============  ==========  =========  ============
Python  Public        Private     Internal   Total
======  ============  ==========  =========  ============
2.7     891           207         0          1,098
3.6     1,041 (+150)  420 (+213)  0 (same)   1,461 (+363)
3.7     1,068 (+27)   479 (+59)   22 (+22)   1,569 (+108)
3.8     1,105 (+37)   456 (-23)   91 (+69)   1,652 (+83)
3.9     1,115 (+10)   439 (-17)   124 (+33)  1,678 (+26)
3.10    1,080 (-35)   441 (+2)    129 (+5)   1,650 (-28)
3.11    1,113 (+33)   383 (-58)   187 (+58)  1,683 (+33)
3.12    1,116 (+3)    382 (-1)    186 (-1)   1,684 (+1)
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
3.12    390 (-10)  77 (+11)       467 (+1)
======  =========  =============  =========

If a function is defined as a private static inline function and exposed as a
public macro, it is counted twice in this table. For example, the public
Py_INCREF() macro and the private _Py_INCREF() static inline functions are
counted as 2 functions, whereas only the "Py_INCREF" name is public.

Structures
==========

Structures in the Python C API:

======  ===========  ===========  ============  =========
Python  Limited API  CPython API  Internal API  Total
======  ===========  ===========  ============  =========
2.7     92           0            0             92
3.6     110 (+18)    0 (same)     0 (same)      110 (+18)
3.7     114 (+4)     0 (same)     18 (+18)      132 (+22)
3.8     81 (-33)     34 (+34)     28 (+10)      143 (+11)
3.9     68 (-13)     46 (+12)     38 (+10)      152 (+9)
3.10    41 (-27)     53 (+7)      91 (+53)      185 (+33)
3.11    19 (-22)     75 (+22)     112 (+21)     206 (+21)
3.12    24 (+5)      75 (same)    113 (+1)      212 (+6)
======  ===========  ===========  ============  =========

These numbers exclude opaque structures like PyInterpreterState (since Python
3.8). The grep command is not exact. For example, PyODictObject is seen as
public, whereas the structure is opaque::

    typedef struct _odictobject PyODictObject;

The _odictobject structure is only defined in Objects/odictobject.c.

