++++++++++++++++++++++++
Split Include/ directory
++++++++++++++++++++++++

Currently, the stable API (Py_LIMITED_API), the private functions (``_Py``
prefix), functions that must only be used in CPython core (``Py_BUILD_CORE``)
and other functions (regular C API) are all defined in the same file. The 3 API
levels:

* Py_BUILD_CORE: API only intended to be used by CPython internals
* Py_LIMITED_API: API for the stable ABI
* other is the :ref:`current C API <old-c-api>`

In the past, many functions have been added to the wrong API level, just
because everything is at the same place. To prevent such mistakes, headers
files should be reorganized with clearly separated files.

* https://bugs.python.org/issue35134
* https://bugs.python.org/issue35081
