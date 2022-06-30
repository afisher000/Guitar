# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 16:23:09 2021

@author: afisher
"""

from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import time
    
root = Tk()

fig,ax = plt.subplots()
plt.text(0.5,0.5,'t1');


figarea = FigureCanvasTkAgg(fig,master=root)
figarea.get_tk_widget().grid(row=0,column=0)
figarea.draw()
figarea.flush_events()
bg = figarea.copy_from_bbox(fig.bbox)

a1 = plt.text(0.2,0.2,'a1',animated = True)
ax.draw_artist(a1)
figarea.blit(fig.bbox)

plt.text(0.45,0.45,'t2')
figarea.draw()

figarea.restore_region(bg)
figarea.draw()

#a1.set_x(0.8)
#a1.set_y(0.8)
#ax.draw_artist(a1)
#figarea.blit(fig.bbox)
#figarea.flush_events()


root.mainloop()

    
