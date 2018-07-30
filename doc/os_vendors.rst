.. _os-vendors:

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Supporting multiple Python versions per operating system release
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Supporting multiple minor Python versions, like Python 3.6 and 3.7, requires
more work for operating system vendors, like Linux vendors. To reduce the
maintenance burden, Linux vendors chose to only support one minor Python
version. For example, even if Fedora 28 provides multiple Python binaries (ex:
2.7, 3.5, 3.6 and 3.7), only packages for Python 3.6 are available. Only
providing a binary is easy. Providing the full chain of dependencies to get a
working Django application is something different.

Issues:

* Each Python minor version introduces subtle minor behaviour changes which
  requires to sometimes to fix issues in Python modules and applications. This
  issue is not solved by the new C API.
* Each C extension must be recompiled once per Python minor version.
* The QA team has to test each Python package: having two packages per Python
  module doubles the work.

Time scale:

* A Python release is supported upstream for 5 years.
* A Fedora release is supported for less than one year.
* Ubuntu LTS releases are supported for 5 years.
* Red Hat Entreprise Linux (RHEL) is supported for 10 years, and customers can
  subscribe to an extended support up to 15 years.

In 2018, the latest macOS release still only provides Python 2.7 which will
reach its end-of-life (EOL) at January 1, 2020 (in less than 2 years).
