+++++++++++++++
Python runtimes
+++++++++++++++

To be able to implement :ref:`backward compatibility <back-compat>`, the plan
is to provide multiple Python runtimes, at least two. An "old" runtime with
maximum backward compatibility, and one "new" runtime which includes
experimental new changes but requires using the newer C API.

Runtimes
========

Regular Python: /usr/bin/python3
--------------------------------

* Python compiled in release mode
* This runtime still provides ``Py_INCREF()`` macro:
  modify ``PyObject.ob_refcnt`` at the ABI level.
* Compatible with Python 3.7 C **API**.
* Should be compatible with Python 3.7 **ABI**.

Compared to Python 3.7 regular runtime, this runtime no longer check its
arguments. The debug runtime should now be preferred to develop C extensions
and to run tests.

Example of Python 3.7 code::

    int
    PyList_Append(PyObject *op, PyObject *newitem)
    {
        if (PyList_Check(op) && (newitem != NULL))
            return app1((PyListObject *)op, newitem);
        PyErr_BadInternalCall();
        return -1;
    }

The ``if (PyList_Check(op) && (newitem != NULL))`` belongs to the debug runtime
and should be removed from the regular Python.

Debug runtime: /usr/bin/python3-dbg
-----------------------------------

* Compatible with Python 3.7 C **API**.
* Compatible with regular runtime 3.8 **ABI**, but **not compatible**
  with regular runtime 3.7 ABI.
* CPython compiled with ``./configure --with-pydebug``
* Provide ``sys.gettotalrefcount()`` which allows to check for reference leaks.
* C function calls check most arguments: check type, value range, etc.
* Runtime compiled with C assertion: crash (kill itself with SIGABRT signal)
  if a C assertion fails (``assert(...);``).
* Use the debug hooks on memory allocators by default, as ``PYTHONDEBUG=debug``
  environment variable: detect memory under- and overflow and misusage of
  memory allocators.
* Compiled without compiler optimizations (``-Og`` or even ``-O0``) to be
  usable with a debugger like ``gdb``: python-gdb.py should work perfectly.
  However, the regular runtime is unusable with gdb since most variables and
  function arguments are stored in registers, and so gdb fails with the
  "<optimized out>" message.

Experimental runtime: experimental-python3
------------------------------------------

* Loading a C extension compiled with Python 3.7 must fail.
* Loading a C extension compiled with the Python C API 3.8 in the backward
  compatible mode must fail.
* Only C extensions compiled with the **new** Python C API 3.8 can be loaded.
  You have to **opt-in** for this runtime.
* Not compatible with Python 3.7 API: PyDict_GetItem() is gone,
  PyDict_GetItemRef() must be used instead.
* Not compatible with Python 3.8 ABI: using Py_INCREF() macro uses
  ``PyObject.ob_refcnt`` at the ABI level, whereas this field must **not** be
  access at the ABI level.
* ``Py_GC`` header and ``PyObject`` structure can be very different from the
  one used by the regular and debug runtimes.

Technically, this experimental runtime is likely to be a opt-in compilation
mode of the upstream CPython code base.

Your runtime
------------

Since a :ref:`stable ABI <stable-abi>` have been designed, if all your C
extensions have opt-in for the new C API: you are now allowed to fork CPython
and experiment your own flavor CPython. Do whatever you want: C extensions only
access your runtime through runtime.

PyPy, RustPython and others
---------------------------

Since the ABI (and the C API) became smaller, you can imagine that Python
implementations other than CPython will be able to more easily have a **full
and up-to-date support** of the latest full C API.

**Welcome into the bright world of multiple new cool and compatible Python
runtimes!**
