++++++++++++++++++++++++++++++++++++
Rationale to change the Python C API
++++++++++++++++++++++++++++++++++++

Problem
=======

The current Python C API produces an ABI which is far from stable. The API
leaks many implementation details into the ABI.

For example, using the ``PyTuple_GET_ITEM()`` macro produces machine code which
uses an **hardcoded** offset. If the PyObject structure changes, the offset
changes, and so the **ABI** changes.

The Big Carrot
==============

Changing the C API means that authors of C extensions have to do something. To
justify these changes, we need a big carrot. Examples:

* faster Python if you pick new API? faster PyPy cpyext?
* less bugs? no more surprising borrow references causing "funny" crashes
* new features?

Performance problem: How can we make Python 2x faster?
======================================================

"Leaking" implementation details into the ABI prevents many optimizations
opportunities. IHMO it was the **root cause** of failures of previous large
optimization projects like *Unladen Swallow* and *Pyston*.


Issues with an unstable ABI
===========================

* **Packaging.** Developers have to publish one binary package per Python
  version (3.6, 3.7, 3.8, etc.). Upgrading Python 3 to a newer version
  is very hard because of this issue: each binary package must be
  distributed in many versions, one per Python version. A stable ABI
  would allow to build a package for Python 3.6 and use the same binary
  for Python 3.7, 3.8, 3.9, etc.
* **Experiment issue.** It is not possible to change the base Python structures
  like PyObject or PyTupleObject to reduce the memory footprint or implement
  new optimizations. Experiment such changes requires to rebuild C extensions.
* **Debug builds.** Most Linux distributions provide a debug build of Python
  (``python3-dbg``), but such build has a different ABI and so all C extensions
  must be recompiled to be usable on such flavor of Python. Being able to use
  debug builds would ease debugging since the debug builds add many debug
  checks which are too expensive (CPU/memory) to be enabled by default in a
  release build.


Advantages of a stable ABI
==========================

See :ref:`Optimization ideas <optim-ideas>`.



The C API is too big
====================

**Goal:** Smaller C API.

Common complain from PyPy developers. Writing a new Python implementation with
implements the full C API is a huge work.

Slowly **remove** functions from the future stable ABI? It should be done
gradually and update most famous Python C extensions in parrallel to not "break
Python".

Some C functions can easily be replaced by a function call, these functions are
mostly written for **internal** usage, to make the CPython code base simpler.
But they should not be exposed (they should be private).


The C API must not leak implementation details anymore
======================================================

**Goal:** Hide implementation details.

See :ref:`Bad C API <bad-api>`.


Performance slowdown
====================

Hiding implementation details is likely to make tiny loops slower, since it
adds function calls instead of directly accessing the memory.

The performance slowdown is expected to be negligible, but has to be measured
once a concrete implmenetation will be written.


Alternative: Stop using the C API, use cffi
===========================================

**Goal:** Remove the public C API. Or at least, stop using it.

Practical issue: ``cffi`` is not part of Python 3.7 standard library yet.
Previous attempt to add it, in 2013: `[Python-Dev] cffi in stdlib
<https://mail.python.org/pipermail/python-dev/2013-February/124337.html>`_.

Questions:

* How many popular Python modules use the C API?
* How long would it take to rewrite a big famous Python module with ``cffi``?
* What is the long-term transition plan to reach the "no C API" goal?


Fix Python headers
==================

**Goal**: Make private APIs private again: Py_BUILD_CORE vs Py_LIMITED_API.

Currently, the stable API (Py_LIMITED_API), the private functions (``_Py``
prefix), functions that must only be used in CPython core (``Py_BUILD_CORE``)
and other functions (regular C API) are all defined in the same file. It is
easy to add a function to the wrong API by mistake.


No public C functions if it can't be done in Python
===================================================

**Goal**: Remove public functions which do things which are not doable in pure
Python.

There shouldn't be C APIs that do something that you can't do in Python.

Example: the C buffer protocol, the Python ``memoryview`` type only expose a
subset of ``buffer`` features.


For internal use only
=====================

The C API documentation contains a few functions with the note "For internal
use only". Examples:

* _PyImport_Init()
* PyImport_Cleanup()
* _PyImport_Fini()

Why PyImport_Cleanup() is still a public method?
