# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 19:48:47 2022

@author: afish
"""

import sys
sys.path.append('C:\\Users\\afisher\\Documents\\GitHub\\Guitar\\PythonArranger\\GUIPackages')

import pandas as pd
import numpy as np

# =============================================================================
# Save songs in pysql database
# 
# =============================================================================

import sys
sys.path.append('C:\\Users\\afisher\\Documents\\GitHub\\Guitar\\PythonArranger\\GUIPackages')
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5.Qt import Qt as qt
import numpy as np
import pandas as pd
from GUI import convert_uis
from Layout import Ui_Layout
import pyqtgraph as pg

# Generate .py from .ui
convert_uis()

# Define parameters
song_dict = {'BPM':120, 'bpm':4, 'capo':0, 'tuning':[0]*6}
spect_dict = {'tmin':0, 'tspan':6, 'wfac':0.5, 'ofac':0.5, 'Nmin':-4, 'Nmax':40}
tab_dict = {'pagelines':8, 'linemeasures':4, 'staff_spacing':4, 'meas_buffer':10}


class Cursor():
    def __init__(self):
        self.beat = 0
        self.string = 0
        self.step = 0.5
        
    def pos(self):
        return (self.beat, self.string)
    
    def move(self, direction):
        if direction=='up':
            self.string = min(self.string+1, 5)
        elif direction=='down':
            self.string = max(self.string-1, 0)
        elif direction=='right':
            self.beat = self.beat + self.step
        elif direction=='left':
            self.beat = max(self.beat-self.step, 0)
        return
    
    def already_played(self, notes):
        matches = (notes[['beat','string']]==self.pos()).all(axis=1)
        status = matches.any()
        idx = None if not status else notes.index[matches].tolist()[0]
        return status, idx


class Transcriber(qtw.QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Import Layout
        self.ui = Ui_Layout()
        self.ui.setupUi(self)

        # Define structures
        self.notes = pd.DataFrame(columns=['beat','string','fret'])
        self.cursor = Cursor()
        
        # Plot staff
        x_staff = [0,2,0]*6 + np.repeat(range(3),3).tolist()
        y_staff = np.repeat(range(6),3).tolist() + [0,5,0]*3
        self.ui.canvas.plot(x_staff, y_staff)
        
        # Add cursor_ptr
        self.ptr = pg.TextItem(text='*')
        self.ui.canvas.addItem(self.ptr)
        self.ptr.setPos(*self.cursor.pos())
        
        # Initialize tab_frets
        self.tab_frets = []
        
    def keyPressEvent(self, signal):

        # Move cursor
        if qt.Key_Left <= signal.key() <= qt.Key_Down:
            if signal.key()==qt.Key_Left:
                self.cursor.move('left')
            if signal.key()==qt.Key_Right:
                self.cursor.move('right')
            if signal.key()==qt.Key_Up:
                self.cursor.move('up')
            if signal.key()==qt.Key_Down:
                self.cursor.move('down')
            self.ptr.setPos(*self.cursor.pos())
            
        # Edit Notes
        
        
        # Add note
        if qt.Key_0 <= signal.key() <= qt.Key_9:
            note_exists, match_idx = self.cursor.already_played(self.notes)
            fret_modifier = 0 if not (signal.modifiers() & qt.ControlModifier) else 10
            fret = signal.key()-48 + fret_modifier
            if not note_exists:
                self.notes.loc[len(self.notes)] = [self.cursor.beat,
                                               self.cursor.string,
                                               fret]
                tab_fret = pg.TextItem(text=str(fret))
                tab_fret.setPos(*self.cursor.pos())
                self.tab_frets.append(tab_fret)
                self.ui.canvas.addItem(tab_fret)
            print(self.notes)
          
        # Remove note
        if signal.key() == qt.Key_Backspace:
            note_exists, match_idx = self.cursor.already_played(self.notes)
            
            if note_exists:
                self.notes = self.notes.drop(labels=match_idx).reset_index(drop=True)
                self.ui.canvas.removeItem(self.tab_frets[match_idx])
                del self.tab_frets[match_idx]
            print(self.notes)
            
        
if __name__ == '__main__':
    app = qtw.QApplication([])
    w = Transcriber()
    w.show()
    app.exec_()



