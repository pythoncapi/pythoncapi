.. _calling-conventions:

+++++++++++++++++++++++++
C API calling conventions
+++++++++++++++++++++++++

CPython 3.7 calling conventions
===============================

* ``METH_NOARGS``: ``PyObject* func(PyObject *module)``
* ``METH_O``: ``PyObject* func(PyObject *module, PyObject *arg)``
* ``METH_VARARGS``: ``PyObject* func(PyObject *module, PyObject *args)``,
  *args* type must be ``tuple`` (subclasses are not supported)
* ``METH_VARARGS | METH_KEYWORDS``:
  ``PyObject* func(PyObject *module, PyObject *args, PyObject *kwargs)``,
  *args* type must be ``tuple`` (subclasses are not supported) and *kwargs*
  type must be ``dict`` (subclasses are not supported), *kwargs* can be NULL
* ``METH_FASTCALL``:
  ``PyObject* func(PyObject *module, PyObject *const *args, Py_ssize_t nargs)``,
  nargs must be greater or equal than ``0``
* ``METH_FASTCALL | METH_KEYWORDS``:
  ``PyObject* func(PyObject *module, PyObject *const *args, Py_ssize_t nargs, PyObject *kwnames)``,
  nargs must be greater or equal than ``0`` and *kwnames* must be a Python
  ``tuple`` of Python ``str``.

Argument Clinic
===============

CPython contains a tool called "Argument Clinic" to generate the boilerplate to
parse arguments and convert the result.

Read the CPython documentation: `Argument Clinic How-To
<http://docs.python.org/dev/howto/clinic.html>`_.

Example with the builtin ``compile()`` function::

    /*[clinic input]
    compile as builtin_compile

        source: object
        filename: object(converter="PyUnicode_FSDecoder")
        mode: str
        flags: int = 0
        dont_inherit: bool(accept={int}) = False
        optimize: int = -1

    Compile source into a code object that can be executed by exec() or eval().

    (...)
    [clinic start generated code]*/

    static PyObject *
    builtin_compile_impl(PyObject *module, PyObject *source, PyObject *filename,
                         const char *mode, int flags, int dont_inherit,
                         int optimize)
    /*[clinic end generated code: output=1fa176e33452bb63 input=0ff726f595eb9fcd]*/
    {
        /* ... */
    }

Generated code::

    #define BUILTIN_COMPILE_METHODDEF    \
        {"compile", (PyCFunction)builtin_compile, METH_FASTCALL|METH_KEYWORDS, builtin_compile__doc__},

    static PyObject *
    builtin_compile_impl(PyObject *module, PyObject *source, PyObject *filename,
                         const char *mode, int flags, int dont_inherit,
                         int optimize);

    static PyObject *
    builtin_compile(PyObject *module, PyObject *const *args, Py_ssize_t nargs, PyObject *kwnames)
    {
        PyObject *return_value = NULL;
        static const char * const _keywords[] = {"source", "filename", "mode", "flags", "dont_inherit", "optimize", NULL};
        static _PyArg_Parser _parser = {"OO&s|iii:compile", _keywords, 0};
        PyObject *source;
        PyObject *filename;
        const char *mode;
        int flags = 0;
        int dont_inherit = 0;
        int optimize = -1;

        if (!_PyArg_ParseStackAndKeywords(args, nargs, kwnames, &_parser,
            &source, PyUnicode_FSDecoder, &filename, &mode, &flags, &dont_inherit, &optimize)) {
            goto exit;
        }
        return_value = builtin_compile_impl(module, source, filename, mode, flags, dont_inherit, optimize);

    exit:
        return return_value;
    }

CPython PyArg_ParseTuple() and Py_BuildValue(), getargs.c
=========================================================

Read the CPython documentation: `Parsing arguments and building values
<http://docs.python.org/dev/c-api/arg.html>`_.

Example::

    static PyObject *
    array_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
    {
        int c;
        PyObject *initial = NULL, *it = NULL;

        if (!PyArg_ParseTuple(args, "C|O:array", &c, &initial))
            return NULL;
        ...
    }

Summer 2018: 3 PEPs
===================

* `PEP 576 -- Rationalize Built-in function classes
  <https://www.python.org/dev/peps/pep-0576/>`_
  by Mark Shannon
* `PEP 579 -- Refactoring C functions and methods
  <https://www.python.org/dev/peps/pep-0579/>`_
  by by Jeroen Demeyer
* `PEP 580 -- The C call protocol
  <https://www.python.org/dev/peps/pep-0580/>`_
  by Jeroen Demeyer

New calling conventions?
========================

New calling conventions means more work for everybody? Benefit? Avoid
boxing/unboxing? Avoid temporary expensive Python objects?

Pass C types like ``char``, ``int`` and ``double`` rather than ``PyObject*``?

Use case: call "C function" from a "C function".

Two entry points? Regular ``PyObject*`` entry point, but efficient "C" entry
point as well?

PyPy wants this, :ref:`Cython <cython>` would benefit as well.

