#!/usr/bin/python
import os.path
import sys

from pythoncapi import PATH_LIMITED_API, PATH_CPYTHON_API, get_types


def main():
    if not os.path.exists('pyconfig.h.in'):
        print("program must be run in the Python source code directory")
        sys.exit(1)

    limited = get_types(PATH_LIMITED_API)
    if 1:
        cpython = get_types(PATH_CPYTHON_API)
        names = sorted(set(limited) | set(cpython))
    else:
        names = limited
    for name in names:
        print("*", name)
    print()
    print("Total:", len(names))

main()
