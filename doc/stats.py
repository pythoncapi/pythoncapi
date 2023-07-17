#!/usr/bin/python
import contextlib
import os

from pythoncapi import (
    GIT_DIR, git_switch_branch,
    PATH_LIMITED_API, PATH_CPYTHON_API, PATH_INTERNAL_API,
    list_files,
    get_types, get_macros_static_inline_funcs,
    get_functions, get_variables, get_line_numbers, get_file_numbers)


BRANCHES = [
    ('v2.7', '2.7.0'),
    ('v3.6.0', '3.6.0'),
    ('v3.7.0', '3.7.0'),
    ('v3.8.0', '3.8.0'),
    ('v3.9.0', '3.9.0'),
    ('v3.10.0', '3.10.0'),
    ('v3.11.0', '3.11.0'),
    #('v3.12.0', '3.12'),
    ('3.12', '3.12 (dev)'),
    ('main', 'main (3.13)'),
]
RST_FILENAME = os.path.normpath(os.path.join(os.path.dirname(__file__), 'stats.rst'))
COLUMNS = ['Python', 'Limited API', 'CPython API', 'Internal API', 'Total']
TABLE_SPACE = '  '


output = []
def log(msg=''):
    output.append(msg)


def display_title(title):
    log(title)
    log('=' * len(title))
    log()


def paragraph(text):
    log(text.strip())
    log()


class Data:
    pass


def _get_data():
    data = Data()
    data.line_numbers = get_line_numbers()
    data.file_numbers = get_file_numbers()
    data.functions = get_functions()
    data.variables = get_variables()
    data.macro_static_inline_funcs = get_macros_static_inline_funcs()
    data.types = get_types()
    return data


def get_data():
    result = []
    for branch, version in BRANCHES:
        git_switch_branch(branch)
        print(f"Parse {branch} header files")
        os.chdir(GIT_DIR)
        data = _get_data()
        result.append((version, data))
    return result


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


def line_numbers(results):
    display_title('Line Numbers')
    paragraph('Number of C API line numbers per Python version:')

    lines = [COLUMNS]
    for name, data in results:
        limited, cpython, internal = data.line_numbers
        total = limited + cpython + internal

        line = [name]
        for value in (limited, cpython, internal):
            line.append(f'{format_number(value)} ({value * 100 / total:.0f}%)')
        line.append(format_number(total))
        lines.append(line)
    render_table(lines)


def file_numbers(results):
    display_title('File Numbers')
    paragraph('Number of header file numbers per Python version:')
    lines = [COLUMNS]
    for name, data in results:
        limited, cpython, internal = data.file_numbers
        line = [name, limited, cpython, internal, limited + cpython + internal]
        lines.append(line)
    table_compute_diff(lines)
    render_table(lines)


def list_functions(results):
    display_title('Functions')
    paragraph('Functions exported with PyAPI_FUNC():')
    lines = [('Python', 'Public', 'Private', 'Internal', 'Total')]
    for name, data in results:
        public, private, internal = data.functions
        total = len(public) + len(private) + len(internal)
        line = [name, len(public), len(private), len(internal), total]
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


def list_variables(results):
    display_title('Variables')
    paragraph('Symbols exported with PyAPI_DATA():')
    lines = [('Python', 'Public', 'Private', 'Internal', 'Total')]
    for name, data in results:
        public, private, internal = data.variables
        total = len(public) + len(private) + len(internal)
        line = [name, len(public), len(private), len(internal), total]
        lines.append(line)
    table_compute_diff(lines)
    render_table(lines)


def static_inline_func(results):
    display_title('Functions defined as macros and static inline functions')
    paragraph('Functions defined as macros and static inline functions:')

    lines = [('Python', 'Macro', 'Static inline', 'Total')]
    for name, data in results:
        macros, static_inline = data.macro_static_inline_funcs

        line = [name, len(macros), len(static_inline),
                len(macros) + len(static_inline)]
        lines.append(line)
    table_compute_diff(lines)
    render_table(lines)

    paragraph('Only count public macros and public static inline functions '
              '(name starting with "Py" or "PY").')


def structures(results):
    display_title('Structures')
    paragraph('Structures in the Python C API:')

    lines = [COLUMNS]
    for name, data in results:
        limited, cpython, internal = data.types
        total = len(limited) + len(cpython) + len(internal)
        line = [name, len(limited), len(cpython), len(internal), total]
        lines.append(line)
    table_compute_diff(lines)
    render_table(lines)
    paragraph('Count also private structures like "_PyCFrame" '
              'and structures with names not starting with Py like "_frozen".')


def render_page():
    results = get_data()

    main_title()
    line_numbers(results)
    file_numbers(results)
    list_functions(results)
    list_variables(results)
    static_inline_func(results)
    structures(results)


def main():
    render_page()

    filename = RST_FILENAME
    with open(filename, 'w') as fp:
        for line in output:
            print(line, file=fp)

    print(f"Write into {filename}")




if __name__ == "__main__":
    main()
