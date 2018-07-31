++++++++++++++++++++++++
Split Include/ directory
++++++++++++++++++++++++

Currently, the ``Include/`` directory of CPython contains 3 levels of API:

* Py_BUILD_CORE: API only intended to be used by CPython internals
* Py_LIMITED_API: API for the stable ABI
* other is the :ref:`current C API <old-c-api>`

In the past, many functions have been added to the wrong API level just because
everything is at the same place. To prevent such mistakes, headers files should
be reorganized.
