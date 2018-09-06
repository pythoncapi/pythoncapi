.. _new-c-api:

++++++++++++++++++++++
A new C API for Python
++++++++++++++++++++++

Design goals
============

* Reducing the number of :ref:`backward incompatible changes <back-compat>`
  to be able to use the new C API on the maximum number of existing C
  extensions which use directly the C API.
* Hide most CPython implementation details. The exact list has to be written.
  One required change is to replace macros with functions calls. The option
  question remains if it will be possible to replace ``Py_INCREF()`` and
  ``Py_DECREF()`` with function calls without killing performances.
* Reduce the size of the C API to reduce the maintenance burden of :ref:`Python
  implementations other than CPython <other-python-impl>`: remove functions.
* Reduce the size of the ABI, especially export less symbols.

The :ref:`backward compatibility <back-compat>` issue is partially solved by
keeping the existing :ref:`old C API <old-c-api>` available as an opt-in option:
see the :ref:`Regular runtime <regular-runtime>`.

.. _remove-funcs:

Remove functions and macros
===========================

Removed functions and macros because they use :ref:`borrowed references
<borrowed-ref>`:

* ``Py_TYPE()``
* ``PyTuple_GET_ITEM()``
* ``PyTuple_GetItem()``
* ``PyTuple_SetItem()``
* ``PyTuple_SET_ITEM()``

New functions
=============

XXX the following functions have been added to the current WORK-IN-PROGRESS
implementation of the new C API. Maybe they will go away later. It's just a
small step to move away from borrowed references. Maybe existing
``PyObject_GetItem()`` and ``PyObject_SetItem()`` are already good enough.

* ``PyTuple_GetItemRef()``: similar to ``PyTuple_GetItem()`` but returns a
  strong reference, rather than a borrowed reference
* ``PyList_GetItemRef()``: similar to ``PyList_GetItem()`` but returns a
  strong reference, rather than a borrowed reference
* ``PyTuple_SetItemRef()``: similar to ``PyTuple_SetItem()`` but uses a strong
  reference on the item
* ``PySequence_Fast_GetItemRef()``
* ``PyStructSequence_SetItemRef()``

XXX private functions:

* ``_Py_SET_TYPE()``: see :ref:`Implement a PyTypeObject in C <impl-pytype>`
* ``_Py_SET_SIZE()``

If we decide that :ref:`Py_TYPE() <py-type>` should go away, 3 more
functions/features are needed:

* ``Py_GetType()``: similar to ``Py_TYPE()`` but returns a strong reference
* ``Py_TYPE_IS(ob, type)``: equivalent to ``Py_TYPE(ob) == type``
* ``%T`` format for ``PyUnicode_FromFormat()``


Non-goal
========

* :ref:`Cython <cython>` and cffi must be preferred to write new C extensions: there is no
  intent to replace Cython. Moreover, there is no intent to make Cython
  development harder. Cython will still be able to access directly the full C
  API which includes implementation details and low-level "private" APIs.

.. _impl-details:

Hide implementation details
===========================

See also :ref:`Bad C API <bad-c-api>`.

What are implementation details?
--------------------------------

"Implementation details" is not well specified at this point, but maybe hiding
implementation can be done incrementally.

The PEP 384 "Defining a Stable ABI" is a very good stable to find the borders
between the public C API and implementation details: see :ref:`Stable ABI
<stable-abi>`.

Replace macros with function calls
----------------------------------

Replacing macros with functions calls is one part of the practical solution.
For example::

    #define PyList_GET_ITEM(op, i) ((PyListObject *)op)->ob_item[i]

would become::

    #define PyList_GET_ITEM(op, i) PyList_GetItem(op, i)

or maybe even::

    PyObject* PyList_GET_ITEM(PyObjcet *op, PyObject *i) { return PyList_GetItem(op, i); }

Adding a **new** ``PyList_GET_ITEM()`` **function** would make the ABI larger,
whereas the ABI should become smaller.

This change remains backward compatible in term of **C API**. Moreover, using
function calls helps to make C extension backward compatible at the **ABI
level** as well.

Problem: it's no longer possible to use ``Py_TYPE()`` and ``Py_SIZE()``
as l-value::

        Py_SIZE(obj) = size;
        Py_TYPE(obj) = type;

XXX in the current implementation, ``_Py_SET_SIZE()`` and ``_Py_SET_TYPE()``
macros have been added for such use case. For the type, see also
:ref:`Implement a PyTypeObject in C <impl-pytype>`.


.. _incref:

Py_INCREF()
-----------

The open question remains if it will be possible to replace ``Py_INCREF()`` and
``Py_DECREF()`` with function calls without killing performances.

See :ref:`Reference counting <refcount>` and :ref:`Change the garbage collector
<change-gc>`.

Hide C structures
-----------------

The most backward incompatible change is to hide fields of C structures, up to
PyObject. To final goal will be able to hide ``PyObject.ob_refcnt`` from the
public C API.

C extensions must be modified to use functions to access fields.

In the worst case, there will be no way to access to hidden field from the
public C API. For these users, the only option will be to stick at the
:ref:`old C API <old-c-api>` which remains backward compatible and still expose
implementation details like C structure fields.
