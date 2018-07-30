.. _optim-ideas:

++++++++++++++++++
Optimization ideas
++++++++++++++++++

Once the :ref:`new C API <new-c-api>` will succeed to hide implementation
details, it becomes possible to experiment radical changes in CPython to
implement new optimizations.

See :ref:`Experimental runtime <exp-runtime>`.

Change the garbage collector: unlikely
======================================

CPython 3.7 garbage collector (GC) uses "stop-the-world" which is a big issue
for realtime applications like games and can be major issue more generally
for performance critical applications. There is a desire to use a GC which
doesn't need to "stop the world". PyPy succeeded to use an incremental GC.

There are discussing to use a tracing garbage collector for CPython, but this
idea remains highly hypothetical since it very likely require deep changes in
the C API, which is out of the scope of the :ref:`new C API project
<new-c-api>`. The main risk is to break too many C extensions which would make
this idea unsuable in practice.

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

Using tagged pointers is a common optimization technic to reduce the
boxing/unboxing cost and to reduce the memory consumption.

Currently, it's not possible to implement such optimization, since most of the
C API rely on real pointer values for direct access to Python objects.

Copy-on-Write (CoW): doable
===========================

**Copy-on-Write (CoW).** Instagram is using prefork with Django but has
memory usage issues caused by reference counting. Accessing a Python object
modifies its reference counter and so copies the page which was created a COW
in the forked child process. Python 3.7 added `gc.freeze()
<https://docs.python.org/dev/library/gc.html#gc.freeze>`_ workaround.

And more!
=========

Insert your new cool idea here!
