++++++++++++++++++++++++++++++
Status of the new Python C API
++++++++++++++++++++++++++++++

Status
======

2022
----

* 2022-03-04: The `pythoncapi-compat project moves
  <https://github.com/python/steering-council/issues/101>`_ to the GitHub
  Python organization.
* 2022-04-22: Petr Viktorin proposes `PEP 689 – Unstable C API tier
  <https://peps.python.org/pep-0689/>`_.
* 2022-04-12: the Python Steering Council accepts the `PEP 670 – Convert macros
  to functions in the Python C API <https://peps.python.org/pep-0670/>`_. It's
  implemented in Python 3.11.
* 2022-04-04: Petr Viktorin `proposes
  <https://mail.python.org/archives/list/python-dev@python.org/message/DUWBMGLEYP6VFFT7OMMA6KJNJKTEY47R/>`_
  the document: `Draft: C API design strategy
  <https://docs.google.com/document/d/1lrvx-ujHOCuiuqH71L1-nBQFHreI8jsXC966AFu9Mqc/>`_
* 2022-01-28: python-dev: `Slowly bend the C API towards the limited API to get
  a stable ABI for everyone
  <https://mail.python.org/archives/list/python-dev@python.org/thread/DN6JAK62ZXZUXQK4MTGYOFEC67XFQYI5/>`_

2021
----

* 2021-11-30: Victor Stinner proposes `PEP 674 – Disallow using macros as l-values
  <https://peps.python.org/pep-0674/>`_.
* 2021-10-19: Victor Stinner proposes `PEP 670 – Convert macros to functions in the Python C API
  <https://peps.python.org/pep-0670/>`_.
* 2021-10-05: `Python C API: Add functions to access PyObject
  <https://vstinner.github.io/c-api-abstract-pyobject.html>`_ article.
* 2021-10-04: `C API changes between Python 3.5 to 3.10
  <https://vstinner.github.io/c-api-python3_10-changes.html>`_ article.
* 2021-09-28: Victor Stinner proposes `PEP: Taking the Python C API to the Next Level
  <https://mail.python.org/archives/list/python-dev@python.org/thread/RA7Q4JAUEITJBOUAXFEJKRRM2RR3QSZI/>`_.
* 2021-03-26: `Make structures opaque in the Python C API
  <https://vstinner.github.io/c-api-opaque-structures.html>`_ article.

2020
----

* 2020-12-04: On the capi-sig list, `New script: add Python 3.10 support to your C
  extensions without losing Python 3.6 support
  <https://mail.python.org/archives/list/capi-sig@python.org/thread/LFLXFMKMZ77UCDUFD5EQCONSAFFWJWOZ/>`_.
* 2020-10-16: Simon Cross writes `Taking the C API to the Next Level
  <https://github.com/hpyproject/hpy/wiki/c-api-next-level-manifesto>`_
  for HPy.
* 2020-06-19: Victor Stinner proposes `PEP 620 – Hide implementation details from the C API
  <https://peps.python.org/pep-0620/>`_.
* 2020-06-04: Creation of the `pythoncapi-compat project
  <https://github.com/python/pythoncapi-compat>`_
* 2020-04-10: `PEP: Modify the C API to hide implementation details
  <https://mail.python.org/archives/list/python-dev@python.org/thread/HKM774XKU7DPJNLUTYHUB5U6VR6EQMJF/#TKHNENOXP6H34E73XGFOL2KKXSM4Z6T2>`_
  sent to python-dev.

2019
----

* 2019-07-12: Creation of the `HPy project <https://docs.hpyproject.org/>`_ on
  GitHub.
* 2019-06-19: `Split Include/ directory in Python 3.8
  <https://vstinner.github.io/split-include-directory-python38.html>`_ article.
* 2019-05-01: Pycon US 2019: `Status of the stable API and ABI in Python 3.8
  <https://github.com/vstinner/conf/blob/master/2019-Pycon/status_stable_api_abi.pdf>`_,
  slides of Victor Stinner's lightning talk at the Language Summit.
* 2019-04-25: In Python 3.8, the Python debug build ABI becomes compatible with
  the release build ABI (`commit
  <https://github.com/python/cpython/commit/f4e4703e746067d6630410408d414b11003334d6>`__):
  `What’s New In Python 3.8: Debug build uses the same ABI as release build
  <https://docs.python.org/dev/whatsnew/3.8.html#debug-build-uses-the-same-abi-as-release-build>`_.
* 2019-02-22: `[capi-sig] Update on CPython header files reorganization
  <https://mail.python.org/archives/list/capi-sig@python.org/thread/WS6ATJWRUQZESGGYP3CCSVPF7OMPMNM6/>`_

2018
----

* 2018-09-21: Antonio Cuni wrote `Inside cpyext: Why emulating CPython C API is
  so Hard
  <https://morepypy.blogspot.com/2018/09/inside-cpyext-why-emulating-cpython-c.html>`_
  article about the PyPy cpyext module.
* 2018-09-04: Creation of CPython fork to experiment a new incompatible C
  API excluding borrowed references and not access directly structure
  members.
* 2018-07-29: Creation of the `pythoncapi project
  <https://github.com/vstinner/pythoncapi>`_ on GitHub.
* 2018-06: The Python capi-sig mailing list migrated to Mailman 3.

2017
----

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
