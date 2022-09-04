# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 19:48:47 2022

@author: afish
"""

import sys
sys.path.append('C:\\Users\\afish\\Documents\\GitHub\\Guitar\\PythonArranger\\GUIPackages')
import pandas as pd
import numpy as np
from Transcriber import Database, Cursor, Tab
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5.Qt import Qt as qt
from PyQt5 import uic
import pyqtgraph as pg
from sqlalchemy import create_engine
import sounddevice as sd
import soundfile as sf
from scipy.interpolate import interp1d


# =============================================================================
# Add print.py to tab class
# Add full playback from cursor with termination...
# Move plotting of staff to main_window, return reference points from Tab
# Add a songname label, useful to keep the name around
# Possibility to rename table?
# =============================================================================



mw_Ui, mw_Base = uic.loadUiType('load_window.ui')
class Load_Window(mw_Base, mw_Ui):
    ''' This class controls the "load/create song" window. '''
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.main_window.hide()

        # Load or create song
        self.setupUi(self)
        
        # Load song menu using database tables
        song_tables = self.main_window.db.get_tables()
        self.existingSongsComboBox.addItems(song_tables)
        
        # Button functions
        self.createButton.clicked.connect(self.create_song)
        self.loadButton.clicked.connect(self.load_song)
        
        
    def load_song(self):
        ''' Load song from the database. '''
        # Get data from table and update notes
        table_name = self.existingSongsComboBox.currentText()
        if table_name!='':
            self.main_window.load_notes(table_name)
            self.main_window.songname = table_name
            self.main_window.songNameLineEdit.setText(self.main_window.songname)
            self.main_window.show()
            self.close()
        return
    
    def create_song(self):
        ''' Create a new song. '''
        songname = self.newSongLineEdit.text().lower().replace(' ','_')
        
        if songname in self.main_window.db.get_tables() or songname=='':
            msg = qtw.QMessageBox()
            msg.setText('Song Table already exists.')
            msg.exec_()
        else:
            self.main_window.db.create_table(songname)
            self.main_window.songname = songname
            self.main_window.songNameLineEdit.setText(songname)
            self.main_window.show()
            self.close()
        return
        

mw_Ui, mw_Base = uic.loadUiType('main_window.ui')
class Main_Window(mw_Base, mw_Ui):
    ''' This class controls the main window for transcribing guitar tabs. '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Define structures
        self.songname = ''
        self.notes = pd.DataFrame(columns=['beatdiv','string','fret'], dtype=int)
        self.cursor = Cursor()
        self.tab = Tab()
        self.db = Database()
        
        # Import Layout
        self.setupUi(self)

        # Create figure
        self.canvas.plot()
        self.tab.add_staff(self.canvas)
        
        # Initialize Displays
        self.stepsizeLineEdit.setText(f'1/{int(96/self.cursor.step)}')
        self.playback_bpm = round(float(self.playbackSpeedLineEdit.text()))
        self.play_tones = self.soundToggleCheckBox.isChecked()

        # Add cursor ptr
        self.ptr = pg.TextItem(text='*', anchor=(0.25,0.25), color=self.tab.textitem_color)
        self.ptr.setPos(*self.cursor.get_canvas_coords(self.tab))
        self.canvas.addItem(self.ptr)
        self.textitem_cnt = []
        
        # Connect signals to slots
        self.canvas.scene().sigMouseClicked.connect(self.mouseClickEvent)
        self.saveButton.clicked.connect(self.save_song)
        self.soundToggleCheckBox.toggled.connect(self.toggle_sounds)
        

        # Run Loading window
        self.load_window = Load_Window(self)
        self.load_window.show()
        
    
    def playback(self):
        ''' Playback the song starting at the cursor. '''
        # Start playing the song from the cursor location.
        # Have a way to stop
        pass
        return
        
    def toggle_sounds(self):
        ''' Toggle tone sound effects. '''
        print('Toggled sounds')
        self.play_tones = self.soundToggleCheckBox.isChecked()
        
    def play_note(self, string, fret):
        ''' Play the tone for a given pitch. '''
        if self.play_tones:
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

        
    def load_notes(self, table_name):
        ''' Load notes from the database into the notes dataframe and canvas. '''
        for index, row in self.db.load_table(table_name).iterrows():
            self.add_note(row.fret, row.beatdiv, row.string)
        self.set_figure_view()
        return
        
    def save_song(self):
        ''' Save the song to the database. '''
        # Save notes to db
        self.db.update_table(self.songname, self.notes)
        return
        
    def mouseClickEvent(self, event):
        ''' Control mouse clicks on the canvas. '''
        target = self.canvas.plotItem.vb.mapToView(event.pos())
        self.cursor.mousemove(target, self.tab)
        self.ptr.setPos(*self.cursor.get_canvas_coords(self.tab))
        
        self.setFocus() # Needed so certain keyPresses work after clicking canvas
        return
        
    def add_note(self, fret, beatdiv=None, string=None):
        ''' Add a note to the notes dataframe and canvas. '''
        if beatdiv is None:
            beatdiv = self.cursor.beatdiv
        if string is None:
            string = self.cursor.string
            
        textitem = pg.TextItem(text=str(fret), anchor=(0,0.5), color=self.tab.textitem_color)
        beat = beatdiv/self.tab.beatdivs
        line, x = divmod(beat, self.tab.linebeats)
        y = string - line*self.tab.linewidth
        textitem.setPos(x, y)
        self.textitem_cnt.append(textitem)
        self.canvas.addItem(textitem)
        
        self.notes.loc[len(self.notes)] = [beatdiv, string, fret]
        return
        
    def redraw(self, notes):
        for idx in notes.index:
            beat = notes.loc[idx].beatdiv/self.tab.beatdivs
            line, x = divmod(beat, self.tab.linebeats)
            y = notes.loc[idx].string - line*self.tab.linewidth
            self.textitem_cnt[idx].setPos(x,y)
        return
    
    
    
    def remove_notes(self, matches):
        ''' Remove notes from the notes dataframe and canvas. '''
        idxs = matches.index.sort_values(ascending=False)
        for idx in idxs:
            self.notes = self.notes.drop(labels=idx).reset_index(drop=True)
            self.canvas.removeItem(self.textitem_cnt[idx])
            del self.textitem_cnt[idx]
        return
            

    def set_figure_view(self, page=0):
        ''' Change figure view of canvas as function of page number. '''
        self.canvas.setXRange(*self.tab.xlimits(page))
        self.canvas.setYRange(*self.tab.ylimits(page))
        return
            
    def get_notes(self, column_conditions):
        ''' Get subset of notes that satisfy column_conditions as specified
        by an input dictionary where keys are column names and values are 
        scalars (check for equivalence) or 2 element lists (check for containment). '''
        matches = self.notes.beatdiv>=0 #Initialize all true
        for col, cond in column_conditions.items():
            if isinstance(cond, list):
                matches = matches & self.notes[col].between(cond[0], cond[1]-.1)
            else:
                matches = matches & (self.notes[col]==cond)
        return self.notes[matches]
        
        
    def keyPressEvent(self, signal):
        ''' Control keystroke events. '''
        cursor_keys = [qt.Key_Left, qt.Key_Right, qt.Key_Down, qt.Key_Up,
                       qt.Key_PageUp, qt.Key_PageDown]
        if signal.key() in cursor_keys:
            if signal.modifiers() & qt.ControlModifier:
                # Shift and redraw later notes
                cond = self.notes.beatdiv<self.cursor.beatdiv
                if signal.key()==qt.Key_Left:
                    self.notes.beatdiv = self.notes.beatdiv.where(cond, self.notes.beatdiv-self.cursor.step)
                    self.redraw(self.notes[~cond])

                if signal.key()==qt.Key_Right:
                    self.notes.beatdiv = self.notes.beatdiv.where(cond, self.notes.beatdiv+self.cursor.step)
                    self.redraw(self.notes[~cond])
            else:
                # Move cursor
                self.cursor.keymove(signal.key(), self.tab)
                self.ptr.setPos(*self.cursor.get_canvas_coords(self.tab))
    
                page = self.cursor.beatdiv // self.tab.pagedivs
                self.set_figure_view(page)


        # Change stepsize
        if signal.key() in [qt.Key_Minus, qt.Key_Equal]:
            self.cursor.change_stepsize(signal.key())
            self.stepsizeLineEdit.setText(f'1/{int(96/self.cursor.step)}')
        
        # Add notes
        if qt.Key_0 <= signal.key() <= qt.Key_9:
            if signal.modifiers() & qt.ControlModifier:
                fret = signal.key() - 38
            else:
                fret = signal.key() - 48

            matches = self.get_notes({'string':self.cursor.string,
                                      'beatdiv':self.cursor.beatdiv})
            if len(matches)==0:
                self.add_note(fret)
                self.play_note(self.cursor.string, fret)
                
        # Remove notes
        if signal.key() == qt.Key_Backspace:
            matches = self.get_notes({'string':self.cursor.string,
                                      'beatdiv':self.cursor.beatdiv})
            self.remove_notes(matches)
            
        if signal.key() == qt.Key_Delete:
            measure = self.cursor.beatdiv // self.tab.measuredivs
            beatdiv_range = np.array([measure, measure+1]) * self.tab.measuredivs
            matches = self.get_notes({'beatdiv':beatdiv_range.tolist()})
            self.remove_notes(matches)
        
        # Copy
        if signal.key()==qt.Key_C and (signal.modifiers() & qt.ControlModifier):
            measure = self.cursor.beatdiv // self.tab.measuredivs
            beatdiv_min = measure*self.tab.measuredivs
            beatdiv_max = (measure+self.measuresToSelectSpinBox.value())*self.tab.measuredivs
            self.clipboard = self.get_notes({'beatdiv':[beatdiv_min, beatdiv_max]})
        
        # Paste
        if signal.key()==qt.Key_V and (signal.modifiers() & qt.ControlModifier):
            # Remove notes in paste region
            measure = self.cursor.beatdiv // self.tab.measuredivs
            beatdiv_min = measure*self.tab.measuredivs
            beatdiv_max = (measure+self.measuresToSelectSpinBox.value())*self.tab.measuredivs
            matches = self.get_notes({'beatdiv':[beatdiv_min, beatdiv_max]})
            self.remove_notes(matches)
            
            # Add new notes
            for index, row in self.clipboard.iterrows():
                self.add_note(row.fret, 
                              beatdiv=(beatdiv_min+row.beatdiv), 
                              string=row.string)
            
            
if __name__=='__main__':
    ''' Run application. Uncomment app.exec_() for troubleshooting. '''
    if not qtw.QApplication.instance():
        app = qtw.QApplication(sys.argv)
    else:
        app = qtw.QApplication.instance()
    w = Main_Window()

    # app.exec_()


