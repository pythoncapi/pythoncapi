.. _cython:

++++++
Cython
++++++

An alternative to using the C API directly is to rewrite a C extension using
`Cython <http://cython.org/>`__ which generates C code using the C API.

XXX write a better rationale why migrating to Cython!

Questions:

* How many popular Python modules use Cython? See :ref:`Consumers of the
  Python C API <consumers>`.
* How long would it take to rewrite a C extension with ``Cython``?
* What is the long-term transition plan to reach the "no C API" goal? At least,
  CPython will continue to use its own C API internally.
* How to deal with :ref:`backward compatibility <back-compat>`?

Small practical issue: ``Cython`` is not part of the Python 3.7 standard
library yet.

See also :ref:`cffi <cffi>` and :ref:`Remove the C API <remove-c-api>`.