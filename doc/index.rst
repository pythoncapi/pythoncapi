++++++++++++++++++++++++++++++++++++++++++
Design a new stable API and ABI for Python
++++++++++++++++++++++++++++++++++++++++++

Bad title: "new API".

Good title: "make the stable API usable".

Brainstorm to change the Python C API (to make it better):

* `Python C API <https://pythoncapi.readthedocs.io/>`_ (this documentation)
* `pythoncapi GitHub project <https://github.com/vstinner/pythoncapi/>`_
  (this documentation can be found in the ``doc/`` subdirectory).
* `capi-sig mailing list
  <https://mail.python.org/mm3/mailman3/lists/capi-sig.python.org/>`_

Pages
=====

.. toctree::
   :maxdepth: 2

   bad_api
   c_api
   calling_conventions
   stable_abi
   rationale
   consumers
   pep

Status
======

* 2018-07-29: `pythoncapi project <https://github.com/vstinner/pythoncapi>`_
  created on GitHub
* 2017-12-21: It's an idea. There is an old PEP draft, but no implementation,
  the PEP has no number and was not accepted yet (nor really proposed).

Players
=======

* CPython: Victor Stinner
* PyPy (cpyext): Ronan Lamy
* Cython: Stefan Behnel

Unknown status:

* `RustPython <https://github.com/RustPython/RustPython>`_
* MicroPython?
* IronPython?
* Jython?
* Pyjion
* Pyston
* any other?

Timeline
========

* 2018-06: capi-sig mailing list migrated to Mailman 3
* 2017-11: Idea proposed on python-dev, `[Python-Dev] Make the stable API-ABI
  usable
  <https://mail.python.org/pipermail/python-dev/2017-November/150607.html>`_
* 2017-09: Blog post: `A New C API for CPython
  <https://vstinner.github.io/new-python-c-api.html>`_
* 2017-09: Idea discussed at the CPython sprint at Instagram (California).
  Liked by all core developers. The expected performance slowdown is likely to
  be accepted.
* 2017-07: Idea proposed on python-ideas. `[Python-ideas] PEP: Hide
  implementation details in the C API
  <https://mail.python.org/pipermail/python-ideas/2017-July/046399.html>`_
* 2017-05: Idea proposed at the Python Language Summit, during Pycon US 2017.
  My `"Python performance" slides (PDF)
  <https://github.com/vstinner/conf/raw/master/2017-PyconUS/summit.pdf>`_.
  LWN article: `Keeping Python competitive
  <https://lwn.net/Articles/723752/#723949>`_.
