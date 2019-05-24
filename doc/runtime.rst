+++++++++++++++++++++++++++
Reorganize Python "runtime"
+++++++++++++++++++++++++++

Starter point: `PEP 554 -- Multiple Interpreters in the Stdlib
<https://www.python.org/dev/peps/pep-0554/>`_.

Goal
====

The goal is to support running multiple Python interpreters in parallel with
one lock per interpreter (no more "Global Interpreter Lock", but one
"Interpreter Lock" per interpreter). An interpreter would only be able to run
one Python thread holding the interpreter lock at the same time, but multiple
Python threads which released the interpreter lock (ex: to call a system call
like ``read()``) can be run in parallel.

What do we need?
================

To maximize performances, shared states between interpreters must be minimized.
Each share state must be carefully protected by a lock, which prevent to run
code in parallel.

Current state of the code (2019-05-24)
======================================

During Python 3.7 and 3.8 dev cycle, Eric Snow moved scattered core global
variables into a _PyRuntimeState structure which has a single global and shared
instance: ``_PyRuntime``.

Most functions access directly to ``_PyRuntime``, directly or indirectly:

* ``PyThreadState *tstate = _PyThreadState_GET();`` access implicitly
  ``_PyRuntime``.
* ``PyThreadState *tstate = _PyRuntimeState_GetThreadState(&_PyRuntime);`` gets
  access explicitly ``_PyRuntime``. Get ``runtime->gilstate.tstate_current``.

``_PyRuntimeState`` fields:

* ``ceval``
* ``exitfuncs``, ``nexitfuncs``
* ``finalizing``
* ``gc``
* ``gilstate``
* ``interpreters``
* ``main_thread``
* ``open_code_hook``, ``open_code_userdata``, ``audit_hook_head``
* ``pre_initialized``, ``core_initialized``, ``initialized``
* ``preconfig``
* ``xidregistry``


TODO
====

* Move ``_PyRuntimeState.gilstate`` to ``PyInterpreterState``:

  * Remove ``_PyRuntimeState_GetThreadState()``
  * Update ``_PyThreadState_GET()``

* Move most ``_PyRuntimeState`` fields into ``PyInterpreterState``
* Pass the "context" to private C functions: the context can be ``_PyRuntime``,
  a field of ``_PyRuntime``, the Python thread state (``tstate``), etc.

Out of the scope
================

* Functions of public C API must not be modified at this stage to add
  new "context" parameters. Only the internal C API can be modified.

Roots
=====

* Get the current Python thread:
  ``_PyRuntimeState_GetThreadState(&_PyRuntime)``. WIP: ``gilstate`` must
  move to ``PyInterpreterState``
* Get the current interpreter: ``tstate->interp``.

Status (2019-05-24)
===================

* ``PyInterpreterState`` moved to the internal C API
* ``_PyRuntimeState`` structure and ``_PyRuntime`` variable created


Links
=====

* https://bugs.python.org/issue36710
* https://bugs.python.org/issue36876
* https://bugs.python.org/issue36877
* https://mail.python.org/archives/list/capi-sig@python.org/thread/RBLU35OUT2KDFCABK32VNOH4UKSKEUWW/
* https://twitter.com/VictorStinner/status/1125887394220269568
