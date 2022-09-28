+++++++++++++++++++++++++++++++++++++++++
Implicit and explicit resource management
+++++++++++++++++++++++++++++++++++++++++

Pointer API
===========

The Python C API has multiple APIs which implicit resource managements:

* ``PyBytes_AsString()``
* ``PyUnicode_AsUTF8AndSize()``

These functions return a pointer to data. The pointer becomes a dangling
pointer once the object is deleted.

This API makes the assumption that the memory address of Python objects are
fixed.  Python implementations moving objects in memory have to pin these
objects in memory to implement the API, and pinning memory is inefficient in
this case.

The ``Py_buffer`` API has a ``PyBuffer_Release()`` function which can execute
code when a buffer is no longer needed:

* Call ``Py_DECREF(obj)``
* Free memory if the buffer was a memory copy
* Close files
* etc.

Array of objects
================

``array = &PyTuple_GET_ITEM(tuple, 0)`` is a common code pattern to access a
Python tuple as a C array of ``PyObject*``: array of ``PyObject**`` type. It
makes the assumption that a tuple stores ``PyObject*`` and ``PyObject**``
becomes a dangling pointer once the tuple is destroyed.
