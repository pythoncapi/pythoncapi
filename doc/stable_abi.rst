.. _stable-abi:

++++++++++++++++++
Python stable ABI?
++++++++++++++++++

Links
=====

* `Petr Viktorin's Python Stable ABI improvement
  <https://github.com/encukou/abi3>`_ notes
* `PEP 489 -- Multi-phase extension module initialization
  <https://www.python.org/dev/peps/pep-0489/>`_

  * `bpo-1635741: Py_Finalize() doesn't clear all Python objects at exit
    <https://bugs.python.org/issue1635741>`_
    (convert extensions to multi-phase init PEP 489)

* `PEP 620 -- Hide implementation details from the C API
  <https://www.python.org/dev/peps/pep-0620/>`_ (Victor Stinner)

  * Move the default C API towards the limited C API
  * Make structures opaque:

    * PyObject: https://bugs.python.org/issue39573
    * PyTypeObject: https://bugs.python.org/issue40170
    * PyFrameObject: https://bugs.python.org/issue40421
    * PyThreadState: https://bugs.python.org/issue39947
    * PyInterpreterState: DONE in Python 3.8!
    * PyGC_Head: DONE in Python 3.9!

  * `bpo-40989: Remove _Py_NewReference() and _Py_ForgetReference() from the
    public C API <https://bugs.python.org/issue40989>`_
  * `bpo-41078: Convert PyTuple_GET_ITEM() macro to a static inline function
    <https://bugs.python.org/issue41078>`_
  * `bpo-40601: Hide static types from the limited C API
    <https://bugs.python.org/issue40601>`_

* `PEP 630 -- Isolating Extension Modules
  <https://www.python.org/dev/peps/pep-0630/>`_ (Petr Viktorin)

  * `bpo-40077: Convert static types to heap types: use PyType_FromSpec()
    <https://bugs.python.org/issue40077>`_

* `bpo-41111: Convert a few stdlib extensions to the limited C API
  <https://bugs.python.org/issue41111>`_
* `HPy project <https://hpy.readthedocs.io/>`_


.. _from-api-to-api:

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

To reduce the maintenance burden, :ref:`Linux vendors <os-vendors>` only
provide C extensions compiled in release mode, making the :ref:`debug mode
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
