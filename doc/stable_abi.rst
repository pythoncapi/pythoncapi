.. _stable-abi:

++++++++++++++++++
Python stable ABI?
++++++++++++++++++

Relationship between the C API and the ABI
==========================================

Here is a short explanation. For a longer explanation, read `A New C API for
CPython <https://vstinner.github.io/new-python-c-api.html>`_ (September 2017)
by Victor Stinner.

Given the following code::

    typedef struct {
        PyVarObject ob_base;
        PyObject **ob_item;   // <-- pointer to the array of list items
        Py_ssize_t allocated;
    } PyListObject;

    #define PyList_GET_ITEM(op, i) ((PyListObject *)op)->ob_item[i]

And the following C code::

    PyObject *item = PyList_GET_ITEM(list, 0);

On a 64-bit machine, the machine code of a release build becomes something
like::

    PyObject **items = (PyObject **)(((char*)op) + 24);
    PyObject *item = items[0];

whereas a debug build uses an offset of **40** instead of **24**, because
``PyVarObject`` contains additional fields for debugging purpose::

    PyObject **items = (PyObject **)(((char*)op) + 40);
    PyObject *item = items[0];

As a consequence, the compiled C extension is incompatible at the ABI level: a
C extension has to be build twice, once in release mode and once in debug mode.

To reduce the maintaince burden, :ref:`Linux vendors <os-vendors>` only provide
C extensions compiled in release mode, making the :ref:`debug mode
<debug-build>` mostly unusable on Linux in practice.


CPython Py_LIMITED_API
======================

* `CPython documentation: Stable Application Binary Interface
  <https://docs.python.org/3/c-api/stable.html>`_
* Who uses it?
* `PEP 384 -- Defining a Stable ABI
  <https://www.python.org/dev/peps/pep-0384/>`_ by Martin v. Löwis:
  implemented in CPython 3.2 (2011)

Check for ABI changes
=====================

* https://abi-laboratory.pro/tracker/timeline/python/
* https://bugs.python.org/issue21142
* https://sourceware.org/libabigail/
