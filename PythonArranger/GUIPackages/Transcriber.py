# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 20:06:05 2022

@author: afisher
"""


import pandas as pd
import numpy as np
import pyqtgraph as pg
import mysql.connector
from sqlalchemy import create_engine
from PyQt5.Qt import Qt as qt

class Database():
    def __init__(self):
        ''' This class interfaces with the mysql "guitar" database. '''
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
        ''' Return a list of databases. '''
        self.execute('show databases')
        databases = [database[0] for database in self.cursor]
        return databases
    
    def get_tables(self):
        ''' Return a list of tables. '''
        self.execute('show tables')
        tables = [table[0] for table in self.cursor]
        return tables
        
    def create_table(self, table_name):
        ''' Create a song table. '''
        command = f'create table {table_name} (beatdiv int, string int, fret int);'
        self.execute(command)
        return
        
    def load_table(self, table_name):
        ''' Load song information from requested table. '''
        command = f'select * from guitar.{table_name}'
        notes = pd.read_sql(command, self.conn)
        return notes.astype(int)
        
    def update_table(self, songname, notes):
        ''' Update song table with new dataframe. '''
        notes = notes.astype(int)
        self.execute(f'truncate {songname}')
        notes.to_sql(songname, self.engine, if_exists='replace', index=False)
        print(f'Updated {songname}')
        return
    
    def close(self):
        self.conn.close()
        return
    
class Tab():
    ''' This class contains parameters for formatting the tabs. '''
    def __init__(self):
        self.measurebeats = 4
        self.beatdivs = 96 # divisions in a beat
        self.tempo = 120
        self.capo = 0
        self.tuning = np.zeros(6)
        self.pagelines = 8
        self.linemeasures = 3
        self.staffspacing = 4
        self.textitem_color = np.ones(3)*255
        self.staffline_color = np.ones(3)*120
        self.beatline_color = np.ones(3)*30

        self.linewidth = 5+self.staffspacing
        self.linebeats = self.linemeasures * self.measurebeats  
        self.linedivs = self.linebeats * self.beatdivs
        self.pagedivs = self.pagelines * self.linedivs
        self.measuredivs = self.measurebeats * self.beatdivs
        self.page_width = self.linebeats
        self.page_height = self.pagelines*self.linewidth

    def xlimits(self, page=0):
        ''' Return xlimits for current page. '''
        return (0, self.page_width)
    
    def ylimits(self, page=0):
        ''' Return ylimits for current page. '''
        return (-self.page_height*(page+1), -self.page_height*(page))
        
    def add_staff(self, canvas):
        ''' This function is awkward. All to ask for reference points but
        the plotting should be done in the main window. '''
        stafflines_x = np.append(np.tile([0,self.linebeats,0],6),
                                  np.repeat(self.measurebeats*np.arange(self.linemeasures+1),3))
        stafflines_y = np.append(np.repeat(range(6),3),
                                  np.tile([0,5,0],self.linemeasures+1))*-1
        
        beatlines_x = np.repeat(np.arange(self.linebeats), 3)
        beatlines_y = np.tile([0,5,0], self.linebeats)*-1
        
        for j in range(50):
            beatlines = pg.PlotDataItem(beatlines_x,
                                    beatlines_y - j*self.linewidth,
                                    pen=(self.beatline_color))
            canvas.addItem(beatlines)
            
            stafflines = pg.PlotDataItem(stafflines_x, 
                                         stafflines_y - j*self.linewidth,
                                         pen=(self.staffline_color))
            canvas.addItem(stafflines)
        
        def printpdf(self):
            ''' Function to print quality tab. '''
            pass
            return
        
        return
        

class Cursor():
    ''' This class is for the cursor used to interact with the main canvas. '''
    def __init__(self):
        self.beatdiv = 0
        self.string = 0
        self.step = 48
        self.stepsizes = [96, 48, 32, 24, 16, 12, 6]
        
    def get_canvas_coords(self, tab):
        ''' Return the cursor location in x,y canvas coordinates. '''
        beat = self.beatdiv/tab.beatdivs
        line, x = divmod(beat, tab.linebeats)
        y = self.string - line*tab.linewidth
        return x, y
    
    def keymove(self, key, tab):
        ''' Move the cursor according to key input. '''
        if key==qt.Key_Up:
            self.string = min(self.string+1, 0)
        elif key==qt.Key_Down:
            self.string = max(self.string-1, -5)
        elif key==qt.Key_Right:
            self.beatdiv = self.beatdiv + self.step
        elif key==qt.Key_Left:
            self.beatdiv = max(self.beatdiv-self.step, 0)
        elif key==qt.Key_PageUp:
            self.beatdiv = max(self.beatdiv-tab.linedivs,0) # need access to linedivs
        elif key==qt.Key_PageDown:
            self.beatdiv = self.beatdiv + tab.linedivs
        return
    
    def mousemove(self, target, tab):
        ''' Move the cursor according to mouse input. '''
        line, string = divmod(target.y(), -tab.linewidth)
        self.beatdiv = round(target.x())*tab.beatdivs + line*tab.linedivs
        self.string = round(np.clip(string, -5, 0))
        return
    
    def change_stepsize(self, key):
        ''' Change the cursor stepsize according to key input. '''
        idx = self.stepsizes.index(self.step)
        if key==qt.Key_Equal:
            idx = min(idx+1, len(self.stepsizes)-1)
        elif key==qt.Key_Minus:
            idx = max(idx-1, 0)
        self.step = self.stepsizes[idx]
        return
            