++++++++++++++++++++++++++++++++++++
Design a new better C API for Python
++++++++++++++++++++++++++++++++++++

Subtitle: "Make the stable API usable".

To be able to introduce backward incompatible changes to the C API without
breaking too many C extensions, this project proposes two things:

* design a :ref:`helper layer <back-compat>` providing :ref:`removed functions
  <remove-funcs>`;
* a new :ref:`Python runtime <runtimes>` which is only usable with C extensions
  compiled with the new stricter and smaller C API (and the new :ref:`stable
  ABI <stable-abi>`) for Python 3.8 and newer, whereas the existing "regular
  python" becomes the "regular runtime" which provides maximum backward
  compatibility with Python 3.7 and older.

The current C API has multiple issues:

* The Python lifecycle is shorter than the :ref:`lifecycle of some operating
  systems <os-vendors>`: how to get the latest Python on an "old" but stable
  operating system?
* :ref:`Python debug build <debug-build>` is currently mostly unusable in
  practice, making development of C extension harder, especially debugging.

Existing C extensions will still be supported and will not have to be modified.
The :ref:`old C API <old-c-api>` is not deprecated and there is no plan
penalize users of the old C API.

Pages
=====

.. toctree::
   :maxdepth: 1

   rationale
   roadmap
   bad_api
   new_api
   runtimes
   old_c_api
   type_object
   remove_functions
   optimization_ideas
   backward_compatibility
   os_vendors
   calling_conventions
   stable_abi
   consumers
   cpyext
   cython
   cffi
   remove_c_api
   performance
   split_include

Links
=====

* `Python C API <https://pythoncapi.readthedocs.io/>`_ (this documentation)
* `pythoncapi GitHub project <https://github.com/pythoncapi/pythoncapi/>`_
  (this documentation can be found in the ``doc/`` subdirectory).
* `capi-sig mailing list
  <https://mail.python.org/mm3/mailman3/lists/capi-sig.python.org/>`_

Table of Contents
=================

.. toctree::
   :maxdepth: 2

   rationale
   roadmap
   bad_api
   new_api
   runtimes
   old_c_api
   type_object
   remove_functions
   optimization_ideas
   backward_compatibility
   os_vendors
   calling_conventions
   stable_abi
   consumers
   cpyext
   cython
   cffi
   remove_c_api
   performance
   split_include

