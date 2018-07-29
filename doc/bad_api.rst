.. _bad-api:

+++++++++
Bad C API
+++++++++

The first step to change the Python C API is to define what is a good and a bad
C API. This page describes bad API.

**Goal:** Hide implementation details.

The C API must not leak implementation details anymore.

Borrowed references
===================

Borrowed references: Too many functions :-(

Attempt to list them:

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

``PyObject**``
==============

``PyObject**`` must not be exposed: ``PyObject** PySequence_Fast_ITEMS(ob)``
has to go.

C structures
============

Don't leak the structures like ``PyObject`` or ``PyTupleObject`` to not
access directly fields, to not use fixed offset at the ABI level. Replace
macros with functions calls. PyPy already this in its C API (``cpyext``).

Py_INCREF
=========

XXX should we do something for reference counting, Py_INCREF and Py_DECREF?

Replace them with macros?

``PyObject_CallFunction("O")``
==============================

Weird ``PyObject_CallFunction()`` API: `bpo-28977
<https://bugs.python.org/issue28977>`_. Fix the API or document it?

PyPy requests
=============

* Deprecate finalizer API.
* Deprecate Unicode API introduced by the PEP 393, compact strings, like
  PyUnicode_4BYTE_DATA(str_obj).

