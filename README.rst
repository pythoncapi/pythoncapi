++++++++++++++++++++++++++++++++++++
Design a new better C API for Python
++++++++++++++++++++++++++++++++++++

Subtitle: "Make the stable API usable".

* `Project website <https://pythoncapi.readthedocs.io/>`_
* `Project source (pythoncapi GitHub project)
  <https://github.com/pythoncapi/pythoncapi/>`_
* `capi-sig mailing list
  <https://mail.python.org/mm3/mailman3/lists/capi-sig.python.org/>`_

Content
=======

* ``doc/`` subdirectory: the current documentation
* ``refcounts_borrowed.py``: search for functions returning a borrowed
  reference from CPython ``Doc/data/refcounts.dat`` file.

Build the documentation
=======================

Work in the ``doc/`` sub-directory.

Install dependencies::

    python -m pip install --user --upgrade sphinx

Build the documentation::

    make html

Regenerate statistics::

    python stats.py
