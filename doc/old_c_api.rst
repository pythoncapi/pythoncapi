.. _old-c-api:

+++++++++
Old C API
+++++++++

The "Old C API" is the Python 3.7 API which "leaks" implementation details like
``PyObject.ob_refcnt`` through :ref:`Py_INCREF() <incref>`. This API will
remain available for CPython internals but also for specific use cases like
Cython (for best performances) and :ref:`debugging tools <debug-tools>`.

See also :ref:`Calling conventensions <calling-conventions>`.

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
* PyPy:
  `pypy/module/cpyext/
  <https://bitbucket.org/pypy/pypy/src/default/pypy/module/cpyext/>`_
  (`cpyext/stubs.py
  <https://bitbucket.org/pypy/pypy/src/default/pypy/module/cpyext/stubs.py>`_)
