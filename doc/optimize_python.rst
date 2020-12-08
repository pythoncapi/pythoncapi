+++++++++++++++++++++++++++++++++++++++
Fix the Python C API to optimize Python
+++++++++++++++++++++++++++++++++++++++

CPython cannot be optimized and other Python implementations see their
performances limited by the C API. The relationship between the C API and
performance is not obvious, and even can be counterintuitive.

Optimizations
=============

Faster object allocation
------------------------

CPython requires to allocate all Python objects on the heap memory and objects
cannot be moved during their life cycle.

It would be more efficient to allow to allocate temporary objects on the stack,
implement nurseries of young objects and compact memory to remove "holes" when
many objects are deallocated.

Faster and incremental garbage collection
-----------------------------------------

CPython relies on reference counting to collect garbage. Reference counting
does not scale for parallelism with multithreading.

A tracing and moving garbage collector would be more efficient. The garbage
collection could be done in multiple steps in separated thread rather than
having long delays causing by the CPython blocking stop-the-world gabage
collector.

The ability to deference pointers like ``PyObject*`` make the implementation
of a moving gabarge collector more complicated. Only using handles would make
the implementation simpler.

Run Python threads in parallel
------------------------------

CPython uses a GIL for objects consistency and to ease the implementation
of the C API. The GIL has many convenient advantages to simplify the
implementation. But it basically limits CPython to a single thread to run
CPU-bound workload distributed in multiple threads.

Per-object locks would allow to help to scale threads on multiple threads.

More efficient data structures (boxing/unboxing)
------------------------------------------------

CPython requires builtin types like list and dict to only contain
``PyObject*``.

PyPy implements a list strategy for integers: integers are stored directly as
integers, not as objects. Integers are only boxed on demand.


Reasons why the C API prevents to optimize Python
=================================================

Structures are part of the public C API (make them opaque)
----------------------------------------------------------

Core C structures like ``PyObject`` are part of the public C API and so every
Python implementations must implement exactly this structure.

The C API directly or indirectly access structure members. For example, the
``Py_INCREF()`` function modifies directly ``PyObject.ob_refcnt`` and so makes
the assumption that objects have a reference counter. Another example is
``PyTuple_GET_ITEM()`` which reads directly the ``PyTupleObject.ob_item``
member and so requires ``PyTupleObject`` to only store ``PyObject*`` objects.


The C API should be modified to abstract accesses to objects through function
calls rather than using macros which access directly to structure members.

Structures must be excluded from the public C API: become "opaque".

PyObject* type can be dereferenced (use handles)
------------------------------------------------

Since structures a public, it is possible to deference pointers to access
structure members. For example, access directly to ``PyObject.ob_type`` member
from a ``PyObject*`` pointer, or access directly to
``PyTupleObject.ob_type[index]`` from a ``PyTupleObject*`` pointer.

Using opaque **handles** like HPy what does would prevent that.

Borrowed references (avoid them)
--------------------------------

Many C API functions like ``PyDict_GetItem()`` or ``PyTuple_GetItem()`` return
a borrowed references. They make the assumption that all objects are actual
objects. For example, if tagged pointers are implemented, a ``PyObject*`` does
not point to a concrete object: the value must be boxed to get a ``PyObject*``.
The problem with borrowed references is to decide when it is safe to destroy
the temporary ``PyObject*`` object. One heuristic is to consider that it must
remain alive as long as its container (ex: a list) remains alive.

PyObject must be allocated on the stack
---------------------------------------

In CPython, all objects must be allocated on the stack. Using reference
counting, when an object is passed to a function, the function can store it in
another container and so the object remains alive after the function completes.
The caller cannot destroy the object, since it does not take care of the object
lifecycle. The object can only be destroyed when the last strong reference to
the object is deleted.

Pseudo-code::

    void func(void)
    {
        PyObject *x = PyLong_FromLong(1);
        func(x);
        Py_DECREF(x);
        // if func() creates a new strong reference to x,
        // x is still alive at this point.
    }

HPy uses a different strategy: if a function wants to create a new reference to
a handle, ``HPy_Dup()`` function must be called. ``HPy_Dup()`` can continue to
use the same object, but it can also duplicate an immutable object.

PyObject cannot be moved in memory
----------------------------------

Since ``PyObject*`` is a direct memory address to a ``PyObject``, moving
a ``PyObject`` requires to change all ``PyObject*`` values pointing to it.
Using handles, there is not such issue.

Other C API functions give a direct memory address into an object content
with no API to "release" the resource. For example, ``PyBytes_AsString()``
gives a direct access into the bytes string, there is no way for the object
to know when the caller no longer needs this pointer. The string cannot be
moved in memory.

Functions using ``PyObject**`` type (array of ``PyObject*`` pointers) have a
similar issue. Example: ``&PyTuple_GET_ITEM()`` is used to get
``&PyTupleObject.ob_item``.

The ``PyObject_GetBuffer()`` is a sane API: it requires the caller to call
``PuBuffer_Release()`` to release the ``Py_buffer`` object. Memory can be
copied if needed to allow to move the object while the buffer is used.
