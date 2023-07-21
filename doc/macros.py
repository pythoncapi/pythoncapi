#!/usr/bin/python3
import os
import subprocess
from pythoncapi import get_macros_static_inline_funcs

#os.chdir('/home/vstinner/python/3.11')
#os.chdir('/home/vstinner/python/2.7')
os.chdir('/home/vstinner/python/main')
macros, funcs, private_macros, private_funcs = get_macros_static_inline_funcs()
for name in sorted(private_macros):
    print(name)
