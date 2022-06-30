# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import Frame
import simpleaudio as sa
from time import sleep
from svglib.svglib import svg2rlg
from PIL import Image,ImageTk
from reportlab.graphics import renderPDF, renderPM

""" Define classes for use with TranscriberApp.py"""
class SVG():
    def __init__(self):
        self.svg_list = []
        self.width = 0
        self.height = 0
        self.templates = self.__generate_templates()
        
    def __generate_templates(self):
        templates = {}
        templates["create"] = "<svg width='{}px' height='{}px' xmlns='http://www.w3.org/2000/svg' version='1.1' xmlns:xlink='http://www.w3.org/1999/xlink'>\n"
        templates["finalize"] = "</svg>"
        templates["circle"] = "    <circle stroke='{}' stroke-width='{}px' fill='{}' r='{}' cy='{}' cx='{}' />\n"
        templates["line"] = "    <line stroke='{}' stroke-width='{}px' y2='{}' x2='{}' y1='{}' x1='{}' />\n"
        templates["rectangle"] = "    <rect fill='{}' stroke='{}' stroke-width='{}px' width='{}' height='{}' y='{}' x='{}' ry='{}' rx='{}' />\n"
        templates["text"] = "    <text x='{}' y = '{}' font-size='{}px'>{}</text>\n"
        templates["ellipse"] = "    <ellipse cx='{}' cy='{}' rx='{}' ry='{}' fill='{}' stroke='{}' stroke-width='{}' />\n"
        return templates
    
    def __add_to_svg(self,text):
        self.svg_list.append(str(text))
        
    def create(self,width,height):
        self.width = width
        self.height = height
        self.svg_list.clear()
        self.__add_to_svg(self.templates["create"].format(width,height))
        
    def finalize(self):
        self.__add_to_svg(self.templates["finalize"])
        
    def fill(self,Fill):
        self.rectangle(self.width,self.height,0,0,Fill,Fill,0,0,0)
    
    def circle(self, stroke, strokewidth, fill, r, cx, cy):
        self.__add_to_svg(self.templates["circle"].format(stroke, strokewidth, fill, r, cy, cx))
        
    def text(self,rx,ry):
        self.__add_to_svg(self.templates["text"].format(rx,ry,12,'x'))

    def rectangle(self, width, height, x, y, fill, stroke, strokewidth, radiusx, radiusy):
        self.__add_to_svg(self.templates["rectangle"].format(fill, stroke, strokewidth, width, height, y, x, radiusy, radiusx))

    def line(self,stroke,width,y2,x2,y1,x1):
        self.__add_to_svg(self.templates['line'].format(stroke,width,y2,x2,y1,x1))
        
    def add_staff(self):
        # Need to complete
        self.fill('#A0A0A0')
        self.line('#555555',1,100,100,200,200)
        
        
        
    def save(self, path):
        self.__add_to_svg(self.templates["finalize"])
        f = open(path+'.svg', "w+")
        for idx in range(len(self.svg_list)):    
            f.write(str(self.svg_list[idx]))
        f.close()
        drawing = svg2rlg(path+'.svg')
        renderPM.drawToFile(drawing,path+'.png',fmt='PNG')


class Layout():
    """Contains tab layout information"""
    def __init__(self):
        self.lines_in_page = 8
        self.meas_in_line = 4
        self.staff_buffer = 4
        self.meas_buffer = 10
        self.dy = .1
        self.meas_in_page = self.meas_in_line*self.lines_in_page
        self.meas_width = self.meas_buffer+100
        self.line_height = 6+self.staff_buffer
        self.xmax = self.meas_width * self.meas_in_line
        self.ymax = 1 + self.lines_in_page*6 + (self.lines_in_page-1)*self.staff_buffer
        self.staff_start = [1+x*(6+self.staff_buffer) for x in np.arange(0,self.lines_in_page,1).tolist()]
        self.play_mode = 0;
        
        
        
class Song():
    """Contain song information"""
    def __init__(self,name='',bpm=4,BPM=120,capo=0,tuning=[0,0,0,0,0,0]):
        self.name = name
        self.bpm = bpm
        self.BPM = BPM
        self.capo = capo
        self.tuning = tuning
        self.open_notes = [24,19,15,10,5,0]
        self.curbeat = 0
        self.curmeas = 0
        self.curstr = 1
        self.stepsize = 0.5
        self.T = pd.DataFrame(columns = ['Measure','Beat','String','Fret','Time','NoteNum'])
        self.layout = Layout()
        self.play_mode = 0
        self.pressed_key = ''
        self.left_bracket=[]
        self.right_bracket=[]
        self.clipboard = pd.DataFrame(columns = ['Measure','Beat','String','Fret','Time','NoteNum'])
        self.clipboard_range = 0
        self.zorder = 3
        
    def reset_from_file(self):
        self.curbeat=0
        self.curmeas=0
        self.curstr=1
        self.stepsize=0.5
        self.play_mode=0
        self.pressed_key=''
        self.left_bracket=[]
        self.right_bracket=[]
        self.clipboard = pd.DataFrame(columns = ['Measure','Beat','String','Fret','Time','NoteNum'])
        self.clipboard_range = 0
        
        
    def get_curpage(self):
        return np.floor(self.curmeas/self.layout.meas_in_page)
    
    def get_page(self,measures):
        return [np.floor(measures[x]/self.layout.meas_in_page)for x in range(len(measures))]
        
    def get_curline(self):
        return np.mod(np.floor(self.curmeas/self.layout.meas_in_line),self.layout.lines_in_page)
    
    def get_line(self,measures):
        return [np.mod(np.floor(measures[x]/self.layout.meas_in_line),self.layout.lines_in_page) for x in range(len(measures))]
        
    def get_curblock(self):
        return np.mod(self.curmeas,self.layout.meas_in_line)
        
    def get_block(self,measures):
        return [np.mod(measures[x],self.layout.meas_in_line) for x in range(len(measures))]
        

    def get_xpix(self,blocks,beats):
        return [(self.layout.meas_buffer+blocks[x]*self.layout.meas_width)+(beats[x]/self.bpm*100) for x in range(len(beats))]
        
    def get_curxpix(self):
        return (self.layout.meas_buffer + self.get_curblock()*self.layout.meas_width) + (self.curbeat/self.bpm*100)
    
    
    def get_ypix(self,lines,strings):
        return [(self.layout.staff_start[int(lines[x])]) + (strings[x]-1)-self.layout.dy for x in range(len(strings))]
    
    def get_curypix(self):
        return (self.layout.staff_start[int( self.get_curline() )]) + (self.curstr-1)
    
    def clear_position(self):
        x0 = self.get_curxpix()
        y0 = self.get_curypix()
        plt.plot([x0+2,x0+4],[-1*y0,-1*y0],color=(1,1,1),linewidth=10,zorder=self.zorder)
        plt.plot([x0-2,x0+8],[-1*y0,-1*y0],'k-',zorder=self.zorder)
        self.increment_zorder()
        
    def increment_zorder(self):
        self.zorder +=1
        
    def plot_cursor(self,f):
        xtemp = (self.layout.meas_buffer + self.get_curblock()*self.layout.meas_width) + self.curbeat/self.bpm*100
        ytemp = self.layout.staff_start[round(self.get_curline())] + (self.curstr-1)
        f.cursor.set_x(xtemp)
        f.cursor.set_y(-1*ytemp)
        f.ax.draw_artist(f.cursor)
        
    def plot_arrow(self,f):
        xtemp = (self.layout.meas_buffer + self.get_curblock()*self.layout.meas_width) + self.curbeat/self.bpm*100
        ytemp = self.layout.staff_start[round(self.get_curline())] + 6
        f.arrow.set_x(xtemp)
        f.arrow.set_y(-1*ytemp)
        f.ax.draw_artist(f.arrow)
        
    def plot_bracket(self,f,side):
        DX = [0,-5,-5,0]
        DY = [1,1,-6,-6]
        if side=='left':
            if not self.left_bracket:
                return
            DX = [0,-5,-5,0]
            x0 = self.left_bracket['x']
            y0 = self.left_bracket['y']
        if side=='right':
            if not self.right_bracket:
                return
            DX = [-10,-5,-5,-10]
            x0 = self.right_bracket['x']
            y0 = self.right_bracket['y']
        
        (bracket,) = plt.plot([x0+x for x in DX],[-1*y0+y for y in DY],'k-',animated=True)
        f.ax.draw_artist(bracket)
        
        
    def play_note(self,curnotenum):
        sa.WaveObject.from_wave_file("Guitar Notes/Note"+str(curnotenum)+".wav").play()
        print('played note')
            
    def play_chord(self):
        try:
            boolvals = ((self.T.Measure==self.curmeas) & (self.T.Beat==self.curbeat)).tolist()
            idxs = [i for i,x in enumerate(boolvals) if x==True]
            for idx in idxs:
                sa.WaveObject.from_wave_file("Guitar Notes/Note"+str(self.T.NoteNum[idx])+".wav").play()
        except:
            pass #no notes to play
        
    def add_note_old(self,curfret):
        curnotenum = self.open_notes[self.curstr-1]+curfret+self.capo+self.tuning[self.curstr-1]
        if self.play_mode:
            self.play_note(curnotenum)
        
        Trow = pd.DataFrame( data={'Measure':[self.curmeas],'Beat':[self.curbeat],'String':[self.curstr],'Fret':[curfret],'Time':[0],'NoteNum':[curnotenum]})
        duplicates = ((self.T.Measure==self.curmeas) & (self.T.Beat==self.curbeat) & (self.T.String==self.curstr))
        if duplicates.any():
           self.T = self.T.drop(labels = duplicates.tolist().index(True))
        self.T=self.T.append(Trow, ignore_index=True)
    
    def add_note(self,f,curfret):
        curnotenum = self.open_notes[self.curstr-1]+curfret+self.capo+self.tuning[self.curstr-1]
        if self.play_mode:
            self.play_note(curnotenum)
    
        Trow = pd.DataFrame( data={'Measure':[self.curmeas],'Beat':[self.curbeat],'String':[self.curstr],'Fret':[curfret],'Time':[0],'NoteNum':[curnotenum]})
        duplicates = ((self.T.Measure==self.curmeas) & (self.T.Beat==self.curbeat) & (self.T.String==self.curstr))
        if duplicates.any():
           self.T = self.T.drop(labels = duplicates.tolist().index(True))
        self.T=self.T.append(Trow, ignore_index=True)
        
        self.clear_position()
        x0 = self.get_curxpix()
        y0 = self.get_curypix()
        if Trow.Fret[0]>=10:
            plt.plot([x0+2,x0+6],[-1*y0,-1*y0],color=(1,1,1),linewidth=4,zorder=self.zorder)
        else:
            plt.plot([x0+2,x0+4],[-1*y0,-1*y0],color=(1,1,1),linewidth=4,zorder=self.zorder)
        test=plt.text(x0,-1*y0-self.layout.dy,str(Trow.Fret[0]),va='center',zorder=self.zorder)
        f.ax.draw_artist(test)
        self.increment_zorder()
    
    
    def move_up(self):
        self.curstr = max([self.curstr-1,1])
        
    def move_down(self):
        self.curstr = min([self.curstr+1,6])
        
    def move_right(self):
        curpos = self.curmeas*self.bpm + self.curbeat
        curpos = curpos + self.stepsize
        self.curmeas = np.floor(curpos/self.bpm)
        self.curbeat = np.mod(curpos,self.bpm)
        if self.play_mode:
            self.play_chord()
        
    def move_left(self):
        curpos = self.curmeas*self.bpm + self.curbeat
        curpos = max([curpos - self.stepsize,0])
        self.curmeas = np.floor(curpos/self.bpm)
        self.curbeat = np.mod(curpos,self.bpm)
        if self.play_mode:
            self.play_chord()
            
    def toggle_play_mode(self):
        if self.play_mode:
            self.play_mode=0
        else:
            self.play_mode=1
        print(self.play_mode)
        
    def delete_note(self):
        current_notes = ((self.T.Measure==self.curmeas) & (self.T.Beat==self.curbeat) & (self.T.String==self.curstr))
        if current_notes.any():
            self.T = self.T.drop(labels = current_notes.tolist().index(True))
            self.T = self.T.reset_index(drop=True)
        
        
    def set_bracket(self,event,side):
        beat = np.round((np.mod(event.xdata,self.layout.meas_width)-self.layout.meas_buffer)*self.bpm/100)
        block = np.floor(event.xdata/self.layout.meas_width)
        line = np.floor(-1*event.ydata/self.layout.line_height)
        page = np.floor(self.curmeas/self.layout.meas_in_page)
        
        if beat==self.bpm:
            beat = 0
            block = block+1
            
        x0 = self.layout.meas_width*block + self.layout.meas_buffer + beat/self.bpm*100    
        y0 = self.layout.staff_start[int(line)]
        total_beat = beat + self.bpm*(block + line*self.layout.meas_in_line + page*self.layout.meas_in_page)
        
        if side=='left':
            self.left_bracket = {'x':x0, 'y':y0, 'total_beat':total_beat}
        if side=='right':
            self.right_bracket = {'x':x0,'y':y0,'total_beat':total_beat}
            
    def remove_brackets(self):
        self.left_bracket={}
        self.right_bracket={}
        
    def move_cursor(self,event):
        beat = np.round((np.mod(event.xdata,self.layout.meas_width)-self.layout.meas_buffer)*self.bpm/100)
        block = np.floor(event.xdata/self.layout.meas_width)
        line = np.floor(-1*event.ydata/self.layout.line_height)
        page = np.floor(self.curmeas/self.layout.meas_in_page)
        if beat==self.bpm:
            beat = 0
            block = block+1
        
        self.curmeas = block + line*self.layout.meas_in_line + page*self.layout.meas_in_page
        self.curbeat = beat
    
    def copy_to_clipboard(self):
        if not (self.left_bracket and self.right_bracket):
            print('Make a selection first.\n')
            return
        #breakpoint()
        self.clipboard = pd.DataFrame(columns = ['Measure','Beat','String','Fret','Time','NoteNum'])        
        for row in range(len(self.T)):
            total_beat = self.T.Measure[row]*self.bpm + self.T.Beat[row]
            if total_beat>=self.left_bracket['total_beat'] and total_beat<self.right_bracket['total_beat']:
                self.clipboard = self.clipboard.append(self.T.loc[row],ignore_index=True) 
        self.clipboard_range = self.right_bracket['total_beat'] - self.left_bracket['total_beat']
    
    def clear_clipboard(self):
        self.clipboard = pd.DataFrame(columns = ['Measure','Beat','String','Fret','Time','NoteNum'])

        
    def paste_from_clipboard(self):
        if self.clipboard.empty:
            print('Add to clipboard first')
            return
        
        min_total_beat = self.curmeas*self.bpm + self.curbeat
        max_total_beat = min_total_beat + self.clipboard_range
        
        for row in range(len(self.T)):
            total_beat = self.T.Measure[row]*self.bpm + self.T.Beat[row]
            if total_beat>=min_total_beat and total_beat<max_total_beat:
                self.T = self.T.drop(row)
        self.T = self.T.reset_index(drop=True)
        
        for row in range(len(self.clipboard)):
            total_beat = min_total_beat + self.clipboard.Measure[row]*self.bpm + self.clipboard.Beat[row]
            Trow = pd.DataFrame( data={'Measure':[np.floor(total_beat/self.bpm)],'Beat':[np.mod(total_beat,self.bpm)],'String':[self.clipboard.String[row]],'Fret':[self.clipboard.Fret[row]],'Time':[0],'NoteNum':[self.clipboard.NoteNum[row]]})
            self.T = self.T.append(Trow,ignore_index=True)
        
        self.remove_brackets()
        self.clear_clipboard()
    
    def delete_selection(self):
        if not (self.left_bracket and self.right_bracket):
            print('Select a range to delete first.\n')
            return
        
        for row in range(len(self.T)):
            total_beat = self.T.Measure[row]*self.bpm + self.T.Beat[row]
            if total_beat>=self.left_bracket['total_beat'] and total_beat<self.right_bracket['total_beat']:
                self.T = self.T.drop(row)
        self.T = self.T.reset_index(drop=True)
    
    
class TabFigure():
    """Creates figure for plotting tab"""
    def __init__(self,s):
        
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(10,14)
        plt.title(s.name)
        plt.xlim([0,s.layout.xmax])
        plt.ylim([-1*s.layout.ymax,0])
        plt.xticks([])
        plt.yticks([])
        plt.tight_layout()
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        # Define cursor and arrow
        self.cursor = plt.text(s.layout.meas_buffer,-1,'*',animated=True,va='center')
        self.arrow = plt.text(s.layout.meas_buffer,-7,'^',animated=True,va='center')
        
        # Plot staff lines
        xtemp   = np.tile([0,s.layout.xmax,0],[1,6]).tolist()[0] + np.tile(np.arange(0,s.layout.xmax+1,s.layout.meas_width).tolist(),[3,1]).transpose().reshape(1,-1).tolist()[0]
        ytemp   = np.tile( np.arange(0,6,1).tolist(),[3,1]).transpose().reshape(1,-1).tolist()[0] + np.tile([0,5,0],[1,s.layout.meas_in_line+1]).tolist()[0]
        for j in range(len(s.layout.staff_start)):
            plt.plot(xtemp,[-1*(x+s.layout.staff_start[j]) for x in ytemp],'k-')


            
class WindowFrames():
    """Hold left, center, and right frames for main window"""
    def __init__(self,frame):
        # Left and right frames
        self.lf = Frame(frame)
        self.lf.grid(row=0,column=0)
        self.cf = Frame(frame)
        self.cf.grid(row=0,column=1)
        self.rf = Frame(frame)
        self.rf.grid(row=0,column=2)
        
    
    
    