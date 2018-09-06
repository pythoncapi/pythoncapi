++++++++++++++++++++++++++++++++++++
Rationale to change the Python C API
++++++++++++++++++++++++++++++++++++

Problem
=======

The current Python C API produces an ABI which is far from stable. The API
leaks many implementation details into the ABI.

For example, using the ``PyTuple_GET_ITEM()`` macro produces machine code which
uses an **hardcoded** offset. If the PyObject structure changes, the offset
changes, and so the **ABI** changes.

The Big Carrot
==============

Changing the C API means that authors of C extensions have to do something. To
justify these changes, we need a big carrot. Examples:

* faster Python if you pick new API? faster PyPy :ref:`cpyext <cpyext>`?
* less bugs? no more surprising borrow references causing "funny" crashes
* new features?

Performance problem: How can we make Python 2x faster?
======================================================

"Leaking" implementation details into the ABI prevents many optimizations
opportunities.


Issues with an unstable ABI
===========================

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
