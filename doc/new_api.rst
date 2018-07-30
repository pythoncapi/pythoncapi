.. _new-c-api:

++++++++++++++++++++++
A new C API for Python
++++++++++++++++++++++

Design goals
============

* Reducing the number of :ref:`backward incompatible changes <back-compat>`
  to be able to use the new C API on the maximum number of existing C
  extensions which use directly the C API.
* Hide most CPython implementation details. The exact list has to be written.
* Reduce the size of the C API to reduce the maintenance burden of :ref:`Python
  implementations other than CPython <other-python-impl>`. See :ref:`Remove
  functions <remove-funcs>`.

Non-goal
========

* Cython and cffi must be preferred to write new C extensions: there is no
  intent to replace Cython. Moreover, there is no intent to make Cython
  development harder. Cython will still be able to access directly the full C
  API which includes implementation details and low-level "private" APIs.
