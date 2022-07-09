# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 20:12:29 2022

@author: afisher
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append('C:\\Users\\afisher\\Documents\\GitHub\\Guitar\\PythonArranger\\GUIPackages')
from Transcriber import Database, Cursor, Tab
import fitz
import os
songname = 'hurt'
tab = Tab()
db = Database()
notes = db.load_table(songname)
db.close()


linemeasures = tab.linemeasures
strings = 6
measurebeats = tab.measurebeats
measbuffer = 0.5 # in beats
pagelines = tab.pagelines
staffbuffer = tab.staffspacing
lineheight = staffbuffer + strings-1


measurewidth = measurebeats + measbuffer
linebeats = linemeasures * measurebeats
linewidth = linemeasures * measurewidth
Npages = notes.beatdiv.max()//tab.pagedivs + 1

for page in range(Npages):
    pagenotes = notes[notes.beatdiv.between(page*tab.pagedivs, (page+1)*tab.pagedivs-1)]
    
    fig, ax = plt.subplots()
    fig.set_size_inches(8.5, 11)
    fig.set_dpi(100)
    
    # Plot staff lines
    xref = np.append([0, linewidth, 0]*strings,
                       np.repeat(np.arange(linemeasures+1)*measurewidth, 3))
    yref = np.append(np.repeat(np.arange(-strings,0)+1,3),
                       [1-strings,0,1-strings]*(linemeasures+1))
    for j in range(pagelines):
        ax.plot(xref, yref - j*lineheight, c='k',
                linewidth=0.7)
    
    # Plot notes
    for index, note in pagenotes.iterrows():
        line, beat = divmod(note.beatdiv /tab.beatdivs, linebeats)
        notebuffer = ((beat // measurebeats)+1)*measbuffer
        
        x = notebuffer + beat
        y = note.string - line*lineheight
        ax.text(x, y, str(int(note.fret)),
                backgroundcolor='w',
                fontfamily = 'serif',
                fontsize = 8,
                va = 'center',
                ha = 'center',
                bbox = dict(pad=0.5, 
                            fill=True, 
                            facecolor='white', 
                            edgecolor='none',
                            mutation_scale = 1,
                            mutation_aspect = 1/10))

    
    # turn off axes and save
    if page==0:
        ax.set_title(songname.title(), fontdict = {'fontsize': 30})
    ax.axis('off')
    plt.savefig(f'{songname}{page}.pdf', bbox_inches='tight')
    plt.close('all')


# Merge pdfs
total_pdf = fitz.open()
pdfs = [f'{songname}{j}.pdf' for j in range(Npages)]
for pdf in pdfs:
    with fitz.open(pdf) as mfile:
        total_pdf.insert_pdf(mfile)
total_pdf.save(os.path.join('Song PDFs',f'{songname}.pdf'))

# Delete individuals
for pdf in pdfs:
    os.remove(pdf)


