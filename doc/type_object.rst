.. _impl-pytype:

+++++++++++++++++++++++++++++
Implement a PyTypeObject in C
+++++++++++++++++++++++++++++

Old C API
=========

Truncated example of the ``PyUnicode_Type`` (Python ``str``)::

    PyTypeObject PyUnicode_Type = {
        PyVarObject_HEAD_INIT(&PyType_Type, 0)
        "str",                        /* tp_name */
        sizeof(PyUnicodeObject),      /* tp_basicsize */
        0,                            /* tp_itemsize */
        /* Slots */
        (destructor)unicode_dealloc,  /* tp_dealloc */
        0,                            /* tp_print */
        0,                            /* tp_getattr */
        0,                            /* tp_setattr */
        0,                            /* tp_reserved */
        unicode_repr,                 /* tp_repr */
        &unicode_as_number,           /* tp_as_number */
        &unicode_as_sequence,         /* tp_as_sequence */
        &unicode_as_mapping,          /* tp_as_mapping */
        (hashfunc) unicode_hash,      /* tp_hash*/
        (...)
        0,                            /* tp_init */
        0,                            /* tp_alloc */
        unicode_new,                  /* tp_new */
        PyObject_Del,                 /* tp_free */
    };

The type must then be initialized once by calling ``PyType_Ready()``::

    if (PyType_Ready(&PyUnicode_Type) < 0) { /* handle the error */ }

This API has an obvious flaw: it rely on the exact implementation of
``PyTypeObject``, the developer has to know all fields.

Variant using C99 syntax::

    static PyTypeObject _abc_data_type = {
        PyVarObject_HEAD_INIT(&PyType_Type, 0)
        "_abc_data",                        /*tp_name*/
        sizeof(_abc_data),                  /*tp_size*/
        .tp_dealloc = (destructor)abc_data_dealloc,
        .tp_flags = Py_TPFLAGS_DEFAULT,
        .tp_alloc = PyType_GenericAlloc,
        .tp_new = abc_data_new,
    };

PyType_FromSpec()
=================

Python 3.1 introduced a new function::

    PyObject* PyType_FromSpec(PyType_Spec *spec)

Documentation:

    Creates and returns a heap type object from the *spec* passed to the function.

There are two additional **private** functions (excluded from the :ref:`Stable
ABI <stable-abi>`)::

    PyObject* PyType_FromSpecWithBases(PyType_Spec*, PyObject*);
    void* PyType_GetSlot(PyTypeObject*, int);

``PyType_GetSlot()`` expects a slot number which comes from
`Include/typeslots.inc
<https://github.com/python/cpython/blob/master/Include/typeslots.h>`_: see
``slotoffsets`` array. The file contains the warning:

    Do not renumber the file; these numbers are **part of the stable ABI**.

Some slots have been disabled (`bpo-10181
<https://bugs.python.org/issue10181>`_)::

    /* Disabled, see #10181 */
    #undef Py_bf_getbuffer
    #undef Py_bf_releasebuffer

Examples of slots::

    #define Py_nb_add 7

    #define Py_tp_alloc 47

    #define Py_tp_call 50

    #define Py_tp_clear 51

    #define Py_tp_doc 56

    #define Py_tp_getattr 57

Example of type::

    static PyType_Slot PyCursesPanel_Type_slots[] = {
        {Py_tp_dealloc, PyCursesPanel_Dealloc},
        {Py_tp_methods, PyCursesPanel_Methods},
        {0, 0},
    };

    static PyType_Spec PyCursesPanel_Type_spec = {
        "_curses_panel.panel",
        sizeof(PyCursesPanelObject),
        0,
        Py_TPFLAGS_DEFAULT,
        PyCursesPanel_Type_slots
    };

Later initialized by::

    PyObject *v = PyType_FromSpec(&PyCursesPanel_Type_spec);
    if (v == NULL)
        goto fail;
    ((PyTypeObject *)v)->tp_new = NULL;
    _curses_panelstate(m)->PyCursesPanel_Type = v;


Remove cross-version binary compatibility
=========================================

See `bpo-32388 <https://bugs.python.org/issue32388>`_.
