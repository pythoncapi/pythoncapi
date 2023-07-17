import glob
import os.path
import re
import subprocess


# Checkout of Python Git repository
CPYTHON_URL = 'https://github.com/python/cpython'
GIT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'cpython_git'))


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


PUBLIC_NAME_PREFIX = ("Py", "PY")


def run_command(cmd, cwd):
    subprocess.run(cmd,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE,
                   check=True,
                   cwd=cwd)


def git_clone():
    if os.path.exists(GIT_DIR):
        return

    print(f"Clone CPython Git repository: {CPYTHON_URL}")
    dst_name = os.path.basename(GIT_DIR)
    cmd = ['git', 'clone', CPYTHON_URL, dst_name]
    run_command(cmd, cwd=os.path.dirname(GIT_DIR))


_CLEANED = False
_FETCHED = False

def git_switch_branch(branch):
    git_clone()

    global _CLEANED
    if not _CLEANED:
        cmd = ['git', 'clean', '-fdx']
        run_command(cmd, cwd=GIT_DIR)

        cmd = ['git', 'checkout', '.']
        run_command(cmd, cwd=GIT_DIR)

        _CLEANED = True

    if branch == 'main':
        cmd = ['git', 'switch', branch]
        run_command(cmd, cwd=GIT_DIR)

        global _FETCHED
        if not _FETCHED:
            print(f"Update the CPython Git repository (git fetch)")
            cmd = ['git', 'fetch']
            run_command(cmd, cwd=GIT_DIR)
            _FETCHED = True

        cmd = ['git', 'merge', '--ff']
        run_command(cmd, cwd=GIT_DIR)
    else:
        cmd = ['git', 'checkout', branch]
        run_command(cmd, cwd=GIT_DIR)


def list_files(path):
    if not os.path.exists(path):
        return []
    files = glob.glob(os.path.join(path, '*.h'))
    # Don't parse pthread_stubs.h: special header file used by WASM
    for index, name in enumerate(files):
        if os.path.basename(name) == 'pthread_stubs.h':
            del files[index]
            break
    return files


def _get_types(filename, names):
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
            raise Exception(f"{filename}: cannot find end of: {match.group()}")
        name = match2.group(1)
        if not name:
            name = struct_name
        if not name:
            raise Exception(f"{filename}: structure has no name: {match.group()})")
        if name in TYPEDEFS:
            name = TYPEDEFS[name]
        names.add(name)

    if 'pthread_mutex_t' in names:
        raise Exception('pthread_stubs.h was parsed')


def get_types_path(directory):
    names = set()
    for filename in list_files(directory):
        _get_types(filename, names)
    return sorted(names)


def get_types():
    limited = get_types_path(PATH_LIMITED_API)
    cpython = get_types_path(PATH_CPYTHON_API)
    internal = get_types_path(PATH_INTERNAL_API)
    return (limited, cpython, internal)


def grep(regex, filenames, group=0):
    for filename in filenames:
        with open(filename, encoding='utf-8') as fp:
            content = fp.read()

        for match in regex.finditer(content):
            yield match.group(group)


def is_function_public(name):
    return name.startswith(PUBLIC_NAME_PREFIX)


def get_macros_static_inline_funcs():
    files = list_files(PATH_LIMITED_API) + list_files(PATH_CPYTHON_API)

    # Match '#define func('
    # Don't match '#define constant (&obj)': space before '('
    regex = re.compile(fr'^ *# *define (P[Yy][A-Za-z_]+)\(', re.MULTILINE)
    macros = set(grep(regex, files, group=1))

    regex = re.compile(fr'^static inline [^(\n]+ ({RE_IDENTIFIER}) *\(', re.MULTILINE)
    funcs = set(grep(regex, files, group=1))

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

    # Remove PyDTrace_xxx functions
    for name in list(funcs):
        if name.startswith("PyDTrace_"):
            funcs.discard(name)

    # Remove private static inline functions
    for name in list(macros):
        if not is_function_public(name):
            macros.discard(name)
    for name in list(funcs):
        if not is_function_public(name):
            funcs.discard(name)

    return (macros, funcs)


def get_functions():
    regex = re.compile(
        # Ignore "#define PyAPI_FUNC(RTYPE) ..." (pyport.h)
        fr'(?<!define )'
        # 'PyAPI_FUNC(int) '
        fr'PyAPI_FUNC\([^)]+\)[ |\n]*'
        # '_Py_NO_RETURN '
        fr'(?:{RE_IDENTIFIER}+[ |\n]+)*'
        # 'PyLong_FromLong('
        fr'({RE_IDENTIFIER})[ |\n]*\(',
        re.MULTILINE | re.DOTALL)

    def get(path):
        files = list_files(path)
        return set(grep(regex, files, group=1))

    limited = get(PATH_LIMITED_API)
    cpython = get(PATH_CPYTHON_API)
    internal = get(PATH_INTERNAL_API)

    for names in (limited, cpython, internal):
        if 'pthread_create' in names:
            raise Exception('pthread_stubs.h was parsed')

    public = set()
    private = set()
    for name in limited | cpython:
        if is_function_public(name):
            public.add(name)
        else:
            private.add(name)

    return (public, private, internal)


def get_variables():
    regex = re.compile(
        # 'Py_DEPRECATED(3.13) '
        fr'^ *(?:Py_DEPRECATED\([^)]+\) *)?'
        # 'PyAPI_DATA' ... ';'
        fr'PyAPI_DATA.*;',
        re.MULTILINE)

    RE_VARIABLE = (
        # 'name'
        # 'name, name2'
        # 'name, *name2'
        fr'(?:const *)?'
        fr'({RE_IDENTIFIER}(?:, *\*? *{RE_IDENTIFIER})*)'
        # '[]', '[256]', '[PY_EXECUTABLE_KINDS+1]'
        fr'(?:\[[^]]*\])?'
    )

    RE_FUNC = (
        # '(*name) (' ... ')'
        # '*(*name) (' ... ')'
        # 'name (' ... ')'
        fr'(?:\*? *\( *\* *({RE_IDENTIFIER}) *\)|({RE_IDENTIFIER})) *\([^)]*\)'
    )

    regex2 = re.compile(
        # 'PyAPI_FUNC(int) '
        fr'PyAPI_DATA\([^)]+\) +'
        # 'Py_VerboseFlag;'
        fr'(?:{RE_VARIABLE}|{RE_FUNC}) *;',
        re.MULTILINE)

    def get(path):
        files = list_files(path)
        names = set()
        for line in grep(regex, files):
            match = regex2.search(line)
            if match is None:
                raise ValueError(f'fail to parse PyAPI_DATA: {line!r}')
            parts = match.group(1) # variable name
            if not parts:
                parts = match.group(2) # func 1
            if not parts:
                parts = match.group(3) # func 2
            for part in parts.split(','):
                part = part.strip()
                names.add(part)
        return names

    limited = get(PATH_LIMITED_API)
    cpython = get(PATH_CPYTHON_API)
    internal = get(PATH_INTERNAL_API)

    public = set()
    private = set()
    for name in limited | cpython:
        if is_function_public(name):
            public.add(name)
        else:
            private.add(name)

    return (public, private, internal)


def get_line_number(filename):
    with open(filename, encoding="utf-8") as fp:
        line_number = 0
        for _ in fp:
            line_number += 1
    return line_number


def get_line_numbers():
    def get(path):
        line_number = 0
        for filename in list_files(path):
            line_number += get_line_number(filename)
        return line_number

    limited = get(PATH_LIMITED_API)
    cpython = get(PATH_CPYTHON_API)
    internal = get(PATH_INTERNAL_API)
    return (limited, cpython, internal)


def get_file_numbers():
    limited = len(list_files(PATH_LIMITED_API))
    cpython = len(list_files(PATH_CPYTHON_API))
    internal = len(list_files(PATH_INTERNAL_API))
    return (limited, cpython, internal)
