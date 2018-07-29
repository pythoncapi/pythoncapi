++++++++++++
Python C API
++++++++++++

Brainstorm to change the Python C API (to make it better):

* `Python C API <https://pythoncapi.readthedocs.io/>`_
* `pythoncapi GitHub project <https://github.com/vstinner/pythoncapi/>`_
* `capi-sig mailing list
  <https://mail.python.org/mm3/mailman3/lists/capi-sig.python.org/>`_

Content:
* ``doc/`` subdirectory: the current documentation
* ``refcounts_borrowed.py``: search for functions returning a borrowed
  reference from CPython ``Doc/data/refcounts.dat`` file.
