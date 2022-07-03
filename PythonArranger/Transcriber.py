# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 19:48:47 2022

@author: afish
"""

import sys
sys.path.append('C:\\Users\\afisher\\Documents\\GitHub\\Guitar\\PythonArranger\\GUIPackages')

import pandas as pd
import numpy as np
from GUI import convert_uis
convert_uis()
# =============================================================================
# Guitar tab midi file
# Add full playback?
# Delete full measure
# Copy measures?
# =============================================================================

from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5.Qt import Qt as qt
from main_window import Ui_Layout
from load_window import Ui_Form
import pyqtgraph as pg
import mysql.connector
from sqlalchemy import create_engine
import sounddevice as sd
import soundfile as sf
from scipy.interpolate import interp1d

class Spectrogram():
    def __init__(self):
        self.wfac = 0.5
        self.ofac = 0.5
        self.Nmin = -4
        self.Nmax = 40
        self.tmin = 0
        self.tspan= 6
        pass
    
    
class Database():
    def __init__(self):
        self.conn = mysql.connector.connect(
            user='root',
            passwd='3l3ctr0ns',
            host='localhost')
        self.engine = create_engine('mysql+pymysql://root:3l3ctr0ns@localhost/guitar')
        self.cursor = self.conn.cursor()
        self.execute = lambda query: self.cursor.execute(query)
        
        # Use 'guitar' database        
        if 'guitar' not in self.get_databases():
            self.execute('Create DATABASE guitar')
        self.execute('USE guitar');

    def get_databases(self):
        self.execute('show databases')
        databases = [database[0] for database in self.cursor]
        return databases
    
    def get_tables(self):
        self.execute('show tables')
        tables = [table[0] for table in self.cursor]
        return tables
        
    def create_table(self, table_name):
        command = f'create table {table_name} (beatdiv int, string int, fret int);'
        self.execute(command)
        return
        
    def load_table(self, table_name):
        command = f'select * from guitar.{table_name}'
        notes = pd.read_sql(command, self.conn)
        return notes.astype(int)
        
    def update_table(self, songname, notes):
        notes = notes.astype(int)
        self.execute(f'truncate {songname}')
        notes.to_sql(songname, self.engine, if_exists='replace', index=False)
        print(f'Updated {songname}')
        return
    
    
class Tab():
    def __init__(self):
        self.measurebeats = 4
        self.beatdivs = 96 # divisions in a beat
        self.tempo = 120
        self.capo = 0
        self.tuning = np.zeros(6)
        self.pagelines = 8
        self.linemeasures = 3
        self.staffspacing = 4

        self.linewidth = 5+self.staffspacing
        self.linebeats = self.linemeasures * self.measurebeats  
        self.linedivs = self.linebeats * self.beatdivs
        self.xlimit = self.linebeats
        self.ylimit = -(self.pagelines*self.linewidth+6)
        
    def add_staff(self, canvas):
        stafflines_x = np.append(np.tile([0,self.linebeats,0],6),
                                  np.repeat(self.measurebeats*np.arange(self.linemeasures+1),3))
        stafflines_y = np.append(np.repeat(range(6),3),
                                  np.tile([0,5,0],self.linemeasures+1))*-1
        
        beatlines_x = np.repeat(np.arange(self.linebeats), 3)
        beatlines_y = np.tile([0,5,0], self.linebeats)*-1
        
        for j in range(self.pagelines):
            beatlines = pg.PlotDataItem(beatlines_x,
                                    beatlines_y - j*self.linewidth,
                                    pen=(50,50,50))
            canvas.addItem(beatlines)
            
            stafflines = pg.PlotDataItem(stafflines_x, 
                                         stafflines_y - j*self.linewidth)
            canvas.addItem(stafflines)
        
        return
        

class Cursor():
    def __init__(self):
        self.beatdiv = 0
        self.string = 0
        self.step = 48
        self.stepsizes = [96, 48, 32, 24, 16, 12, 6]
        
    def pos(self, tab):
        beat = self.beatdiv/tab.beatdivs
        line, xpos = divmod(beat, tab.linebeats)
        ypos = self.string - line*tab.linewidth
        return xpos, ypos
    
    def move(self, direction):
        if direction=='up':
            self.string = min(self.string+1, 0)
        elif direction=='down':
            self.string = max(self.string-1, -5)
        elif direction=='right':
            self.beatdiv = self.beatdiv + self.step
        elif direction=='left':
            self.beatdiv = max(self.beatdiv-self.step, 0)
        return
    
    def change_stepsize(self, direction):
        idx = self.stepsizes.index(self.step)
        if direction=='minus':
            idx = min(idx+1, len(self.stepsizes)-1)
        elif direction=='plus':
            idx = max(idx-1, 0)
        self.step = self.stepsizes[idx]
        return
            
    def move_to_mouse(self, target, tab):
        if not 0 <= target.x() <= tab.xlimit:
            return #outside xrange
        if not tab.ylimit <= target.y() <= 0:
            return #outside yrange
        
        line, string = divmod(target.y(), -tab.linewidth)
        self.beatdiv = round(target.x())*tab.beatdivs + line*tab.linedivs
        self.string = round(np.clip(string, -5, 0))
        return

    def check_if_played(self, notes):
        matches = (notes[['beatdiv','string']]==(self.beatdiv, self.string)).all(axis=1)
        note_exists = matches.any()
        idx = None if not note_exists else notes.index[matches].tolist()[0]
        return note_exists, idx



class Load_Window(qtw.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Load or create song
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        # Load song menu using database tables
        song_tables = self.main_window.db.get_tables()
        self.ui.song_menu.addItems(song_tables)
        
        # Button functions
        self.ui.new_song_button.clicked.connect(self.create_song)
        self.ui.load_song_button.clicked.connect(self.load_song)
        
        
    def load_song(self):
        # Get data from table and update notes
        table_name = self.ui.song_menu.currentText()
        if table_name!='':
            self.main_window.load_notes(table_name)
            self.main_window.songname = table_name
            self.main_window.show()
            self.close()
        return
    
    def create_song(self):
        songname = self.ui.songname.text().lower().replace(' ','_')
        
        if songname in self.main_window.db.get_tables() or songname=='':
            msg = qtw.QMessageBox()
            msg.setText('Song Table already exists.')
            msg.exec_()
        else:
            self.main_window.db.create_table(songname)
            self.main_window.songname = songname
            self.main_window.show()
            self.close()
        return
        


class Main_Window(qtw.QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

        # Import Layout
        self.ui = Ui_Layout()
        self.ui.setupUi(self)

        # Define structures
        self.songname = ''
        self.notes = pd.DataFrame(columns=['beatdiv','string','fret'], dtype=int)
        self.cursor = Cursor()
        self.tab = Tab()
        self.db = Database()
        
        # Create canvas plot
        self.ui.canvas.plot()
        self.tab.add_staff(self.ui.canvas)
        self.ui.canvas.setXRange(0, self.tab.xlimit)
        self.ui.canvas.setYRange(self.tab.ylimit,0)
        
        # Update Displays
        self.update_displays()
        self.playsound = True

        # Add cursor_ptr
        self.ptr = pg.TextItem(text='*', anchor=(0.25,0.25))
        self.ptr.setPos(*self.cursor.pos(self.tab))
        self.ui.canvas.addItem(self.ptr)
        
        # Connect signals to slots
        self.ui.canvas.scene().sigMouseClicked.connect(self.mouseclickEvent)
        self.ui.save_button.clicked.connect(self.save_song)
        
        # Initialize textitem_cnt
        self.textitem_cnt = []
        
        # Loading window
        self.load_window = Load_Window(self)
        self.load_window.show()
        self.hide()
        
    
    def playback(self):
        # Start playing the song from the cursor location.
        # Have a way to stop
        pass
        return
        
        
    def play_note(self, string, fret):
        if not self.playsound:
            return

        # Read note .wav
        ref_note = 58
        data, fs = sf.read('guitarnote_A#.wav', dtype='float32')
        time = np.arange(0, len(data)/fs, 1/fs)
        f = interp1d(time, data, bounds_error=False, fill_value=0)

        # Construct signal
        midi_openstrings = np.array([40, 45, 50, 55, 59, 64])
        midi_note = (midi_openstrings+self.tab.tuning)[string+5]+fret
        scale = (2**(1/12))**(midi_note-ref_note)
        sd.play(f(time*scale), fs)
        return

    def update_displays(self):
        # Define outputs
        self.ui.stepsize_display.setText(f'1/{int(96/self.cursor.step)}')
        return
        
    def load_notes(self, table_name):
        self.notes = self.db.load_table(table_name)
        for index, row in self.notes.iterrows():
            self.add_note(row.beatdiv, row.string, row.fret)
        return
        
    def save_song(self):
        # Save notes to db
        self.db.update_table(self.songname, self.notes)
        return
        
    def mouseclickEvent(self, event):
        target = self.ui.canvas.plotItem.vb.mapToView(event.pos())
        self.cursor.move_to_mouse(target, self.tab)
        self.ptr.setPos(*self.cursor.pos(self.tab))
        return
        
    def add_note(self, beatdiv, string, fret):
        textitem = pg.TextItem(text=str(fret), anchor=(0,0.5))
        
        beat = beatdiv/self.tab.beatdivs
        line, x = divmod(beat, self.tab.linebeats)
        y = string - line*self.tab.linewidth
        textitem.setPos(x, y)
        self.textitem_cnt.append(textitem)
        self.ui.canvas.addItem(textitem)
        
        return
        
    def keyPressEvent(self, signal):
        # Move cursor
        if qt.Key_Left <= signal.key() <= qt.Key_Down:
            if signal.key()==qt.Key_Left:
                self.cursor.move('left')
            elif signal.key()==qt.Key_Right:
                self.cursor.move('right')
            elif signal.key()==qt.Key_Up:
                self.cursor.move('up')
            elif signal.key()==qt.Key_Down:
                self.cursor.move('down')
            self.ptr.setPos(*self.cursor.pos(self.tab))
            
        # Change stepsize
        if signal.key()==qt.Key_Minus:
            self.cursor.change_stepsize('minus')
            self.update_displays()
        elif signal.key()==qt.Key_Equal:
            self.cursor.change_stepsize('plus')
            self.update_displays()
        
        # Add note
        if qt.Key_0 <= signal.key() <= qt.Key_9:
            if signal.modifiers() & qt.ControlModifier:
                fret = signal.key() - 38
            else:
                fret = signal.key() - 48

            note_exists, _ = self.cursor.check_if_played(self.notes)
            if not note_exists:
                self.add_note(self.cursor.beatdiv, self.cursor.string, fret)
                self.notes.loc[len(self.notes)] = [self.cursor.beatdiv,
                                               self.cursor.string,
                                               fret]
                self.play_note(self.cursor.string, fret)
                
        # Remove note
        if signal.key() == qt.Key_Backspace:
            note_exists, note_idx = self.cursor.check_if_played(self.notes)
            if note_exists:
                self.notes = self.notes.drop(labels=note_idx).reset_index(drop=True)
                self.ui.canvas.removeItem(self.textitem_cnt[note_idx])
                del self.textitem_cnt[note_idx]


    
if __name__=='__main__':
    if not qtw.QApplication.instance():
        app = qtw.QApplication(sys.argv)
    else:
        app = qtw.QApplication.instance()
    w = Main_Window()

    #app.exec_()


