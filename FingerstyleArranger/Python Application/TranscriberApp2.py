# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 21:16:11 2021

@author: afish
"""

import simpleaudio as sa
from helper_classes2 import Song, Layout, TabFigure, WindowFrames, SVG
from tkinter import Toplevel,Label,Entry,Button,Tk,Frame,Canvas,StringVar,OptionMenu
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from os.path import exists
import os
from time import sleep
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pickle
from matplotlib.animation import ArtistAnimation
from time import sleep
from PIL import Image,ImageTk
# Read in py file of functions

'''
#### Thoughts ####

# Add delete_notes_in_range method to remove notes in total_beats range
# helpful to simplify?

# Add message readout in right_frame

# Plot beatlines
# related: name of artist doesn"t matter, it is drawn to f immediately, so it can be called anything

# Add save button

# Add change song option

# Use widget.destory() to remove a widget


'''
#sa.WaveObject.from_wave_file("Guitar Notes/Note7.wav").play()






def set_stepsize(s,frame,new_stepsize):
    s.stepsize = new_stepsize
    update_readouts(s,frame)
    return
    
def update_readouts(s,frame):
    Label(frame,text='Measure:',width=10).grid(row=0,column=0)
    measure_entry = Entry(frame,width=5)
    measure_entry.grid(row=0,column=1)
    measure_entry.insert([0],str(s.curmeas))
    
    Label(frame,text='Beat:',width=10).grid(row=1,column=0)
    beat_entry = Entry(frame,width=5)
    beat_entry.grid(row=1,column=1)
    beat_entry.insert([0],str(s.curbeat))
    
    Label(frame,text='String:',width=10).grid(row=2,column=0)
    string_entry = Entry(frame,width=5)
    string_entry.grid(row=2,column=1)
    string_entry.insert([0],str(s.curstr))
    
    Label(frame,text='Stepsize:',width=10).grid(row=3,column=0)
    stepsize_entry = Entry(frame,width=5)
    stepsize_entry.grid(row=3,column=1)
    stepsize_entry.insert([0],str(s.stepsize))

def plotbgnotes(f,s):
    Npage = s.get_page(s.T.Measure)
    Nline = s.get_line(s.T.Measure)
    Nblock = s.get_block(s.T.Measure)
    Nx = s.get_xpix(Nblock,s.T.Beat)
    Ny = s.get_ypix(Nline,s.T.String)
    curpage = s.get_curpage()
    curline = s.get_curline()
    bg_notes = []
    bg_whites = []
    for j in range(len(s.T)):
        if Npage[j]==curpage and Nline[j]!=curline:
            if s.T.Fret[j]>=10:
                Nxwhite = [Nx[j]+1,Nx[j]+6]
                Nywhite = [-1*Ny[j]-s.layout.dy,-1*Ny[j]-s.layout.dy]
            else:
                Nxwhite = [Nx[j]+1,Nx[j]+3.5]
                Nywhite = [-1*Ny[j]-s.layout.dy,-1*Ny[j]-s.layout.dy]
            bg_whites.append(plt.plot(Nxwhite,Nywhite,color=(1,1,1),linewidth=4)[0])
            f.ax.draw_artist(bg_whites[-1])
            bg_notes.append(plt.text(Nx[j],-1*Ny[j],str(s.T.Fret[j]),va='center',color='red'))
            f.ax.draw_artist(bg_notes[-1])
    test=plt.text(10,-10,'test',va='center',color='red')
    f.ax.draw_artist(test)
    pass
    
def plotfgnotes(f,s):
    Npage = s.get_page(s.T.Measure)
    Nline = s.get_line(s.T.Measure)
    Nblock = s.get_block(s.T.Measure)
    Nx = s.get_xpix(Nblock,s.T.Beat)
    Ny = s.get_ypix(Nline,s.T.String)
    curpage = s.get_curpage()
    curline = s.get_curline()
    fg_notes = []
    fg_whites = []
    for j in range(len(s.T)):
        if Npage[j]==curpage and Nline[j]==curline:
            if s.T.Fret[j]>=10:
                Nxwhite = [Nx[j]+1,Nx[j]+6]
                Nywhite = [-1*Ny[j]-s.layout.dy,-1*Ny[j]-s.layout.dy]
            else:
                Nxwhite = [Nx[j]+1,Nx[j]+3.5]
                Nywhite = [-1*Ny[j]-s.layout.dy,-1*Ny[j]-s.layout.dy]
            fg_whites.append(plt.plot(Nxwhite,Nywhite,animated=True,color=(1,1,1),linewidth=4)[0])
            f.ax.draw_artist(fg_whites[-1])
            fg_notes.append(plt.text(Nx[j],-1*Ny[j],str(s.T.Fret[j]),animated=True,va='center'))
            f.ax.draw_artist(fg_notes[-1])
    

def plotartists(f,s):
    f.figarea.flush_events()
    f.figarea.draw()
    f.bg = f.figarea.copy_from_bbox(f.fig.bbox)
    f.figarea.flush_events()
    f.figarea.restore_region(f.bg)
    
    s.plot_cursor(f)
    s.plot_arrow(f)
    s.plot_bracket(f,'left')
    s.plot_bracket(f,'right')
    #plotbeatlines
    #plotfgnotes(f,s)
    f.figarea.blit(f.fig.bbox)
    f.figarea.flush_events()
    sleep(.001)
    
def definebg(f,s):
    #f.reset_figure(s)
    #f.figarea.draw()
    #f.figarea.restore_region(f.bg0)
    #f.figarea.draw()
    #f.figarea.flush_events()
    #plotbgnotes(f,s)    # Add notes on same page, not same line
    #f.figarea.flush_events()
    #f.figarea.draw()
    #f.bg = f.figarea.copy_from_bbox(f.fig.bbox)
    #f.figarea.flush_events()
    #return f
    pass

def key_press(event,f,s,w):
    s.pressed_key = event.key
    curline = s.get_curline()
    
    
    try:
        s.add_note(f,int(event.key))
    except:
        if event.key=='p':
            s.add_note(10)
        if event.key=='q':
            s.add_note(11)
        if event.key=='w':
            s.add_note(12)
        if event.key=='e':
            s.add_note(13)
        if event.key=='r':
            s.add_note(14)
    if event.key == 'up':
        s.move_up()
    if event.key == 'down':
        s.move_down()
    if event.key == 'right':
        s.move_right()
    if event.key == 'left':
        s.move_left()
    if event.key == 'l':
        s.toggle_play_mode()
    if event.key == 'backspace':
        s.delete_note()
    if event.key == 'c':
        s.copy_to_clipboard()
    if event.key == 'v':
        s.paste_from_clipboard()
    if event.key == 'delete':
        s.delete_selection()
        #definebg(f,s)
        
        
    update_readouts(s, w)
    #if curline!=s.get_curline():
        #f.figarea.flush_events()
        #f.figarea.restore_region(f.bg0)
        #definebg(f,s);
        #f.figarea.flush_events()
        
    #f.fig.canvas.restore_region(f.bg)
    plotartists(f,s)

def mouse_press(event,f,s,w):
    if s.pressed_key=='s':
        s.set_bracket(event,'left')
    elif s.pressed_key=='j':
        curline = s.get_curline()
        s.move_cursor(event)
        if curline!=s.get_curline():
            definebg(f,s)
    else:
        s.remove_brackets()
        
    f.fig.canvas.restore_region(f.bg)
    plotartists(f, s)
    
def mouse_release(event,f,s,w):
    if s.pressed_key=='s':
        s.set_bracket(event,'right')
    else:
        s.remove_brackets()
        
    f.fig.canvas.restore_region(f.bg)
    plotartists(f,s)
    
def key_release(event,f,s,w):
    s.pressed_key = ''

def get_songlist():
    songlist = []
    #Search for pickle files
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for root,dirs,files in os.walk(dir_path):
        for file in files:
            if file.endswith('.pickle'):
                songlist.append(file[0:-7]) #remove .pickle ending
    return songlist
    

class MainApplication():
    def __init__(self,root):
        self.s = Song()
        self.svg = SVG()
        self.root = root
        self.width = 0.5*root.winfo_screenwidth()
        self.height = 0.7*root.winfo_screenheight()
        self.root.geometry('%dx%d' % (self.width,self.height))
    
        self.root.configure(background='grey')
        self.main_win()
        
    
    def refresh_root(self):
        self.L['song_name'].configure(text='Song: '+self.s.name)
        self.M['songlist'].destroy()
        self.B['load_song'].destroy()

        songlist = get_songlist() #list of saved songs
        if songlist:
            self.cursong = StringVar(root)
            self.cursong.set(songlist[0])
            self.B['load_song'] = Button(self.F['left'],command=self.unpickle_song,text='Load Song');
            self.B['load_song'].grid(row=2,column=0)
            self.M['songlist'] = OptionMenu(self.F['left'],self.cursong,*songlist)
            self.M['songlist'].grid(row=3,column=0)
            
    def create_song(self):
            self.s = Song(self.E['song_name'].get(),int(self.E['bpm'].get()),int(self.E['BPM'].get()),int(self.E['capo'].get()),[0,0,0,0,0,0])
            self.pickle_song()
            self.refresh_root()
            
    def pickle_song(self):
            pickle.dump(self.s,open(self.E['song_name'].get()+'.pickle','wb'))
            print('Created '+self.E['song_name'].get()+'.pickle')
            self.initwin.destroy()
            
    def unpickle_song(self):
        ## Read in data from picklefile
        self.s = pickle.load(open(self.cursong.get()+'.pickle','rb'))
        print('Loaded '+self.cursong.get()+'.pickle')
        self.refresh_root()
        self.s.reset_from_file()

    def update_canvas(self):
        self.F['center'].update()
        self.svg.create(self.F['center'].winfo_width()*.9,self.F['center'].winfo_height()*.9)
        self.svg.add_staff()
        self.svg.save(self.s.name)
        self.img = ImageTk.PhotoImage(Image.open(self.s.name+'.png'))
        self.canvas.create_image(self.F['center'].winfo_width()/2,self.F['center'].winfo_height()/2,image=self.img)

        
    def init_win(self):
        ## Creates window for user to input data and create song matfile
        # Add menus so inputs are valid
        self.initwin = Toplevel(root)
        self.initwin.title('Initialize Song')
        self.initwin.geometry("200x100")
        Label(self.initwin,width=10,text="Song Name").grid(row=0,column=0)
        Label(self.initwin,width=10,text="Beats/Measure").grid(row=1,column=0)
        Label(self.initwin,width=10,text="Tempo (BPM)").grid(row=2,column=0)
        Label(self.initwin,width=10,text="Capo Position").grid(row=3,column=0)
        self.E = {}
        self.E['song_name'] = Entry(self.initwin,width=10)
        self.E['song_name'].grid(row=0,column=1)
        self.E['song_name'].insert(0,'default_songname')
        self.E['bpm']   = Entry(self.initwin,width=10)
        self.E['bpm'].grid(row=1,column=1)
        self.E['bpm'].insert(0,4)
        self.E['BPM']   = Entry(self.initwin,width=10)
        self.E['BPM'].grid(row=2,column=1)
        self.E['BPM'].insert(0,100)
        self.E['capo'] = Entry(self.initwin,width=10)
        self.E['capo'].grid(row=3,column=1)
        self.E['capo'].insert(0,0)
        Button(self.initwin,command=self.create_song,text='Initialize').grid(row=4,column=0,columnspan=2)
        return
    
    def main_win(self):
        # create frames
        frame = Frame(self.root).grid() 
        self.F = {}
        self.B = {}
        self.M = {}
        self.L = {}
        self.F['left'] = Frame(frame,width=.25*self.width,height=self.height)
        self.F['left'].grid(row=0,column=0)
        self.F['center'] = Frame(frame,width=.5*self.width,height=self.height)
        self.F['center'].grid(row=0,column=1)
        self.F['right'] = Frame(frame,width=.25*self.width,height=self.height)
        self.F['right'].grid(row=0,column=2)

        # New song
        Button(self.F['left'],command=self.init_win,text='New Song').grid(row=1,column=0)
        
        # Button to load old song
        songlist = get_songlist() #list of saved songs
        if songlist:
            self.cursong = StringVar(root)
            self.cursong.set(songlist[0])
            self.B['load_song'] = Button(self.F['left'],command=self.unpickle_song,text='Load Song');
            self.B['load_song'].grid(row=2,column=0)
            self.M['songlist'] = OptionMenu(self.F['left'],self.cursong,*songlist)
            self.M['songlist'].grid(row=3,column=0)
        
        # Song name
        self.L['song_name'] = Label(self.F['left'],text='Song: '+self.s.name,width=20)
        self.L['song_name'].grid(row=0,column=0)
        
        # Readouts
        update_readouts(self.s,self.F['right'])
            
        # Stepsize options
        Label(self.F['left'],text="Select Stepsize",width=20).grid(row=4,column=0)
        Button(self.F['left'],text='Sixteenth',command=lambda: set_stepsize(self.s,self.F['right'],0.25)).grid(row=5,column=0)
        Button(self.F['left'],text='Triplet',command=lambda: set_stepsize(self.s,self.F['right'],1/3)).grid(row=5,column=1)
        Button(self.F['left'],text='Eighth',command=lambda: set_stepsize(self.s,self.F['right'],0.5)).grid(row=6,column=0)
        Button(self.F['left'],text='Quarter',command=lambda: set_stepsize(self.s,self.F['right'],1)).grid(row=6,column=1)
        
        # Canvas
        self.img = ImageTk.PhotoImage(Image.open('test.png'))
        self.F['center'].update()
        self.canvas = Canvas(self.F['center'],width=self.F['center'].winfo_width(),height=self.F['center'].winfo_height())
        self.canvas.grid(row=1,column=0)
        #self.L['title']=Label(self.F['center'],width=50,height=100,text=self.s.name )
        #self.L['title'].grid(row=0,column=0)
        self.update_canvas()

        
        def closeapp():
            """Save Data before closing application"""
            if self.s.name:
                pickle.dump(self.s,open(self.s.name+'.pickle','wb'))
                print('saved '+self.s.name)
            else:
                print('No data to save')
            root.destroy()
            return
        root.protocol("WM_DELETE_WINDOW",closeapp)



if __name__ == "__main__":
    root = Tk()
    MainApplication(root)
    root.mainloop()

