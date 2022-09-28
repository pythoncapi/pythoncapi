++++++++++++++++++++++++++++++++++++
Design a new better C API for Python
++++++++++++++++++++++++++++++++++++

Subtitle: "Make the stable API usable".

:ref:`PyPy <cpyext>` and :ref:`Gilectomy <gilectomy>` projects are using
different approaches to optimize Python, but their performance are limited by
the :ref:`current C API <old-c-api>` on C extensions. The C API should be
"fixed" to unlock raw performances!

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

Table of Contents
=================

.. toctree::
   :maxdepth: 2

   stats
   status
   rationale
   bad_api
   new_api
   runtimes
   old_c_api
   type_object
   optimization_ideas
   backward_compatibility
   os_vendors
   calling_conventions
   stable_abi
   consumers
   cpyext
   cython
   cffi
   gilectomy
   remove_c_api
   performance
   split_include
   pyhandle
   deprecate
   python_ir
   runtime
   opaque_pyobject
   resource
   links
   misc
