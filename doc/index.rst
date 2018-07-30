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

* Optimization attempts like Unladen Swallow and Pyston failed because of the C
  API and the lack of an usable :ref:`stable ABI <stable-abi>`.
* "Short" Python lifecycle doesn't fit well with the "long" :ref:`lifecycle of
  operating systems <os-vendors>`: how to get the latest Python on an "old" but
  stable operating system?
* :ref:`Python debug build <debug-build>` is currently basically unusable.

Pages
=====

.. toctree::
   :maxdepth: 2

   roadmap
   runtimes
   bad_api
   c_api
   private_c_api
   remove_functions
   backward_compatibility
   os_vendors
   calling_conventions
   stable_abi
   consumers
   rationale
   pep

Links
=====

* `Python C API <https://pythoncapi.readthedocs.io/>`_ (this documentation)
* `pythoncapi GitHub project <https://github.com/vstinner/pythoncapi/>`_
  (this documentation can be found in the ``doc/`` subdirectory).
* `capi-sig mailing list
  <https://mail.python.org/mm3/mailman3/lists/capi-sig.python.org/>`_
