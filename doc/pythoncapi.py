import glob
import os.path
import re


# Checkout of Python Git repository, one directory per branch:
#
# - 2.7/ = Python 2.7 branch
# - 3.6/ = Python 3.6 branch
# - main/ = Python main branch
# - etc.
PYTHON_ROOT = '/home/vstinner/python'


PATH_LIMITED_API = 'Include'
PATH_CPYTHON_API = os.path.join('Include', 'cpython')
PATH_INTERNAL_API = os.path.join('Include', 'internal')

RE_IDENTIFIER = r'[A-Za-z_][A-Za-z0-9_]*'
RE_STRUCT_START = re.compile(r'^(?:typedef +)?struct(?: +([A-Za-z0-9_]+))? *{', re.MULTILINE)
RE_STRUCT_END = re.compile(r'^}(?: +([A-Za-z0-9_]+))? *;', re.MULTILINE)


TYPEDEFS = {
    '_object': 'PyObject',
    '_longobject': 'PyLongObject',
    '_typeobject': 'PyTypeObject',
    'PyCodeObject': 'PyCodeObject',
    '_frame': 'PyFrameObject',
    '_ts': 'PyThreadState',
    '_is': 'PyInterpreterState',
    '_xid': '_PyCrossInterpreterData',
    '_traceback': 'PyTracebackObject',
}


def list_files(path):
    if not os.path.exists(path):
        return []
    return glob.glob(os.path.join(path, '*.h'))


def _get_types(filename, names):
    if 'pthread_stubs.h' in filename:
        # skip special header file used by WASM
        return
    if os.path.basename(filename) == 'pystats.h':
        # skip Include/pystats.h which is code only used if Python is built
        # with --enable-pystats (if the Py_STATS macro is defined)
        return

    with open(filename, encoding="utf-8") as fp:
        content = fp.read()

    for match in RE_STRUCT_START.finditer(content):
        struct_name = match.group(1)
        match2 = RE_STRUCT_END.search(content, match.end())
        if not match2:
            raise Exception(f"cannot find end of: {filename}: {match.group()}")
        name = match2.group(1)
        if not name:
            name = struct_name
        if not name:
            raise Exception(f"structure has no name: {filename}: {match.group()})")
        if name in TYPEDEFS:
            name = TYPEDEFS[name]
        names.add(name)


def get_types(directory):
    names = set()
    for filename in list_files(directory):
        _get_types(filename, names)
    return sorted(names)


def grep(regex, filenames, group=0):
    for filename in filenames:
        with open(filename, encoding='utf-8') as fp:
            content = fp.read()

        for match in regex.finditer(content):
            yield match.group(group)


def get_macros_static_inline_funcs():
    files = list_files(PATH_LIMITED_API) + list_files(PATH_CPYTHON_API)

    args = r'[a-zA-Z][a-zA-Z_, ]*'
    regex = re.compile(fr'^ *# *define (P[Yy][A-Za-z_]+) *\( *{args}\)', re.MULTILINE)
    macros = set(grep(regex, files, group=1))

    regex = re.compile(fr'^static inline [^(\n]+ ({RE_IDENTIFIER}) *\(', re.MULTILINE)
    funcs = set(grep(regex, files, group=1))
    # FIXME: exclude 'pydtrace'?

    # Remove macros only used to cast arguments types. Like:
    # "static inline void Py_INCREF(...) { ...}"
    # "#define Py_INCREF(obj) Py_INCREF(_PyObject_CAST(obj))"
    # Only count 1 static inline function, ignore the macro.
    macros = macros - funcs

    for name in list(macros):
        # In Python 3.10, the Py_INCREF() was wrapping the _Py_INCREF() static
        # inline function.
        if f"_{name}" in funcs:
            macros.discard(name)

    return (macros, funcs)
