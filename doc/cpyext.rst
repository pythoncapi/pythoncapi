.. _cpyext:

++++++++++++++++++
PyPy cpyext module
++++++++++++++++++

cpyext is the implementation of the C API in PyPy.

See Ronan Lamy's talk `Adventures in compatibility emulating CPython's C API in
PyPy <https://www.youtube.com/watch?v=qH0eeh-4XE8>`_ (Youtube video) at
EuroPython 2018.

Source
======

See `pypy/module/cpyext/
<https://bitbucket.org/pypy/pypy/src/default/pypy/module/cpyext/>`_ and
`cpyext/stubs.py
<https://bitbucket.org/pypy/pypy/src/default/pypy/module/cpyext/stubs.py>`_.

cpyext has unit tests written in Python.

Performance issue
=================

PyPy with cpyext remains slower than CPython.

XXX how much?

Issue with borrowed references
==============================

See :ref:`Borrowed references <borrowed-ref>`.

Replace macros with functions
=============================

Already done in cpyext.
