# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 21:16:11 2021

@author: afish
"""

import simpleaudio as sa
from helper_classes import Song, Layout, TabFigure, WindowFrames
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



'''
#sa.WaveObject.from_wave_file("Guitar Notes/Note7.wav").play()

def initialize_song():
    ## Creates window for user to input data and create song matfile
    # Add menus so inputs are valid
    
    def create_song():
        s = Song(name_entry.get(),int(bpm_entry.get()),int(BPM_entry.get()),int(capo_entry.get()),[0,0,0,0,0,0])
        pickle_song(s)
    def pickle_song(s):
        pickle.dump(s,open(name_entry.get()+'.pickle','wb'))
        print('Created '+name_entry.get()+'.pickle')
        initwin.destroy()
        resetroot(s)
        return s

    initwin = Toplevel(root)
    initwin.title('Initialize Song')
    initwin.geometry("200x100")
    Label(initwin,width=10,text="Song Name").grid(row=0,column=0)
    Label(initwin,width=10,text="Beats/Measure").grid(row=1,column=0)
    Label(initwin,width=10,text="Tempo (BPM)").grid(row=2,column=0)
    Label(initwin,width=10,text="Capo Position").grid(row=3,column=0)
    name_entry  = Entry(initwin,width=10)
    name_entry.grid(row=0,column=1)
    name_entry.insert(0,'default_songname')
    bpm_entry   = Entry(initwin,width=10)
    bpm_entry.grid(row=1,column=1)
    bpm_entry.insert(0,4)
    BPM_entry   = Entry(initwin,width=10)
    BPM_entry.grid(row=2,column=1)
    BPM_entry.insert(0,100)
    capo_entry = Entry(initwin,width=10)
    capo_entry.grid(row=3,column=1)
    capo_entry.insert(0,0)
    Button(initwin,command=create_song,text='Initialize').grid(row=4,column=0,columnspan=2)
    return


def unpickle_song():
    ## Read in data from picklefile
    s = pickle.load(open(cursong.get()+'.pickle','rb'))
    print('Loaded '+cursong.get()+'.pickle')
    s.reset_from_file()
    resetroot(s)
    return s

def set_stepsize(s,w,new_stepsize):
    s.stepsize = new_stepsize
    update_readouts(s,w)
    return
    
def update_readouts(s, w):
    Label(w.right_frame,text='Measure:',width=10).grid(row=0,column=0)
    measure_entry = Entry(w.right_frame,width=5)
    measure_entry.grid(row=0,column=1)
    measure_entry.insert([0],str(s.curmeas))
    
    Label(w.right_frame,text='Beat:',width=10).grid(row=1,column=0)
    beat_entry = Entry(w.right_frame,width=5)
    beat_entry.grid(row=1,column=1)
    beat_entry.insert([0],str(s.curbeat))
    
    Label(w.right_frame,text='String:',width=10).grid(row=2,column=0)
    string_entry = Entry(w.right_frame,width=5)
    string_entry.grid(row=2,column=1)
    string_entry.insert([0],str(s.curstr))
    
    Label(w.right_frame,text='Stepsize:',width=10).grid(row=3,column=0)
    stepsize_entry = Entry(w.right_frame,width=5)
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
    
def resetroot(s):
    frame = Frame(root).grid() 
    w   = WindowFrames(frame)
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry('%dx%d' % (width*.7,height))
    
    ### Left frame
    # Songname
    Label(w.left_frame,text='Song: '+s.name,width=20).grid(row=0,column=0)
    
    ### Right frame
    update_readouts(s, w)
        
    # Change stepsize
    Label(w.left_frame,text="Select Stepsize",width=20).grid(row=4,column=0)
    Button(w.left_frame,text='Sixteenth',command=lambda: set_stepsize(s,w,0.25)).grid(row=5,column=0)
    Button(w.left_frame,text='Triplet',command=lambda: set_stepsize(s,w,1/3)).grid(row=5,column=1)
    Button(w.left_frame,text='Eighth',command=lambda: set_stepsize(s,w,0.5)).grid(row=6,column=0)
    Button(w.left_frame,text='Quarter',command=lambda: set_stepsize(s,w,1)).grid(row=6,column=1)
    
    
    #### Populate CenterFrame
    f = TabFigure(s)
    
    # Create FigureCanvas, connect to callback 
    f.figarea = FigureCanvasTkAgg(f.fig, master=root)
    f.figarea.get_tk_widget().grid(row=0,column=1)
    f.figarea.get_tk_widget().focus_set()
    f.figarea.mpl_connect('button_press_event',lambda event: mouse_press(event,f,s,w))
    f.figarea.mpl_connect('button_release_event',lambda event: mouse_release(event,f,s,w))
    f.figarea.mpl_connect('key_release_event',lambda event: key_release(event,f,s,w))
    f.figarea.mpl_connect('key_press_event',lambda event: key_press(event,f,s,w))
    f.figarea.draw()
    f.figarea.flush_events()
    f.bg = f.figarea.copy_from_bbox(f.fig.bbox)

    
    #definebg(f,s)
    plotartists(f,s)
    
    # Save data before closing application
    def closeapp():
        """Save Data before closing application"""
        pickle.dump(s,open(s.name+'.pickle','wb'))
        root.destroy()
        print('saved '+s.name)
        return
    root.protocol("WM_DELETE_WINDOW",closeapp)
    
    return

def get_songlist():
    songlist = []
    #Search for pickle files
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for root,dirs,files in os.walk(dir_path):
        for file in files:
            if file.endswith('.pickle'):
                songlist.append(file[0:-7]) #remove .pickle ending
    return songlist
    
### Main window
root = Tk()

# New Song
newsong_Button = Button(root,command=initialize_song,text='New Song')
newsong_Button.grid(row=0,column=0)

# Load old song
songlist = get_songlist() #list of saved songs
if songlist:
    cursong = StringVar(root)
    cursong.set(songlist[0])
    loadsongButton = Button(root,command=unpickle_song,text='Load Song');
    loadsongButton.grid(row=1,column=0)
    loadsongMenu = OptionMenu(root,cursong,*songlist)
    loadsongMenu.grid(row=2,column=0)


# Popup menu for songs saved
root.mainloop()

