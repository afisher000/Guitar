# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 16:44:26 2022

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
from scipy.signal import spectrogram


mw_Ui, mw_Base = uic.loadUiType('spectrogram.ui')
class Main_Window(mw_Base, mw_Ui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Define structures
        self.notes = pd.DataFrame(columns=['beatdiv','string','fret'], dtype=int)

        
        # Import Layout
        self.setupUi(self)
        
        
        
        
        # Read file
        _, fs = sf.read('WAV files/hurt.wav', dtype='float32', start=0, stop=10)
        data, _ = sf.read('WAV files/hurt.wav', dtype='float32', start=0, stop=20*fs)
        data = data.mean(axis=1)
        time = np.arange(0, len(data)/fs, 1/fs)

        # Perform spectrogram
        f, t, Sxx = spectrogram(data, fs=fs, nperseg=round(fs*.5), noverlap=round(fs*.1))
        self.canvas.setImage(Sxx)
        self.hist = self.canvas.getHistogramWidget()
        
        self.show()
        
        return
        
        
if __name__=='__main__':
    ''' Run application. Uncomment app.exec_() for troubleshooting. '''
    if not qtw.QApplication.instance():
        app = qtw.QApplication(sys.argv)
    else:
        app = qtw.QApplication.instance()
    w = Main_Window()

        
        
        
        
        
        
        