# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 09:26:51 2022

@author: afish
"""

import socket
import numpy as np
import re


port = 5282
ip = '127.0.0.1'
ip = '192.168.0.239'

class OSC():
    def __init__(self, ip='127.0.0.1', port='5282'):
        self.af, self.socktype, _, _, self.address = socket.getaddrinfo(ip, port, type=socket.SOCK_DGRAM)[0]
        self.get_commands()
        
    def get_commands(self):
        # Needs improved, clean up regex logic
        regex = '\s+"([-\w]+)"'
        with open('musescore_shortcuts.txt','r') as f:
            lines = f.readlines()
            cmds = []
            for line in lines:
                result = re.search(regex, line)
                if result is not None:
                    cmds.append(result.group().replace(' ','').replace('"',''))
        self.commands = cmds
        return
    
    def send(self, command, args=[]):
        with socket.socket(self.af, self.socktype) as sock:
            if command in self.commands:
                command = '/actions/' + command
            else:
                print('Command not recognized')
            
    
            typetag = ','
            databytes = b''
            args = args if isinstance(args, list) else [args]
            for arg in args:
                if isinstance(arg, int):
                    typetag += 'i'
                    databytes += np.int32(arg).tobytes()
                elif isinstance(arg, float):
                    typetag += 'f'
                    databytes += np.float32(arg).tobytes()
                elif isinstance(arg, str):
                    typetag += 's'
                    databytes += arg.encode('utf-8')
                else:
                    Exception('Datatype not recognized..')
            
            if len(typetag)==1:
                message = command.encode('utf-8')
            else:
                message = command.encode('utf-8') + typetag.encode('utf-8') + databytes
            sock.sendto(message, self.address)
        return 
    

# =============================================================================
# # Working Commands
# note-input
# note-input-steptime
# next-measure and prev-measure
# undo
# redo
# file-new
# file-save
# file-export
# fret-1 with integer input
# string-above and string-below
# =============================================================================


osc = OSC()
osc.send('note-input')


# =============================================================================
# commands = ['note-input','note-d']
# 
# commands = commands if isinstance(commands, list) else [commands]
# for command in commands:
#     osc.send(command)
# =============================================================================







