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

See :ref:`Bad C API <bad-c-api>`.

Functions and macros removed from the new CAPI
==============================================

Removed functions and macros which use :ref:`borrowed references
<borrowed-ref>`:

* ``Py_TYPE()``
* ``PyTuple_GET_ITEM()``
* ``PyTuple_GetItem()``
* ``PyTuple_SetItem()``
* ``PyTuple_SET_ITEM()``

Only keep abstract functions?
=============================

Good: abstract functions. Examples:

* ``PyObject_GetItem()``, ``PySequence_GetItem()``

Bad? implementations for concrete types. Examples:

* ``PyObject_GetItem()``, ``PySequence_GetItem()``:

  * ``PyList_GetItem()``
  * ``PyTuple_GetItem()``
  * ``PyDict_GetItem()``

Implementations for concrete types don't *have to* be part of the C API.
Moreover, using directly them introduce bugs when the caller pass a subtype.
For example, PyDict_GetItem() **must not** be used on a dict subtype, since
``__getitem__()`` be be overriden for good reasons.


Functions to call functions
===========================


* ``PyEval_CallFunction()``: a comment says *"PyEval_CallFunction is exact copy
  of PyObject_CallFunction. This function is kept for backward compatibility."*
* ``PyEval_CallMethod()``: a comment says *"PyEval_CallMethod is exact copy of
  PyObject_CallMethod. This function is kept for backward compatibility."*

Open questions
==============

Functions to call functions
---------------------------

Should we remove the following functions to make the C API smaller?

* ``PyEval_CallObjectWithKeywords()``: almost duplicate ``PyObject_Call()``,
  except that *args* (tuple of positional arguments) can be ``NULL``
* ``PyObject_CallObject()``: almost duplicate ``PyObject_Call()``,
  except that *args* (tuple of positional arguments) can be ``NULL``
