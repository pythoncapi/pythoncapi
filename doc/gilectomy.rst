.. _gilectomy:

+++++++++
Gilectomy
+++++++++

`Gilectomy <https://github.com/larryhastings/gilectomy>`__ is Larry Hastings's
project to attempt to remove the GIL from CPython. It a fork on CPython which
uses lock per object rather than using a Global Interpreter Lock (GIL).

Gilectomy has multiple issues, but the two main issues are:

* The :ref:`current C API <old-c-api>`: "CPython doesn't use multiple cores and
  Gilectomy 1.0 is not high performance, which leads him to **consider breaking
  the C API**".
* Reference counting: "With his complicated buffered-reference-count approach
  he was able to get his "gilectomized" interpreter to reach performance parity
  with CPython—except that his interpreter was running on around seven cores to
  keep up with CPython on one."

For "Gilectomy 2.0", Hastings will be looking at using a tracing garbage
collector (GC), rather than the CPython GC that is based on reference counts.
Tracing GCs are more multi-core friendly, but he doesn't know anything about
them. He also would rather not write his own GC.

* https://github.com/larryhastings/gilectomy
* May 2018: https://lwn.net/Articles/754577/
* PyCon US 2017: https://speakerdeck.com/pycon2017/larry-hastings-the-gilectomy-hows-it-going
