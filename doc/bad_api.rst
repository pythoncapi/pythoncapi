.. _bad-c-api:

+++++++++
Bad C API
+++++++++

The first step to change the Python C API is to define what is a good and a bad
C API. The goal is to hide :ref:`implementation details <impl-details>`.  The
:ref:`new C API <new-c-api>` must not leak implementation details anymore.

The Python C API is just too big. For performance reasons, CPython calls
internally directly the implementation of a function instead of using the
abstract API. For example, ``PyDict_GetItem()`` is preferred over
``PyObject_GetItem()``. Inside, CPython, such optimization is fine. But
exposing so many functions is an issue: CPython has to keep backward
compatibility, PyPy has to implement all these functions, etc. Third party
C extensions should call abstract functions like ``PyObject_GetItem()``.

.. _borrowed-ref:

Borrowed references
===================

Problem caused by borrowed references
-------------------------------------

A borrowed reference is a pointer which doesn't "hold" a reference. If the
object is destroyed, the borrowed reference becomes a `dangling pointer
<https://en.wikipedia.org/wiki/Dangling_pointer>`_: point to freed memory which
might be reused by a new object. Borrowed references can lead to bugs and
crashes when misused. Recent example of CPython bug: `bpo-25750: crash in
type_getattro() <https://bugs.python.org/issue25750>`_.

Borrowed references are a problem whenever there is no reference to borrow:
they assume that a referenced object already exists (and thus have a positive
refcount), so that it is just borrowed.

:ref:`Tagged pointers <tagged-pointer>` are an example of this: since there is
no concrete ``PyObject*`` to represent the integer, it cannot easily be
manipulated.

PyPy has a similar problem with list strategies: if there is a list containing
only integers, it is stored as a compact C array of longs, and the W_IntObject
is only created when an item is accessed (most of the time the W_IntObject is
optimized away by the JIT, but this is another story).

But for :ref:`cpyext <cpyext>`, this is a problem: ``PyList_GetItem()`` returns a borrowed
reference, but there is no any concrete ``PyObject*`` to return! The current
``cpyext`` solution is very bad: basically, the first time ``PyList_GetItem()``
is called, the *whole* list is converted to a list of ``PyObject*``, just to
have something to return: see `cpyext get_list_storage()
<https://bitbucket.org/pypy/pypy/src/b9bbd6c0933349cbdbfe2b884a68a16ad16c3a8a/pypy/module/cpyext/listobject.py#lines-28>`_.

See also the :ref:`Specialized list for small integers <specialized-list>`
optimization: same optimization applied to CPython. This optimization is
incompatible with borrowed references, since the runtime cannot guess when the
temporary object should be destroyed.


If ``PyList_GetItem()`` returned a strong reference, the ``PyObject*`` could
just be allocated on the fly and destroy it when the user decref it. Basically,
by putting borrowed references in the API, we are fixing in advance the data
structure to use!

C API using borrowed references
-------------------------------

CPython 3.7 has many functions and macros which return or use borrowed
references.  For example, ``PyTuple_GetItem()`` returns a borrowed reference,
whereas ``PyTuple_SetItem()`` stores a borrowed reference (store an item into a
tuple without increasing the reference counter).

CPython contains ``Doc/data/refcounts.dat`` (file is edited manually) which
documents how functions handle reference count.

See also :ref:`functions steal references <steal-ref>`.

Functions
^^^^^^^^^

* ``PyCell_GET()``
* ``PyDict_GetItem()``
* ``PyDict_GetItemString()``
* ``PyDict_GetItemWithError()``
* ``PyDict_SetDefault()``
* ``PyErr_Occurred()``
* ``PyEval_GetBuiltins()``
* ``PyEval_GetFrame()``
* ``PyEval_GetGlobals()``
* ``PyEval_GetLocals()``
* ``PyFunction_GetAnnotations()``
* ``PyFunction_GetClosure()``
* ``PyFunction_GetCode()``
* ``PyFunction_GetDefaults()``
* ``PyFunction_GetGlobals()``
* ``PyFunction_GetModule()``
* ``PyImport_GetModuleDict()``
* ``PyInstanceMethod_Function()``
* ``PyInstanceMethod_GET_FUNCTION()``
* ``PyList_GET_ITEM()``
* ``PyList_GetItem()``
* ``PyMethod_Function()``
* ``PyMethod_GET_FUNCTION()``
* ``PyMethod_GET_SELF()``
* ``PyMethod_Self()``
* ``PyModuleDef_Init()``
* ``PyModule_GetDict()``
* ``PyObject_Init()``
* ``PySequence_Fast_GET_ITEM()``
* ``PyState_FindModule()``
* ``PyStructSequence_GET_ITEM()``
* ``PyStructSequence_GetItem()``
* ``PySys_GetObject()``
* ``PySys_GetXOptions()``
* ``PyThreadState_GetDict()``
* ``PyTuple_GET_ITEM()``
* ``PyTuple_GetItem()``
* ``PyWeakref_GET_OBJECT()``
* ``PyWeakref_GetObject()``: see https://mail.python.org/pipermail/python-dev/2016-October/146604.html

Raw pointer without relase function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``PyBytes_AS_STRING()``
* ``PyBytes_AsString()``
* ``PyEval_GetFuncName()``
* ``PyUnicode_AsUTF8()``
* ``PyUnicode_AsUTF8AndSize()``


.. _py-type:

Py_TYPE() corner case
---------------------

Technically, ``Py_TYPE()`` returns a borrowed reference to a ``PyTypeObject*``.
In practice, for heap types, an instance holds already a strong reference
to the type in ``PyObject.ob_type``. For static types, instances use a borrowed
reference, but static types are never destroyed.

Hugh Fisher summarized:

   It don't think it is  worth forcing every C extension module to be rewritten,
   and incur a performance hit, to eliminate a rare bug from badly written
   code.

Discussions:

* `[Python-Dev] bpo-34595: How to format a type name?
  <https://mail.python.org/pipermail/python-dev/2018-September/155150.html>`_
  (Sept 2018)
* capi-sig: `Open questions about borrowed reference.
  <https://mail.python.org/mm3/archives/list/capi-sig@python.org/thread/V5EMBIIJFJGJGBQPLCFFXCHAUFNTA45H/>`_
  (Sept 2018).


See also :ref:`Opaque PyObject structure <opaque-pyobject>`.


Duplicated functions
====================

* ``PyEval_CallObjectWithKeywords()``: almost duplicate ``PyObject_Call()``,
  except that *args* (tuple of positional arguments) can be ``NULL``
* ``PyObject_CallObject()``: almost duplicate ``PyObject_Call()``,
  except that *args* (tuple of positional arguments) can be ``NULL``


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
``__getitem__()`` be be overridden for good reasons.


Functions kept for backward compatibility
=========================================

* ``PyEval_CallFunction()``: a comment says *"PyEval_CallFunction is exact copy
  of PyObject_CallFunction. This function is kept for backward compatibility."*
* ``PyEval_CallMethod()``: a comment says *"PyEval_CallMethod is exact copy of
  PyObject_CallMethod. This function is kept for backward compatibility."*


No public C functions if it can't be done in Python
===================================================

There should not be C APIs that do something that you can't do in Python.

Example: the C buffer protocol, the Python ``memoryview`` type only expose a
subset of ``buffer`` features.


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

* ``PyTypeObject`` structure should become opaque
* ``PyType_Ready()`` should be removed

See :ref:`Implement a PyTypeObject in C <impl-pytype>` for the rationale.

Integer overflow
================

``PyLong_AsUnsignedLongMask()`` ignores integer overflow.

``k`` format of ``PyArg_ParseTuple()`` calls ``PyLong_AsUnsignedLongMask()``.

See also ``PyLong_AsLongAndOverflow()``.


.. _steal-ref:

Functions stealing references
=============================

* ``PyContextVar_Reset()``: *token*
* ``PyContext_Exit()``: *ctx*
* ``PyErr_Restore()``: *type*, *value*, *traceback*
* ``PyList_SET_ITEM()``
* ``PyList_SetItem()``
* ``PyModule_AddObject()``: *o* on success, no change on error!
* ``PySet_Discard()``: *key*, no effect if key not found
* ``PyString_ConcatAndDel()``: *newpart*
* ``PyTuple_SET_ITEM()``
* ``PyTuple_SetItem()``
* ``Py_DECREF()``: *o*
* ``Py_XDECREF()``: *o* if *o* is not NULL

Border line API:

* ``Py_SETREF()``, ``Py_XSETREF()``: the caller has to manually increment the
  reference counter of the new value
* ``N`` format of ``Py_BuildValue()``?

See also :ref:`borrowed references <borrowed-ref>`.

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

Finalizer API
^^^^^^^^^^^^^

Deprecate finalizer API: PyTypeObject.tp_finalize of `PEP 442
<https://www.python.org/dev/peps/pep-0442/>`_. Too specific to the CPython
garbage collector? Destructors (``__del__()``) are not deterministic in PyPy
because of their garbage collector: context manager must be used
(ex: ``with file:``), or resources must be explicitly released
(ex: ``file.close()``).

Cython uses ``_PyGC_FINALIZED()``, see:

* https://github.com/cython/cython/issues/2721
* https://bugs.python.org/issue35081#msg330045
* `Cython generate_dealloc_function()
  <https://github.com/cython/cython/blob/da657c8e326a419cde8ae6ea91be9661b9622504/Cython/Compiler/ModuleNode.py#L1442-L1456>`_.

Compact Unicode API
^^^^^^^^^^^^^^^^^^^

Deprecate Unicode API introduced by the PEP 393, compact strings, like
``PyUnicode_4BYTE_DATA(str_obj)``.

PyArg_ParseTuple
----------------

The family of ``PyArg_Parse*()`` functions like ``PyArg_ParseTuple()`` support
a wide range of argument formats, but some of them leak implementation details:

* ``O``: returns a borrowed reference
* ``s``: returns a pointer to internal storage

Is it an issue? Should we do something?


For internal use only
=====================

Public but not documented and not part of Python.h:

* ``PyFrame_FastToLocalsWithError()``
* ``PyFrame_FastToLocals()``
* ``PyFrame_LocalsToFast()``

These functions should be made really private and removed from the C API.
