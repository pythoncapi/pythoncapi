+++++++++++
Performance
+++++++++++

The C API exposes implementation details for historical reasons (there was no
design for the public C API, the public C API is just the private API made
public), but also for performance. Macros are designed for best performances,
but should be reserved to developers who have a good understanding of CPython
internals.


Performance slowdown
====================

Hiding implementation details is likely to make tiny loops slower, since it
adds function calls instead of directly accessing the memory.

The performance slowdown is expected to be negligible, but has to be measured
once a concrete implmenetation will be written.

Question: would it be acceptable to have a new better C API if the average
slowdown is around 10%? What if the slowdown is up to 25%? Or even 50%?

Right now, the project is too young to guess anything or to bet. Performances
will be carefully measured using the Python benchmark suite pyperformance,
but only once the design of the new C API is complete.

