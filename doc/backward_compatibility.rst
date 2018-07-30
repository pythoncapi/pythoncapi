.. _back-compat:

++++++++++++++++++++++
Backward compatibility
++++++++++++++++++++++

To reduce the risk of failure, changing the C API should be as much as possible
compatible with the old C API. One solution for that is to provide a backward
compatible header file and/or library.

For example, if ``PyDict_GetItem()`` is removed because it returns a borrowed
reference, a new function ``PyDict_GetItemRef()`` which increases the reference
counter can be added in the new API. But to make it backward compatible, a
macro can be used in Python 3.7 using ``PyDict_GetItem()`` and
``Py_XINCREF()``. Pseudo-code::

    static PyObject*
    PyDict_GetItemRef(PyObject *dict, PyObject *key)
    {
        PyObject *value = PyDict_GetItem(dict, key);
        Py_XINCREF(value);
        return value;
    }

Option questions:

* Should the backward compatibility layer be only a header file? Should it
  be a C library?
* Should we support Python 2.7? Technically, supporting Python 2 shouldn't be
  hard since the many functions of the C API are the same between Python 2
  and Python 3.
