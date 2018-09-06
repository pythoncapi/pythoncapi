++++++++++++++++++++++++++++++++++++
Rationale to change the Python C API
++++++++++++++++++++++++++++++++++++

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

PyPy cpyext is slow
===================

The :ref:`PyPy cpyext <cpyext>` is slow because there is no efficient way to
write a correct implementation of the :ref:`current C API <old-c-api>`.
For example, :ref:`borrowed references <borrowed-ref>` is hard to optimize
since the runtime cannot track the lifetime of a borrowed object.


The stable ABI is not usable
============================

The current Python C API produces an ABI which is far from :ref:`stable
<stable-abi>`. The API leaks many implementation details into the ABI.

For example, using the ``PyTuple_GET_ITEM()`` macro produces machine code which
uses an **hardcoded** offset. If the PyObject structure changes, the offset
changes, and so the **ABI** changes.

See :ref:`Relationship between the C API and the ABI <from-api-to-api>`.

Issues with an unstable ABI:

* **Packaging.** Developers have to publish one binary package per Python
  version (3.6, 3.7, 3.8, etc.). Upgrading Python 3 to a newer version
  is very hard because of this issue: each binary package must be
  distributed in many versions, one per Python version. A stable ABI
  would allow to build a package for Python 3.6 and use the same binary
  for Python 3.7, 3.8, 3.9, etc.
* **Experiment issue.** It is not possible to change the base Python structures
  like PyObject or PyTupleObject to reduce the memory footprint or implement
  new optimizations. Experiment such changes requires to rebuild C extensions.
* **Debug builds.** Most Linux distributions provide a debug build of Python
  (``python3-dbg``), but such build has a different ABI and so all C extensions
  must be recompiled to be usable on such flavor of Python. Being able to use
  debug builds would ease debugging since the debug builds add many debug
  checks which are too expensive (CPU/memory) to be enabled by default in a
  release build.


Performance problem: How can we make Python 2x faster?
======================================================

"Leaking" implementation details into the ABI prevents many optimizations
opportunities. See :ref:`Optimization ideas <optim-ideas>`.


Keep backward compatibility
===========================

Existing C extensions will still be supported and will not have to be modified.
The :ref:`old C API <old-c-api>` is not deprecated and there is no plan
penalize users of the old C API.

See :ref:`Backward compatibility <back-compat>`.


The Big Carrot
==============

Changing the C API means that authors of C extensions have to do something. To
justify these changes, we need a big carrot. Examples:

* faster Python if you pick new API? faster PyPy :ref:`cpyext <cpyext>`?
* less bugs? Bugs caused by borrow references are hard to debug.
* new features?

