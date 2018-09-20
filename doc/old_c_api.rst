.. _old-c-api:

+++++++++
Old C API
+++++++++

The "current" or "old" C API is the Python 3.7 API which "leaks" implementation
details like ``PyObject.ob_refcnt`` through :ref:`Py_INCREF() <incref>` macro.

With the new C API, the old C API will remain available thanks to the
:ref:`regular runtime <regular-runtime>`, for CPython internals, for specific
use cases like :ref:`Cython <cython>` (for best performances) and
:ref:`debugging tools <debug-tools>`, but also for the long tail of C
extensions on PyPI.

See also :ref:`Calling conventions <calling-conventions>`.

What is the Python C API?
=========================

* Python objects

  * Protocol, Abstract
  * Types, Classes

* Memory Allocators
* Python initialization and configuration
* Control flow

  * Generator
  * Exception: ``PyErr_SetString()``, ``PyErr_Clear()``

Current Python C API
====================

* CPython:
  `headers of the Include/ directory
  <https://github.com/python/cpython/tree/master/Include>`_
* PyPy :ref:`cpyext <cpyext>`:
  `pypy/module/cpyext/
  <https://bitbucket.org/pypy/pypy/src/default/pypy/module/cpyext/>`_
  (`cpyext/stubs.py
  <https://bitbucket.org/pypy/pypy/src/default/pypy/module/cpyext/stubs.py>`_)
