+++++++++++++
Private C API
+++++++++++++

CPython C API is big, very big. Some functions are "private". Some functions
are declared as private just because their symbol starts with ``_Py`` rather
than ``Py``. Some symbols are hidden from the :ref:`Stable ABI (Py_LIMITED_API)
<stable-abi>`.

There are projects which must access this private API, like debug tools.
