++++++++++++++++++++++++++++++++++++++++++
Design a new stable API and ABI for Python
++++++++++++++++++++++++++++++++++++++++++

Bad title: "new API".

Good title: "make the stable API usable".

Brainstorm to change the Python C API (to make it better):

* `Python C API <https://pythoncapi.readthedocs.io/>`_ (this documentation)
* `pythoncapi GitHub project <https://github.com/vstinner/pythoncapi/>`_
  (this documentation can be found in the ``doc/`` subdirectory).
* `capi-sig mailing list
  <https://mail.python.org/mm3/mailman3/lists/capi-sig.python.org/>`_

Pages
=====

.. toctree::
   :maxdepth: 2

   pep

Status
======

* 2018-07-29: `pythoncapi project <https://github.com/vstinner/pythoncapi>`_
  created on GitHub
* 2017-12-21: It's an idea. There is an old PEP draft, but no implementation,
  the PEP has no number and was not accepted yet (nor really proposed).


Players
=======

* CPython: Victor Stinner
* Cython: Stefan Behnel
* PyPy: Ronan Lamy

Unknown status:

* MicroPython?
* IronPython?
* Jython?
* Pyjion
* Pyston
* any other?

Timeline
========

* 2018-06: capi-sig mailing list migrated to Mailman 3
* 2017-11: Idea proposed on python-dev, `[Python-Dev] Make the stable API-ABI
  usable
  <https://mail.python.org/pipermail/python-dev/2017-November/150607.html>`_
* 2017-09: Blog post: `A New C API for CPython
  <https://vstinner.github.io/new-python-c-api.html>`_
* 2017-09: Idea discussed at the CPython sprint at Instagram (California).
  Liked by all core developers. The expected performance slowdown is likely to
  be accepted.
* 2017-07: Idea proposed on python-ideas. `[Python-ideas] PEP: Hide
  implementation details in the C API
  <https://mail.python.org/pipermail/python-ideas/2017-July/046399.html>`_
* 2017-05: Idea proposed at the Python Language Summit, during Pycon US 2017.
  My `"Python performance" slides (PDF)
  <https://github.com/vstinner/conf/raw/master/2017-PyconUS/summit.pdf>`_.
  LWN article: `Keeping Python competitive
  <https://lwn.net/Articles/723752/#723949>`_.



Problem
=======

The current Python C API produces an ABI which is far from stable. The API
leaks many implementation details into the ABI.

For example, using the ``PyTuple_GET_ITEM()`` macro produces machine code which
uses an **hardcoded** offset. If the PyObject structure changes, the offset
changes, and so the **ABI** changes.

Longer explanation: `A New C API for CPython
<https://vstinner.github.io/new-python-c-api.html>`_.


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

It becomes possible to design new flavors of CPython with radical changes:

* **Change the garbage collector.** CPython not using reference counting
  internally, but likely still use reference counting in the C API. Maybe use a
  tracing garbage collector.  It's hard to estimate how many lines of code
  would have to be modified to use a different garbage collector. The external
  C API compatibility must not be broken.
* **Remove the GIL.** CPython without a global interpreter lock, but smaller
  locks on objects, as Jython does. -- Gilectomy is an example of such CPython
  fork
* **Tagged pointer.** Common optimization technic to reduce the boxing/unboxing
  cost and reduce the memory consumption. Currently, it's not possible to
  implement such optimization.
* **Copy-on-Write (CoW).** Instagram is using prefork with Django but has
  memory usage issues caused by reference counting. Accessing a Python object
  modifies its reference counter and so copies the page which was created a COW
  in the forked child process. Python 3.7 added `gc.freeze()
  <https://docs.python.org/dev/library/gc.html#gc.freeze>`_ workaround.
* Insert your new cool idea here!


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

First, what is the C API?

* Python objects

  * Protocol, Abstract
  * Types, Classes

* Memory Allocators
* Python initialization and configuration
* Control flow

  * Generator
  * Exception

Bad design for the C API:

* ``PyObject**`` must not be exposed. ``PyObject** PySequence_Fast_ITEMS(ob)``
  has to go.
* Borrowed references: Too many functions :-( My attempt to list them:

  * ``PyCell_GET()``
  * ``PyDict_GetItem()``
  * ``PyDict_GetItemWithError()``
  * ``PyDict_GetItemString()``
  * ``PyDict_SetDefault()``
  * ``PyErr_Occurred()``
  * ``PyEval_GetBuiltins()``
  * ``PyEval_GetLocals()``
  * ``PyEval_GetGlobals()``
  * ``PyEval_GetFrame()``
  * ``PyFunction_GetClosure()``
  * ``Py_InitModule()``
  * ``PyImport_GetModuleDict()``
  * ``PyList_GET_ITEM()``
  * ``PyList_GetItem()``
  * ``PyMethod_GET_SELF()``
  * ``PySequence_Fast_GET_ITEM()``
  * ``PySys_GetObject()``
  * ``PyThreadState_GetDict()``
  * ``PyTuple_GET_ITEM()``
  * ``PyTuple_GetItem()``
  * ``PyWeakref_GetObject()``

* Don't leak the structures like ``PyObject`` or ``PyTupleObject`` to not
  access directly fields, to not use fixed offset at the ABI level. Replace
  macros with functions calls. PyPy already this in its C API (``cpyext``).

XXX weird PyObject_CallFunction() API: https://bugs.python.org/issue28977
XXX Fix the API or document it?

XXX should we do something for reference counting, Py_INCREF and Py_DECREF?

PyPy requests:

* Deprecate finalizer API.
* Deprecate Unicode API introduced by the PEP 393, compact strings.


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


Check for ABI changes
=====================

* https://abi-laboratory.pro/tracker/timeline/python/
* https://bugs.python.org/issue21142
* https://sourceware.org/libabigail/
