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

RE_STRUCT_START = re.compile(r'^(?:typedef +)?struct(?: +([A-Za-z0-9_]+))? *{', re.MULTILINE)
RE_STRUCT_END = re.compile(r'^}(?: +([A-Za-z0-9_]+))? *;', re.MULTILINE)


def files(path):
    return glob.glob(os.path.join(path, '*.h'))


def _get_types(filename, names):
    if 'pthread_stubs.h' in filename:
        # skip special header file used by WASM
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
        names.add(name)


def get_types(directory):
    names = set()
    for filename in files(directory):
        _get_types(filename, names)
    return sorted(names)
