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
  implementations other than CPython <other-python-impl>`. See :ref:`Remove
  functions <remove-funcs>`.
* Reduce the size of the ABI, especially export less symbols.

The :ref:`backward compatibility <back-compat>` issue is partially solved by
keeping the existing :ref:`old C API <old-c-api>` available as an opt-in option:
see the :ref:`Regular runtime <regular-runtime>`.

Non-goal
========

* Cython and cffi must be preferred to write new C extensions: there is no
  intent to replace Cython. Moreover, there is no intent to make Cython
  development harder. Cython will still be able to access directly the full C
  API which includes implementation details and low-level "private" APIs.

Hide implementation details
===========================

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

.. _incref:

Py_INCREF()
-----------

The open question remains if it will be possible to replace ``Py_INCREF()`` and
``Py_DECREF()`` with function calls without killing performances.

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
