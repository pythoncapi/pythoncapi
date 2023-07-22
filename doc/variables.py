#!/usr/bin/python3
import os
import subprocess
from pythoncapi import get_variables

os.chdir('/home/vstinner/python/main')
(public, private, internal) = get_variables()
for name in sorted(private):
    print(name)
