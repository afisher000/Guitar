# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 12:47:44 2022

@author: afish
"""
import pandas as pd

class MIDI():
    def __init__(self, filereader):
        super().__init__()
        self.f = filereader
        self.encoding = 'utf-8'
        self.endian = 'big'
        
        self.meta = {'ff54': [('nn', 1, self.read_int), 
                              ('dd', 1, self.read_int), 
                              ('cc', 1, self.read_int), 
                              ('bb', 1, self.read_int)],
                     'ff59': [('sf', 1, self.read_int), 
                              ('mi', 1, self.read_int)],
                     'ff03': [('track_name', -1, self.read_str)]}
    
    def get_keysignature(self):
        assert self.read_int()==2
        self.sf = self.read_int()
        self.mi = self.read_int()
        return
        
    def get_timesignature(self):
        assert self.read_int()==5
        self.nn = self.read_int()
        self.dd= self.read_int()
        self.cc = self.read_int()
        self.bb = self.read_int()
        return
        
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
        delta = self.read_hex()
        event = self.read_hex()
        if event=='ff':
            event += self.read_hex()
            length = self.read_int()
            
            if event in self.meta.keys():
                for attr, num_bytes, fcn in self.meta[event]:
                    if num_bytes==-1:
                        num_bytes == length
                    setattr(self, attr, fcn(num_bytes))
                    print(f'Set attr {attr}')
            else:
                print(f'Do not recognize event {event}')
            
        
            
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
    
    midi.read_event()
    midi.read_event()
    
    
    
    
    
    
    
    
    
    
    