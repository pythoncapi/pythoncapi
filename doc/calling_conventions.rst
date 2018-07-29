.. _calling-conventions:

+++++++++++++++++++++++++
C API calling conventions
+++++++++++++++++++++++++

CPython 3.7 calling conventions
===============================

* METH_NOARGS
* METH_O
* METH_VARARGS
* METH_VARARGS | METH_KEYWORDS
* METH_FASTCALL
* METH_FASTCALL | METH_KEYWORDS

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

PyPy wants this, Cython would benefit as well.

