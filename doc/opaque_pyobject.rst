.. _opaque-pyobject:

=========================
Opaque PyObject structure
=========================

A blocker issue for many :ref:`optimization ideas <optim-ideas>` is that the
``PyObject`` structure fields are exposed in the public C API. Example::

    PyObject *
    PyUnicode_FromObject(PyObject *obj)
    {
        ...
        PyErr_Format(PyExc_TypeError,
                     "Can't convert '%.100s' object to str implicitly",
                     Py_TYPE(obj)->tp_name);
        return NULL;
    }

with::

    #define Py_TYPE(ob)           (_PyObject_CAST(ob)->ob_type)
    #define _PyObject_CAST(op)    ((PyObject*)(op))

The issue is that ``obj->ob_type`` is accessed directly. It prevents to
implement :ref:`Tagged pointers <tagged-pointer>` for example.

By the way, ``Py_TYPE()`` returns a :ref:`borrowed reference <borrowed-ref>`
which is another kind of problem. See :ref:`Py_TYPE() corner case <py-type>`.

In the long term, ``PyObject`` structure should be opaque. Accessing
``ob_refcnt`` and ``ob_type`` fields should always go through functions.

XXX which functions?

XXX how to convert old code to these new functions?
