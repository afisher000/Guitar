# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 14:39:52 2022

@author: afisher
"""

import os
import subprocess

# pyuic5 -o test.py test.ui

files = os.listdir()
for file in files:
    if file.endswith('.ui'):
        print(file)
        syscall = f'pyuic5 -x -o {file.strip(".ui")+".py"} {file}'
        print(syscall)
        #syscall = 'dir'
        os.system(syscall)
        #cmd = subprocess.run(syscall.split(' '), capture_output=True, encoding='UTF-8')
