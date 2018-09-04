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

CPython 3.7 has many functions and macros which return or use borrowed
references.  For example, ``PyTuple_GetItem()`` returns a borrowed reference,
whereas ``PyTuple_SetItem()`` stores a borrowed reference (store an item into a
tuple without increasing the reference counter).

CPython contains ``Doc/data/refcounts.dat`` (file is edited manually) which
documents how functions handle reference count.

Functions
---------

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
* ``PyList_GetItem()``
* ``PyList_SetItem()``
* ``PyMethod_Class()``
* ``PyMethod_Function()``
* ``PyMethod_Self()``
* ``PyModule_GetDict()``
* ``PyNumber_Check()``
* ``PyObject_Init()``
* ``PySys_GetObject()``
* ``PySys_GetXOptions()``
* ``PyThreadState_GetDict()``
* ``PyTuple_GetItem()``
* ``PyTuple_SetItem()``
* ``PyWeakref_GetObject()``

Macros
------

* ``PyCell_GET()``
* ``PyList_GET_ITEM()``
* ``PyList_SET_ITEM()``
* ``PyMethod_GET_CLASS()``
* ``PyMethod_GET_FUNCTION()``
* ``PyMethod_GET_SELF()``
* ``PySequence_Fast_GET_ITEM()``
* ``PyTuple_GET_ITEM()``
* ``PyTuple_SET_ITEM()``
* ``PyWeakref_GET_OBJECT()``

Border line:

* ``Py_TYPE()``
* ``Py_SETREF()``, ``Py_XSETREF()``: the caller has to manually increment the
  reference counter of the new value

Borrowed references: PyEval_GetFuncName()
=========================================

* ``PyEval_GetFuncName()`` returns the internal ``const char*`` inside a
   borrowed reference to a function ``__name__``.

Array of pointers to Python objects (``PyObject**``)
====================================================

``PyObject**`` must not be exposed: ``PyObject** PySequence_Fast_ITEMS(ob)``
has to go.

PyDict_GetItem()
================

The ``PyDict_GetItem()`` API is one of the most commonly called function but
it has multiple flaws:

* it returns a :ref:`borrowed reference <borrowed-ref>`
* it ignores any kind of error: it calls ``PyErr_Clear()``

The dictionary lookup is surrounded by ``PyErr_Fetch()`` and
``PyErr_Restore()`` to ignore any exception.

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

Example of macros:

* ``PyCell_GET()``: access directly ``PyCellObject.ob_ref``
* ``PyList_GET_ITEM()``: access directly ``PyListObject.ob_item``
* ``PyMethod_GET_FUNCTION()``: access directly ``PyMethodObject.im_func``
* ``PyMethod_GET_SELF()``: access directly ``PyMethodObject.im_self``
* ``PySequence_Fast_GET_ITEM()``: use ``PyList_GET_ITEM()``
  or ``PyTuple_GET_ITEM()``
* ``PyTuple_GET_ITEM()``: access directly ``PyTupleObject.ob_item``
* ``PyWeakref_GET_OBJECT()``: access directly ``PyWeakReference.wr_object``

PyType_Ready() and setting directly PyTypeObject fields
=======================================================

* ``PyTypeObject`` structure should become opaquet
* ``PyType_Ready()`` should be removed

See :ref:`Implement a PyTypeObject in C <impl-pytype>` for the rationale.

Integer overflow
================

``PyLong_AsUnsignedLongMask()`` ignores integer overflow.

``k`` format of ``PyArg_ParseTuple()`` calls ``PyLong_AsUnsignedLongMask()``.

See also ``PyLong_AsLongAndOverflow()``.

Open questions
==============

.. _refcount:

Reference counting
------------------

Should we do something for reference counting, Py_INCREF and Py_DECREF?
Replace them with function calls at least?

See :ref:`Change the garbage collector <change-gc>` and :ref:`Py_INCREF
<incref>`.

``PyObject_CallFunction("O")``
------------------------------

Weird ``PyObject_CallFunction()`` API: `bpo-28977
<https://bugs.python.org/issue28977>`_. Fix the API or document it?

PyPy requests
-------------

* Deprecate finalizer API.
* Deprecate Unicode API introduced by the PEP 393, compact strings, like
  PyUnicode_4BYTE_DATA(str_obj).

PyArg_ParseTuple
----------------

The family of ``PyArg_Parse*()`` functions like ``PyArg_ParseTuple()`` support
a wide range of argument formats, but some of them leak implementation details:

* ``O``: returns a borrowed reference
* ``s``: returns a pointer to internal storage

Is it an issue? Should we do something?
