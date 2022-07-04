# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 12:47:44 2022

@author: afish
"""
import pandas as pd


        
sys_msgs = pd.read_csv('system_messages.csv').set_index('ID')
sys_msgs.index = sys_msgs.index.map(str)
chan_msgs = pd.read_csv('channel_messages.csv').set_index('ID')
chan_msgs.index = chan_msgs.index.map(str)
cont_msgs = pd.read_csv('controller_messages.csv').set_index('ID')
cont_msgs.index = cont_msgs.index.map(lambda x: str(x).zfill(8))
            


class MIDI():
    def __init__(self, filereader):
        super().__init__()
        self.f = filereader
        self.encoding = 'utf-8'
        self.endian = 'big'

        
    def read_int(self, num_bytes=1):
        return int.from_bytes(self.f.read(num_bytes), self.endian)
        
    def read_bin(self, num_bytes=1):
        binary = bin(int.from_bytes(self.f.read(num_bytes), self.endian))
        return binary[2:].zfill(8*num_bytes)
    
    def read_str(self, num_bytes=1):
        return f.read(num_bytes).decode(self.encoding)
    
    def read_hex(self, num_bytes=1):
        integer = int.from_bytes(self.f.read(num_bytes), self.endian)
        return hex(integer)[2:].zfill(2*num_bytes)
        
    def read_event(self):
        delta = self.read_int()
        if delta>127: 
            delta = 128**(delta-127) + self.read_int()
            
        print(f'\nDelta = {delta}')
        code = self.read_bin()
        print(f'Code = {code}')
        if code in sys_msgs.index:
            #print(sys_msgs.Message[code])
            hexcode = self.read_hex()
            length = self.read_int()
            for _ in range(length):
                self.read_int()
            
        if code in cont_msgs.index:
            self.read_int()
            # print(cont_msgs.Message[code])

            
        if code[:4] in chan_msgs.index:
            print(f'Channel = {int(code[4:], 2)}')
            print(chan_msgs.Message[code[:4]])
            [print(self.read_int()) for _ in range(chan_msgs.Bytes[code[:4]])]
            

            

encoding = 'utf-8'
with open('test.mid', 'rb') as f:
    midi = MIDI(f)
    header = midi.read_str(4)
    header_len = midi.read_int(4)
    ftype = midi.read_int(2)
    ntrks = midi.read_int(2)
    division = midi.read_bin(2)

    assert(division[0]=='0')
    ticks = int(division,2)
    

    track = midi.read_str(4)
    chunk_length = midi.read_int(4)
    
    for j in range(80):
        midi.read_event()
    
    
    
    
    