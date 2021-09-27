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

=======  ==============  ===============  ===========
Python   Public          Private          Total
=======  ==============  ===============  ===========
2.7      891             207              1098
3.6      1041 (+150)     419 (+212)       1460 (+362)
3.7      1068 (+27)      479 (+60)        1547 (+87)
3.8      1105 (+37)      456 (-23)        1561 (+14)
3.9      1115 (+10)      437 (-19)        1552 (-9)
3.10     1080 (-35)      435 (-2)         1515 (-37)
3.11     1062 (-18)      437 (+2)         1499 (-16)
=======  ==============  ===============  ===========

Command (total)::

    grep -E 'PyAPI_(FUNC|DATA)' Include/*.h Include/cpython/*.h|wc -l

Command (private)::

    grep -E 'PyAPI_(FUNC|DATA)' Include/*.h Include/cpython/*.h|grep ' _Py'|wc -l

Since Python 3.9, Python is now built with ``-fvisibility=hidden`` to avoid
exporting symbols which are not **explicitly** exported.

The ``make smelly`` command checks for public symbols of libpython and C
extension which are prefixed by ``Py`` or ``_Py``. See
``Tools/scripts/smelly.py`` script.

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
3.11    412    40             452
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
3.11    104 (same)
======  ==========

These numbers exclude opaque structures like PyInterpreterState (since Python
3.8).

Command::

    grep 'typedef struct' Include/*.h Include/cpython/*.h|wc -l
