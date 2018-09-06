.. _remove-c-api:

++++++++++++++++
Remove the C API
++++++++++++++++

One obvious alternative to a new better C API is no C API at all! Existing
solutions are already available, complete and reliable:

* :ref:`Cython <cython>`
* :ref:`cffi <cffi>`

Open questions: What about the long tail of C extensions on PyPI which still
use the C extension? Would it mean a new Python without all these C extensions
on PyPI?

The C API is part of Python success. There would be no numpy without the C API,
for example. See :ref:`Consumers of the Python C API <consumers>`.
