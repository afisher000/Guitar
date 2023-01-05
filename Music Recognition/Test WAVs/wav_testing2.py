# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 17:52:20 2023

@author: afisher
"""

import pandas as pd
import numpy as np
from scipy.io.wavfile import read, write
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq, irfft
from playsound import playsound
from scipy.signal import savgol_filter

# Read files
sample_rate, raw_audio = read('guitarnote_A#.wav')
fundamental = 233 #Hz
T = 4

# Separate audio
pluck = raw_audio[:sample_rate//4]
audio = raw_audio[sample_rate//4:2*sample_rate]

# Remove high frequency noise
noise_cutoff = 10*fundamental
low_pass_audio = savgol_filter(
    audio, 
    2*(sample_rate//noise_cutoff)+1, 
    polyorder=3
)

# Compute decay
intensity = savgol_filter(
    np.abs(low_pass_audio), 
    10*(sample_rate//fundamental)+1, 
    polyorder=1
)

# Fit with exponential
time = np.arange(len(intensity)) * 1/sample_rate
line_fit = np.polyfit(time, np.log(intensity), 1)
decay = line_fit[0]

# Cancel decay of signal
steady_state_audio = (low_pass_audio * np.exp(-decay*time)).astype(np.int16())

# Take fourier transform
yf = rfft(steady_state_audio)
freq = rfftfreq(len(steady_state_audio), 1/sample_rate)

# Interpolate to finer frequency, 1/T
reals, imags = yf.real, yf.imag
f_r = interp1d(freq, reals, 'nearest')
f_i = interp1d(freq, imags, 'nearest')
new_freq = np.arange(freq[0], freq[-1], 1/T)
new_reals = f_r(new_freq)
new_imags = f_i(new_freq)
new_yf = new_reals + 1j*new_imags

# Inverse transform back to time domain
lengthened_audio = irfft(new_yf, T*sample_rate).astype(np.int16)

# Compute decay and cancel it
intensity = savgol_filter(
    np.abs(lengthened_audio), 
    10*(sample_rate//fundamental)+1, 
    polyorder=1
)
steady_state_audio = (lengthened_audio * 1.5*intensity[0]/intensity).astype(np.int16)



# Save to file and plot
write('test.wav', sample_rate, steady_state_audio)

plt.close('all')
fig, ax = plt.subplots()
ax.plot(lengthened_audio)
# ax.plot(steady_state_audio)
