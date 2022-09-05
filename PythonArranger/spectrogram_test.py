# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 16:46:15 2022

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


# Read file
_, fs = sf.read('WAV files/hurt.wav', dtype='float32', start=0, stop=10)
data, _ = sf.read('WAV files/hurt.wav', dtype='float32', start=0, stop=20*fs)
data = data.mean(axis=1)
time = np.arange(0, len(data)/fs, 1/fs)

# Perform spectrogram
f, t, s = spectrogram(data, fs=fs, nperseg=round(fs*.5), noverlap=round(fs*.1))
