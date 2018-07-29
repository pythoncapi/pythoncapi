.. _pep:

++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Hide implementation details of the C API (old draft PEP)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This page is a old draft for a PEP, written at 31-May-2017; no update since May
2017.

PEP headers::

    PEP: xxx
    Title: Hide implementation details of the C API
    Version: $Revision$
    Last-Modified: $Date$
    Author: Victor Stinner <victor.stinner@gmail.com>,
    Status: Draft
    Type: Standards Track
    Content-Type: text/x-rst
    Created: 31-May-2017

Abstract
========

Modify the C API to remove implementation details. Add an opt-in option
to compile C extensions to get the old full API with implementation
details.

The modified C API allows to more easily experiment new optimizations:

* Indirect Reference Counting
* Remove Reference Counting, New Garbage Collector
* Remove the GIL
* Tagged pointers

Reference counting may be emulated in a future implementation for
backward compatibility.


Rationale
=========

History of CPython forks
------------------------

Last 10 years, CPython was forked multiple times to attempt
different CPython enhancements:

* Unladen Swallow: add a JIT compiler based on LLVM
* Pyston: add a JIT compiler based on LLVM (CPython 2.7 fork)
* Pyjion: add a JIT compiler based on Microsoft CLR
* Gilectomy: remove the Global Interpreter Lock nicknamed "GIL"
* etc.

Sadly, none is this project has been merged back into CPython. Unladen
Swallow lost its funding from Google, Pyston lost its funding from
Dropbox, Pyjion is developed in the limited spare time of two Microsoft
employees.

One hard technically issue which blocked these projects to really
unleash their power is the C API of CPython. Many old technical choices
of CPython are hardcoded in this API:

* reference counting
* garbage collector
* C structures like PyObject which contains headers for reference
  counting and the garbage collector
* specific memory allocators
* etc.

PyPy
----

PyPy uses more efficient structures and uses a more efficient garbage
collector without reference counting. Thanks to that (but also many
other optimizations), PyPy succeeded to run Python code up to 5x faster
than CPython.


Plan made of multiple small steps
=================================

Step 1: split Include/ into subdirectories
------------------------------------------

Split the ``Include/`` directory of CPython:

* ``python`` API: ``Include/Python.h`` remains the default C API
* ``core`` API: ``Include/core/Python.h`` is a new C API designed for
  building Python
* ``stable`` API: ``Include/stable/Python.h`` is the stable ABI

Expect declarations to be duplicated on purpose: ``#include`` should be
not used to include files from a different API to prevent mistakes. In
the past, too many functions were exposed *by mistake*, especially
symbols exported to the stable ABI by mistake.

At this point, ``Include/Python.h`` is not changed at all: zero risk of
backward incompatibility.

The ``core`` API is the most complete API exposing *all* implementation
details and use macros for best performances.

XXX should we abandon the stable ABI? Never really used by anyone.


Step 2: Add an opt-in API option to tools building packages
-----------------------------------------------------------

Modify Python packaging tools (distutils, setuptools, flit, pip, etc.)
to add an opt-in option to choose the API: ``python``, ``core`` or
``stable``.

For example, debuggers like ``vmprof`` need need the ``core`` API to get
a full access to implementation details.

XXX handle backward compatibility for packaging tools.

Step 3: first pass of implementation detail removal
---------------------------------------------------

Modify the ``python`` API:

* Add a new ``API`` subdirectory in the Python source code which will
  "implement" the Python C API
* Replace macros with functions. The implementation of new functions
  will be written in the ``API/`` directory. For example, Py_INCREF()
  becomes the function ``void Py_INCREF(PyObject *op)`` and its
  implementation will be written in the ``API`` directory.
* Slowly remove more and more implementation details from this API.

Modifications of these API should be driven by tests of popular third
party packages like:

* Django with database drivers
* numpy
* scipy
* Pillow
* lxml
* etc.

Compilation errors on these extensions are expected. This step should
help to draw a line for the backward incompatible change.

Goal: remove a few implementation details but don't break numpy and
lxml.

Step 4
------

Switch the default API to the new restricted ``python`` API.

Help third party projects to patch their code: don't break the "Python
world".

Step 5
------

Continue Step 3: remove even more implementation details.

Long-term goal to complete this PEP: Remove *all* implementation
details, remove all structures and macros.


Alternative: keep core as the default API
=========================================

A smoother transition would be to not touch the existing API but work on
a new API which would only be used as an opt-in option.

Similar plan used by Gilectomy: opt-in option to get best performances.

It would be at least two Python binaries per Python version: default
compatible version, and a new faster but incompatible version.


Idea: implementation of the C API supporting old Python versions?
=================================================================

Open questions.

Q: Would it be possible to design an external library which would work
on Python 2.7, Python 3.4-3.6, and the future Python 3.7?

Q: Should such library be linked to libpythonX.Y? Or even to a pythonX.Y
binary which wasn't built with shared library?

Q: Would it be easy to use it? How would it be downloaded and installed
to build extensions?


Collaboration with PyPy, IronPython, Jython and MicroPython
===========================================================

XXX to be done


Enhancements becoming possible thanks to a new C API
====================================================

Indirect Reference Counting
---------------------------

* Replace ``Py_ssize_t ob_refcnt;`` (integer)
  with ``Py_ssize_t *ob_refcnt;`` (pointer to an integer).
* Same change for GC headers?
* Store all reference counters in a separated memory block
  (or maybe multiple memory blocks)

Expected advantage: smaller memory footprint when using fork() on UNIX
which is implemented with Copy-On-Write on physical memory pages.

See also `Dismissing Python Garbage Collection at Instagram
<https://engineering.instagram.com/dismissing-python-garbage-collection-at-instagram-4dca40b29172>`_.


Remove Reference Counting, New Garbage Collector
------------------------------------------------

If the new C API hides well all implementation details, it becomes
possible to change fundamental features like how CPython tracks the
lifetime of an object.

* Remove ``Py_ssize_t ob_refcnt;`` from the PyObject structure
* Replace the current XXX garbage collector with a new tracing garbage
  collector
* Use new macros to define a variable storing an object and to set the
  value of an object
* Reimplement Py_INCREF() and Py_DECREF() on top of that using a hash
  table: object => reference counter.

XXX PyPy is only partially successful on that project, cpyext remains
very slow.

XXX Would it require an opt-in option to really limit backward
compatibility?


Remove the GIL
--------------

* Don't remove the GIL, but replace the GIL with smaller locks
* Builtin mutable types: list, set, dict
* Modules
* Classes
* etc.

Backward compatibility:

* Keep the GIL


Tagged pointers
---------------

https://en.wikipedia.org/wiki/Tagged_pointer

Common optimization, especially used for "small integers".

Current C API doesn't allow to implement tagged pointers.

Tagged pointers are used in MicroPython to reduce the memory footprint.

Note: ARM64 was recently extended its address space to 48 bits, causing
issue in LuaJIT: `47 bit address space restriction on ARM64
<https://github.com/LuaJIT/LuaJIT/issues/49>`_.

Misc ideas
----------

* Software Transactional Memory?
  See `PyPy STM <http://doc.pypy.org/en/latest/stm.html>`_


Idea: Multiple Python binaries
==============================

Instead of a single ``python3.7``, providing two or more binaries, as
PyPy does, would allow to experiment more easily changes without
breaking the backward compatibility.

For example, ``python3.7`` would remain the default binary with
reference counting and the current garbage collector, whereas
``fastpython3.7`` would not use reference counting and a new garbage
collector.

It would allow to more quickly "break the backward compatibility" and
make it even more explicit than only prepared C extensions will be
compatible with the new ``fastpython3.7``.


cffi
====

XXX

Long term goal: "more cffi, less libpython".


Copyright
=========

This document has been placed in the public domain.



..
   Local Variables:
   mode: indented-text
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 70
   coding: utf-8
   End:
