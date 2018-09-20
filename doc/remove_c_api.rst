.. _remove-c-api:

++++++++++++++++
Remove the C API
++++++++++++++++

One proposed alternative to a new better C API is no C API at all. The reasoning is that since existing
solutions are already available, complete and reliable:

* :ref:`Cython <cython>`
* :ref:`cffi <cffi>`

We do not need to have one for python itself.

However, this approach has lots of open questions without satisfying answers:

What about the long tail of C extensions on PyPI which still use the C extension? 
Would it mean a new Python without all these C extensions on PyPI?

Moreover, lots of project do not use those solution, and the C API is part of Python success. For example, there would be no numpy without the C API, and one can look at :ref:`Consumers of the Python C API <consumers>` to see others examples. 

Removing it would negatively impact those projects, so this doesn't sound like a workable solution.
