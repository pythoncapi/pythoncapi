.. _remove-funcs:

++++++++++++++++++++++++++++++++++++++
Remove functions from the Python C API
++++++++++++++++++++++++++++++++++++++

The Python C API is just too big. For performance reasons, CPython calls
internally directly the implementation of a function instead of using the
abstract API. For example, ``PyDict_GetItem()`` is preferred over
``PyObject_GetItem()``. Inside, CPython, such optimization is fine. But
exposing so many functions is an issue: CPython has to keep backward
compatibility, PyPy has to implement all these functions, etc. Third party
C extensions should call abstract functions like ``PyObject_GetItem()``.

Good: abstract functions
========================

Examples:

* ``PyObject_GetItem()``, ``PySequence_GetItem()``

Bad? implementations
====================

Examples:

* ``PyObject_GetItem()``, ``PySequence_GetItem()``:

  * ``PyList_GetItem()``
  * ``PyTuple_GetItem()``
  * ``PyDict_GetItem()``
