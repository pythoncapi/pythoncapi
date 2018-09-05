.. _optim-ideas:

++++++++++++++++++
Optimization ideas
++++++++++++++++++

Once the :ref:`new C API <new-c-api>` will succeed to hide implementation
details, it becomes possible to experiment radical changes in CPython to
implement new optimizations.

See :ref:`Experimental runtime <exp-runtime>`.

Remove debug checks
===================

See :ref:`Regular runtime <regular-runtime>`: since a debug runtime will be
provided by default, many sanity checks can be removed from the release build.

.. _change-gc:

Change the garbage collector and remove reference counting: unlikely
====================================================================

CPython 3.7 garbage collector (GC) uses "stop-the-world" which is a big issue
for realtime applications like games and can be major issue more generally
for performance critical applications. There is a desire to use a GC which
doesn't need to "stop the world". PyPy succeeded to use an incremental GC.

There are discussing to use a tracing garbage collector for CPython, but this
idea remains highly hypothetical since it very likely require deep changes in
the C API, which is out of the scope of the :ref:`new C API project
<new-c-api>`. The main risk is to break too many C extensions which would make
this idea unsuable in practice.

It may be possible to emulate reference counting for the C API. Py_INCREF() and
Py_DECREF() would be reimplemented using an hash table: object => reference
counter.

See also :ref:`Reference counting <refcount>`.

Remove the GIL: unlikely
========================

Removing the Global Interpreter Lock (GIL) from CPython, or at least being able
to use one GIL per Python interpreter (when using multiple interpreters per
process) is an old dream. It means replacing a single big lock with many
smaller locks, maybe one lock per Python object.

Jython has not GIL.

Reference couting remains a good and convenient API for C extension. Maybe this
design can be kept for the public C API for external C extensions, but CPython
internals can be modified to avoid reference counting, like using a tracing
garbage collector for example. Once the C API stops leaking implementation
details, many new options become possible.

Gilectomy project is CPython 3.6 fork which tries to remove the GIL. In 2017,
the project did not succeed yet to scale linearly performances with the number
of threads. It seems like **reference counting is a performance killer** for
multithreading.

By the way, using atomic operations to access (increase in ``Py_INCREF()``,
decrease and test in ``Py_DECREF()``) the reference count has been proposed,
but experiment showed a slowdown of 20% on single threaded microbenchmarks.


Tagged pointers: doable
=======================

See `Wikipedia: Tagged pointer
<https://en.wikipedia.org/wiki/Tagged_pointer>`_.

Tagged pointers are used by MicroPython to reduce the memory footprint.

Using tagged pointers is a common optimization technic to reduce the
boxing/unboxing cost and to reduce the memory consumption.

Currently, it's not possible to implement such optimization, since most of the
C API rely on real pointer values for direct access to Python objects.

Note: ARM64 was recently extended its address space to 48 bits, causing
issue in LuaJIT: `47 bit address space restriction on ARM64
<https://github.com/LuaJIT/LuaJIT/issues/49>`_.

Copy-on-Write (CoW): doable
===========================

**Copy-on-Write (CoW).** Instagram is using prefork with Django but has
memory usage issues caused by reference counting. Accessing a Python object
modifies its reference counter and so copies the page which was created a COW
in the forked child process. Python 3.7 added `gc.freeze()
<https://docs.python.org/dev/library/gc.html#gc.freeze>`_ workaround.

* Replace ``Py_ssize_t ob_refcnt;`` (integer)
  with ``Py_ssize_t *ob_refcnt;`` (pointer to an integer).
* Same change for the GC header?
* Store all reference counters in a separated memory block
  (or maybe multiple memory blocks)

Expected advantage: smaller memory footprint when using fork() on UNIX
which is implemented with Copy-On-Write on physical memory pages.

See also `Dismissing Python Garbage Collection at Instagram
<https://engineering.instagram.com/dismissing-python-garbage-collection-at-instagram-4dca40b29172>`_.

Transactional Memory: highly experimental
=========================================

PyPy experimented Software Transactional Memory (STM) but the project has
been abandoned, `PyPy STM <http://doc.pypy.org/en/latest/stm.html>`_.


.. _specialized-list:

Specialized list for small integers
===================================

If C extensions don't access structure members anymore, it becomes
possible to modify the memory layout.

For example, it's possible to design a specialized implementation of
``PyListObject`` for small integers::

    typedef struct {
        PyVarObject ob_base;
        int use_small_int;
        PyObject **pyobject_array;
        int32_t *small_int_array;   // <-- new compact C array for integers
        Py_ssize_t allocated;
    } PyListObject;

    PyObject* PyList_GET_ITEM(PyObject *op, Py_ssize_t index)
    {
        PyListObject *list = (PyListObject *)op;
        if (list->use_small_int) {
            int32_t item = list->small_int_array[index];
            /* create a new object at each call */
            return PyLong_FromLong(item);
        }
        else {
            return list->pyobject_array[index];
        }
    }

Each call to ``PyList_GET_ITEM()`` of this example creates a new temporary
object which leads the memory leak (reference leak). This is one concrete
example of issue with borrowed references.

List specialized for numbers is just a example easy to understand to show that
it becomes possible to modify PyObject structures. The main benefit of the
memory footprint, but the overall on performances is unknown at this point.


And more!
=========

Insert your new cool idea here!
