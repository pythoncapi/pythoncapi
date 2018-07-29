#!/usr/bin/env python3
"""
Script parsing CPython Doc/data/refcounts.dat to list functions which
return a borrow PyObject* reference.
"""
import sys


def parse_refcounts(filename):
    total = 0
    header = True
    for line in open(filename, encoding="utf8"):
        pos = line.find('#')
        if pos >= 0:
            line = line[pos:]
        line = line.strip()
        if not line:
            header = True
            continue
        if not header:
            continue
        if ':PyObject*:' in line and line.endswith((':0', ':0:')):
            func = line.split(':')[0]
            print("Borrowed reference: %s()" % func)
            total += 1
        header = False

    print()
    print("Total: %s functions" % total)


def main():
    if len(sys.argv) != 2:
        print("usage: %s cpython/Doc/data/refcounts.dat" % sys.argv[0])
        sys.exit(1)
    filename = sys.argv[1]
    parse_refcounts(filename)


if __name__ == "__main__":
    main()
