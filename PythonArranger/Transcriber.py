# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 19:48:47 2022

@author: afish
"""
import pandas as pd
import numpy as np

# =============================================================================
# Save songs in pysql database
# 
# =============================================================================


# Define parameters
song_dict = {'BPM':120, 'bpm':4, 'capo':0, 'tuning':[0]*6}
spect_dict = {'tmin':0, 'tspan':6, 'wfac':0.5, 'ofac':0.5, 'Nmin':-4, 'Nmax':40}
tab_dict = {'pagelines':8, 'linemeasures':4, 'staff_spacing':4, 'meas_spacing':10, 'dy':.1}

# Initialize song dataframe and cursor
data = pd.DataFrame(columns=['time','notenum','meas','beat','string','fret'])
cur = pd.Series([0,0,1,0.5],index=['meas','beat','string','step'])
