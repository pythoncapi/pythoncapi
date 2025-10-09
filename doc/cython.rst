.. _cython:

++++++
Cython
++++++

An alternative to using the C API directly is to rewrite a C extension using
`Cython <http://cython.org/>`__ which generates C code using the C API.

Cython allows you to wrap existing C code, but if you want to use Python
objects in C or details which are not exposed at the Python level, you still
need the Python C API to work with those.

The code that Cython generates is usually faster than the "obvious" C-API
functions, so *not* using the C-API explicitly in Cython has many advantages,
such as not relying on CPython version details, simplifying your code, and
speeding it up.

Cython is not just a tool to "wrap existing C code". That's only one of
its major use cases. Speeding up Python code, and writing C code without
writing C code, are just as important.

Whether to use Cython or not depends on your use case. It's not
always the obvious choice (otherwise, those other tools would not
exist).

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

See `issue gh-89410 <https://github.com/python/cpython/issues/89410>`_:
"[C API] Add explicit support for Cython to the C API".

See also :ref:`cffi <cffi>` and :ref:`Remove the C API <remove-c-api>`.
