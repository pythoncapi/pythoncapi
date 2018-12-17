++++++++
PyHandle
++++++++

Email
=====

Copy of Armin Rigo's email (Nov 2018):

https://mail.python.org/pipermail/python-dev/2018-November/155806.html

FWIW, a "handle" is typically something that users of an API store and
pass around, and which can be used to do all operations on some
object.  It is whatever a specific implementation needs to describe
references to an object.  In the CPython C API, this is ``PyObject*``.
I think that using "handle" for something more abstract is just going
to create confusion.

Also FWIW, my own 2 cents on the topic of changing the C API: let's
entirely drop ``PyObject *`` and instead use more opaque
handles---like a ``PyHandle`` that is defined as a pointer-sized C
type but is not actually directly a pointer.  The main difference this
would make is that the user of the API cannot dereference anything
from the opaque handle, nor directly compare handles with each other
to learn about object identity.  They would work exactly like Windows
handles or POSIX file descriptors.  These handles would be returned by
C API calls, and would need to be closed when no longer used.  Several
different handles may refer to the same object, which stays alive for
at least as long as there are open handles to it.  Doing it this way
would untangle the notion of objects from their actual implementation.
In CPython objects would internally use reference counting, a handle
is really just a PyObject pointer in disguise, and closing a handle
decreases the reference counter.  In PyPy we'd have a global table of
"open objects", and a handle would be an index in that table; closing
a handle means writing NULL into that table entry.  No emulated
reference counting needed: we simply use the existing GC to keep alive
objects that are referenced from one or more table entries.  The cost
is limited to a single indirection.

The C API would change a lot, so it's not reasonable to do that in the
CPython repo.  But it could be a third-party project, attempting to
define an API like this and implement it well on top of both CPython
and PyPy.  IMHO this might be a better idea than just changing the API
of functions defined long ago to make them more regular (e.g. stop
returning borrowed references); by now this would mostly mean creating
more work for the PyPy team to track and adapt to the changes, with no
real benefits.

POSIX and Windows API
=====================

POSIX uses file descriptors, ``int`` type:

* open() creates a file descriptor
* dup() duplicates a file descriptor
* close() closes a file descriptor

Windows uses an oquaque ``HANDLE`` type:

* CreateFile() creates a handle
* DuplicateHandle() duplicates a handle
* CloseHandle() closes a handle
