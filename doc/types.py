#!/usr/bin/python3
import os
import subprocess
from pythoncapi import get_types

#os.chdir('/home/vstinner/python/3.12')
#os.chdir('/home/vstinner/python/2.7')
os.chdir('/home/vstinner/python/main')
public, private, internal = get_types()
for name in sorted(private):
    print(name)
