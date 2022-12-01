#!/usr/bin/python
import builtins
import contextlib
import functools
import glob
import re
import os
import subprocess
import sys

from pythoncapi import files, PYTHON_ROOT, PATH_LIMITED_API, PATH_CPYTHON_API, PATH_INTERNAL_API, get_types


RST_FILENAME = 'stats.rst'
MAIN_BRANCH = '3.12'
BRANCHES = [
    '2.7',
    '3.6',
    '3.7',
    '3.8',
    '3.9',
    '3.10',
    '3.11',
    'main',
]
COLUMNS = ['Python', 'Limited API', 'CPython API', 'Internal API', 'Total']
TABLE_SPACE = '  '
RE_IDENTIFIER = r'[A-Za-z_][A-Za-z0-9_]*'


output = []
def log(msg=''):
    output.append(msg)


def get_output(cmd, error=True):
    proc = subprocess.run(cmd,
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL,
                          text=True)
    out = proc.stdout

    exitcode = proc.returncode
    if exitcode and error:
        print(f"Command failed with exit code {exitcode}")
        print(f"cmd: {cmd}")
        print(f"cwd: {os.getcwd()}")
        sys.exit(exitcode)

    return out


def get_int(cmd):
    out = get_output(cmd)
    try:
        return int(out)
    except ValueError:
        print("Command output is not an integer")
        print(f"cmd: {cmd}")
        print(f"cwd: {os.getcwd()}")
        print("stdout:", out)
        sys.exit(1)


@contextlib.contextmanager
def change_directory(path):
    old_dir = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(old_dir)


def iter_branches():
    for name in BRANCHES:
        with change_directory(name):
            if name == 'main':
                name = MAIN_BRANCH
            yield name


def display_title(title):
    log(title)
    log('=' * len(title))
    log()


def paragraph(text):
    log(text.strip())
    log()


def main_title():
    title = 'Statistics on the Python C API'
    log('+' * len(title))
    log(title)
    log('+' * len(title))
    log()


def render_table_line(widths, line):
    text = []
    for width, cell in zip(widths[:-1], line[:-1]):
        cell = cell.ljust(width)
        text.append(cell)
    text.append(line[-1])
    log(TABLE_SPACE.join(text))


def render_table(lines):
    widths = [0] * len(lines[0])
    for line in lines:
        for index, cell in enumerate(line):
            widths[index] = max(widths[index], len(cell))

    table_line = []
    for width in widths:
        table_line.append('=' * width)
    table_line = TABLE_SPACE.join(table_line)

    log(table_line)
    for line_number, line in enumerate(lines, 1):
        render_table_line(widths, line)
        if line_number == 1:
            log(table_line)
    log(table_line)
    log()


def format_number(number):
    return format(number, ',d')


def format_diff(number):
    if number != 0:
        return format(number, '+,d')
    else:
        return 'same'


def table_compute_diff(lines):
    previous = None
    for index, line in enumerate(lines):
        if index >= 2:
            new_line = [line[0]]
            for prev_value, value in zip(previous[1:], line[1:]):
                cell = f'{format_number(value)} ({format_diff(value - prev_value)})'
                new_line.append(cell)
            previous = line
            lines[index] = new_line
        elif index == 1:
            previous = line
            new_line = [line[0]]
            for value in line[1:]:
                cell = f'{format_number(value)}'
                new_line.append(cell)
            lines[index] = new_line
        else:
            pass


def has_include_cpython(name):
    return (name not in ('2.7', '3.6', '3.7'))


def line_numbers():
    display_title('Line Numbers')
    paragraph('Number of C API line numbers per Python version:')

    def get(cmd):
        out = get_output(cmd)
        value = out.split()[0]
        return int(value)

    lines = [COLUMNS]
    for name in iter_branches():
        limited = get('wc -l Include/*.h|grep total')
        if has_include_cpython(name):
            cpython = get('wc -l Include/cpython/*.h|grep total')
        else:
            cpython = 0
        if name not in ['2.7', '3.6']:
            internal = get('wc -l Include/internal/*.h|grep total')
        else:
            internal = 0

        total = limited + cpython + internal
        line = [name]
        for value in (limited, cpython, internal):
            line.append(f'{format_number(value)} ({value * 100 / total:.0f}%)')
        line.append(format_number(total))
        lines.append(line)
    render_table(lines)


def file_numbers():
    display_title('File Numbers')
    paragraph('Number of header file numbers per Python version:')
    lines = [COLUMNS]
    for name in iter_branches():
        limited = len(files(PATH_LIMITED_API))
        cpython = len(files(PATH_CPYTHON_API))
        internal = len(files(PATH_INTERNAL_API))
        line = [name, limited, cpython, internal, limited + cpython + internal]
        lines.append(line)
    table_compute_diff(lines)
    render_table(lines)


def list_functions():
    display_title('Functions')
    paragraph('Functions exported with PyAPI_FUNC():')
    lines = [('Python', 'Public', 'Private', 'Internal', 'Total')]
    for name in iter_branches():
        total = get_int("grep 'PyAPI_FUNC' Include/*.h Include/cpython/*.h Include/internal/*.h|wc -l")
        public = get_int("grep 'PyAPI_FUNC' Include/*.h Include/cpython/*.h|grep -v ' _Py'|wc -l")
        public_private = get_int("grep 'PyAPI_FUNC' Include/*.h Include/cpython/*.h|wc -l")
        private = public_private - public
        internal = get_int("grep 'PyAPI_FUNC' Include/internal/*.h|wc -l")
        line = [name, public, private, internal, total]
        lines.append(line)
    table_compute_diff(lines)
    render_table(lines)

    paragraph("""
Since Python 3.9, Python is now built with ``-fvisibility=hidden`` to avoid
exporting symbols which are not **explicitly** exported.

The ``make smelly`` command checks for public symbols of libpython and C
extension which are prefixed by ``Py`` or ``_Py``. See
the ``Tools/scripts/smelly.py`` script.
    """)


def list_variables():
    display_title('Variables')
    paragraph('Symbols exported with PyAPI_DATA():')
    lines = [('Python', 'Public', 'Private', 'Internal', 'Total')]
    for name in iter_branches():
        total = get_int("grep 'PyAPI_DATA' Include/*.h Include/cpython/*.h Include/internal/*.h|wc -l")
        public = get_int("grep 'PyAPI_DATA' Include/*.h Include/cpython/*.h|grep -v ' _Py'|wc -l")
        public_private = get_int("grep 'PyAPI_DATA' Include/*.h Include/cpython/*.h|wc -l")
        private = public_private - public
        internal = get_int("grep 'PyAPI_DATA' Include/internal/*.h|wc -l")
        line = [name, public, private, internal, total]
        lines.append(line)
    table_compute_diff(lines)
    render_table(lines)


def iter_header_filenames(name):
    if has_include_cpython(name):
        patterns = ['Include/*.h', 'Include/cpython/*.h']
    else:
        patterns = ['Include/*.h']
    for pattern in patterns:
        yield from glob.glob(pattern)


def cat_files(filenames):
    for filename in filenames:
        with open(filename, encoding='utf-8') as fp:
            yield fp.read()

def grep(regex, files, group=0):
    for content in files:
        for match in regex.finditer(content):
            yield match.group(group)


def static_inline_func():
    display_title('Functions defined as macros and static inline functions')
    paragraph('Functions defined as macros (only public) and static inline functions (public or private):')

    lines = [('Python', 'Macro', 'Static inline', 'Total')]
    for name in iter_branches():
        if has_include_cpython(name):
            headers = 'Include/*.h Include/cpython/*.h'
        else:
            headers = 'Include/*.h'

        args = r'[a-zA-Z][a-zA-Z_, ]*'
        regex = re.compile(fr'^ *# *define (P[Yy][A-Za-z_]+) *\( *{args}\)', re.MULTILINE)
        files = cat_files(iter_header_filenames(name))
        macros = set(grep(regex, files, group=1))

        regex = re.compile(fr'^static inline [^(\n]+ ({RE_IDENTIFIER}) *\(', re.MULTILINE)
        files = cat_files(iter_header_filenames(name))
        static_inline = set(grep(regex, files, group=1))
        # FIXME: exclude 'pydtrace'?

        # Remove macros only used to cast arguments types. Like:
        # "static inline void Py_INCREF(...) { ...}"
        # "#define Py_INCREF(obj) Py_INCREF(_PyObject_CAST(obj))"
        # Only count 1 static inline function, ignore the macro.
        macros = macros - static_inline

        line = [name, len(macros), len(static_inline),
                len(macros) + len(static_inline)]
        lines.append(line)
    table_compute_diff(lines)
    render_table(lines)


def structures():
    display_title('Structures')
    paragraph('Structures in the Python C API:')

    lines = [COLUMNS]
    for name in iter_branches():
        limited = len(get_types(PATH_LIMITED_API))
        cpython = len(get_types(PATH_CPYTHON_API))
        internal = len(get_types(PATH_INTERNAL_API))
        line = [name, limited, cpython, internal, limited + cpython + internal]
        lines.append(line)
    table_compute_diff(lines)
    render_table(lines)


def render_page():
    main_title()
    line_numbers()
    file_numbers()
    list_functions()
    list_variables()
    static_inline_func()
    structures()


def main():
    with change_directory(PYTHON_ROOT):
        render_page()

    with open(RST_FILENAME, 'w') as fp:
        for line in output:
            print(line, file=fp)

    print(f"Write into {RST_FILENAME}")




if __name__ == "__main__":
    main()
