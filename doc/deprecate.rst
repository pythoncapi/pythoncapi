++++++++++++++++++
Deprecate old APIs
++++++++++++++++++

CPython is old, the code evolved. Some functions became useless and so should
be removed. But backward compatibility matters in Python, so we need a
transition period with a deprecation process.

The deprecation can be:

* Emitted at runtime: ``DeprecationWarning``
* At the compilation: ``Py_DEPRECATED()``
* In the documentation

Functions that should deprecated:

* Unicode functions using ``Py_UNICODE`` type
* Py_VA_COPY: see `email <https://mail.python.org/pipermail/python-dev/2016-September/146537.html>`_

See:

* https://bugs.python.org/issue19569
*
