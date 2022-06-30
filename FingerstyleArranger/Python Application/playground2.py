# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 17:55:44 2021

@author: afisher
"""
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import time
    
root = Tk()

fig,ax = plt.subplots()
figarea = FigureCanvasTkAgg(fig,master=root)
figarea.get_tk_widget().grid(row=0,column=0)

plt.text(0.5,0.5,'X',zorder=2)
plt.plot([0,1],[0,1],color=(1,1,1),linewidth=10)

figarea.draw()

plt.plot([1,0],[0,1],color='red',linewidth=10)
figarea.draw()



root.mainloop()