.. _bad-c-api:

+++++++++
Bad C API
+++++++++

The first step to change the Python C API is to define what is a good and a bad
C API. The goal is to hide :ref:`implementation details <impl-details>`.  The
:ref:`new C API <new-c-api>` must not leak implementation details anymore.

See also :ref:`Remove functions <remove-funcs>`.

.. _borrowed-ref:

Borrowed references
===================

CPython 3.7 has 36 functions and macros which return borrowed references:

* ``PyCell_GET()``
* ``PyDict_GetItem()``
* ``PyDict_GetItemWithError()``
* ``PyDict_GetItemString()``
* ``PyDict_SetDefault()``
* ``PyErr_Occurred()``
* ``PyEval_GetBuiltins()``
* ``PyFile_Name()``
* ``PyFunction_GetClosure()``
* ``PyFunction_GetCode()``
* ``PyFunction_GetDefaults()``
* ``PyFunction_GetGlobals()``
* ``PyFunction_GetModule()``
* ``Py_InitModule()``
* ``Py_InitModule3()``
* ``Py_InitModule4()``
* ``PyImport_GetModuleDict()``
* ``PyList_GET_ITEM()``
* ``PyList_GetItem()``
* ``PyMethod_Class()``
* ``PyMethod_Function()``
* ``PyMethod_GET_CLASS()``
* ``PyMethod_GET_FUNCTION()``
* ``PyMethod_GET_SELF()``
* ``PyMethod_Self()``
* ``PyModule_GetDict()``
* ``PyNumber_Check()``
* ``PyObject_Init()``
* ``PySequence_Fast_GET_ITEM()``
* ``PySys_GetObject()``
* ``PySys_GetXOptions()``
* ``PyThreadState_GetDict()``
* ``PyTuple_GET_ITEM()``
* ``PyTuple_GetItem()``
* ``PyWeakref_GET_OBJECT()``
* ``PyWeakref_GetObject()``

CPython contains ``Doc/data/refcounts.dat`` (file is edited manually) which
documents how functions handle reference count.


``PyObject**``
==============

``PyObject**`` must not be exposed: ``PyObject** PySequence_Fast_ITEMS(ob)``
has to go.

Evil PyDict_GetItem()
=====================

The ``PyDict_GetItem()`` API is one of the most commonly called function but
it has multiple flaws:

* it returns a :ref:`borrowed reference <borrowed-ref>`
* it ignores any kind of error: it calls ``PyErr_Clear()``

The lookup is surrounded by ``PyErr_Fetch()`` and ``PyErr_Restore()`` to ignore
any exception.

If hash(key) raises an exception, it clears the exception and just returns
``NULL``.

Enjoy the comment from the C code::

    /* Note that, for historical reasons, PyDict_GetItem() suppresses all errors
     * that may occur (originally dicts supported only string keys, and exceptions
     * weren't possible).  So, while the original intent was that a NULL return
     * meant the key wasn't present, in reality it can mean that, or that an error
     * (suppressed) occurred while computing the key's hash, or that some error
     * (suppressed) occurred when comparing keys in the dict's internal probe
     * sequence.  A nasty example of the latter is when a Python-coded comparison
     * function hits a stack-depth error, which can cause this to return NULL
     * even if the key is present.
     */

Functions implemented with ``PyDict_GetItem()``:

* ``PyDict_GetItemString()``
* ``_PyDict_GetItemId()``

There is ``PyDict_GetItemWithError()`` which doesn't ignore all errors: it only
ignores ``KeyError`` if the key doesn't exist. Sadly, the function still
returns a borrowed references.

C structures
============

Don't leak the structures like ``PyObject`` or ``PyTupleObject`` to not
access directly fields, to not use fixed offset at the ABI level. Replace
macros with functions calls. PyPy already does this in its C API (``cpyext``).

Integer overflow
================

``PyLong_AsUnsignedLongMask()`` ignores integer overflow.

``k`` format of ``PyArg_ParseTuple()`` calls ``PyLong_AsUnsignedLongMask()``.

See also ``PyLong_AsLongAndOverflow()``.

Open questions
==============

Reference counting
------------------

Should we do something for reference counting, Py_INCREF and Py_DECREF?
Replace them with function calls at least?

``PyObject_CallFunction("O")``
------------------------------

Weird ``PyObject_CallFunction()`` API: `bpo-28977
<https://bugs.python.org/issue28977>`_. Fix the API or document it?

PyPy requests
-------------

* Deprecate finalizer API.
* Deprecate Unicode API introduced by the PEP 393, compact strings, like
  PyUnicode_4BYTE_DATA(str_obj).
