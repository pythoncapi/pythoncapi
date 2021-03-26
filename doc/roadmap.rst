++++++++++++++++++++++++++++++
Roadmap for a new Python C API
++++++++++++++++++++++++++++++

Roadmap
=======

* Step 1: Identify :ref:`Bad C API <bad-c-api>` and list functions that should
  be modified or even removed
* Step 2: Add an **opt-in** :ref:`new C API <new-c-api>` with these cleanups. Test :ref:`popular
  C extensions <consumers>` to measure how much code is broken. Start to fix
  these C extensions by making them **forward** compatible. Slowly involve more
  and more players into the game.
* Step 3: :ref:`Remove more functions <remove-funcs>`. Maybe replace
  :ref:`Py_INCREF() macro <incref>` with a function call. Finish to hide all C
  structures especially ``PyObject.ob_refcnt``. Measure the performance.
  Decide what to do.
* Step 4: if step 3 gone fine and most people are still ok to continue, make
  the :ref:`new C API <new-c-api>` as the default in CPython and add an option
  for **opt-out** to stick with the :ref:`old C API <old-c-api>`.

Open questions
==============

* Remove or deprecate APIs using borrowed references? If ``PyTuple_GetItem()``
  must be replaced with ``PyTuple_GetItemRef()``, how do we provide
  ``PyTuple_GetItemRef()`` for Python 3.7 and older? See :ref:`Backward
  compatibility <back-compat>`.

Status
======

* 2020-04-10: `PEP: Modify the C API to hide implementation details
  <https://mail.python.org/archives/list/python-dev@python.org/thread/HKM774XKU7DPJNLUTYHUB5U6VR6EQMJF/#TKHNENOXP6H34E73XGFOL2KKXSM4Z6T2>`_
  sent to python-dev.
* 2019-05-01: `Status of the stable API and ABI in Python 3.8
  <https://github.com/vstinner/conf/blob/master/2019-Pycon/status_stable_api_abi.pdf>`_,
  slides of Victor Stinner's lightning talk at the Language Summit (during
  Pycon US 2019)
* 2019-02-22: `[capi-sig] Update on CPython header files reorganization
  <https://mail.python.org/archives/list/capi-sig@python.org/thread/WS6ATJWRUQZESGGYP3CCSVPF7OMPMNM6/>`_
* 2018-09-04: Creation of CPython fork to experiment a new incompatible C
  API excluding borrowed references and not access directly structure
  members.
* 2018-07-29: `pythoncapi project <https://github.com/vstinner/pythoncapi>`_
  created on GitHub
* 2018-06: capi-sig mailing list migrated to Mailman 3
* 2017-12-21: It's an idea. There is an old PEP draft, but no implementation,
  the PEP has no number and was not accepted yet (nor really proposed).
* 2017-11: Idea proposed on python-dev, `[Python-Dev] Make the stable API-ABI
  usable
  <https://mail.python.org/pipermail/python-dev/2017-November/150607.html>`_
* 2017-09: Blog post: `A New C API for CPython
  <https://vstinner.github.io/new-python-c-api.html>`_
* 2017-09: Idea discussed at the CPython sprint at Instagram (California).
  Liked by all core developers. The expected performance slowdown is likely to
  be accepted.
* 2017-07-11:
  `[Python-ideas] PEP: Hide implementation details in the C API
  <https://mail.python.org/pipermail/python-ideas/2017-July/046399.html>`_
* 2017-07: Idea proposed on python-ideas. `[Python-ideas] PEP: Hide
  implementation details in the C API
  <https://mail.python.org/pipermail/python-ideas/2017-July/046399.html>`_
* 2017-05: Idea proposed at the Python Language Summit, during PyCon US 2017.
  My `"Python performance" slides (PDF)
  <https://github.com/vstinner/conf/raw/master/2017-PyconUS/summit.pdf>`_.
  LWN article: `Keeping Python competitive
  <https://lwn.net/Articles/723752/#723949>`_.

Players
=======

* CPython: Victor Stinner
* PyPy :ref:`cpyext <cpyext>`: Ronan Lamy
* :ref:`Cython <cython>`: Stefan Behnel

Unknown status:

* `RustPython <https://github.com/RustPython/RustPython>`_
* MicroPython?
* IronPython?
* Jython?
* Pyjion
* Pyston
* any other?
