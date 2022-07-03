# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 14:39:52 2022

@author: afisher
"""

import os


def convert_uis(folder=None):
    ''' Convert all .ui files in a specified folder to .py files using the 
    command syntax: pyuic5 -x -o test.py test.ui.'''
    
    files = os.listdir(folder)
    for file in files:
        if file.endswith('.ui'): 
            os.system(f'pyuic5 -x -o {file.strip(".ui")+".py"} {file}')
    return