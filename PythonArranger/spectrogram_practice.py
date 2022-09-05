# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 19:30:08 2022

@author: afisher
"""

from scipy.signal import spectrogram
from scipy.io import wavfile
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.interpolate import interp2d, RectBivariateSpline
from scipy.fft import rfft, rfftfreq
from scipy.optimize import minimize

plt.close('all')



# MIDI Convention
# Middle C - C4 is note 60
# A4 (note 69) is defined as 440Hz
# For reference, guitar open note frequencies are 82, 110, 146, 196, 250, 330
# Midi open notes are 40, 45, 50, 55, 59, 64

freq_to_note = lambda f: 12/np.log(2)*np.log(f/440) + 69
open_midi_notes = np.array([40, 45, 50, 55, 59, 64])
tstart = 5
tend = 10
fmin = 78
fmax = 1000

# Read wav file
file = 'Hurt.wav'
folder = 'WAV Downloads'
raw_fs, raw_data = wavfile.read(os.path.join(folder, file))

# Reduce sampling frequency according to fmax (speeds up spectrogram computation)
ideal_fs = 2 * fmax
skip = raw_fs//ideal_fs
fs = raw_fs/skip
sample = raw_data[round(tstart*raw_fs):round(tend*raw_fs):skip,0]

# Compute spectrogram
tseg = .33 #seconds
overlap = .9

nperseg = round(fs*tseg)
noverlap = round(nperseg*overlap)
f, t, S = spectrogram(sample, fs=fs, nperseg=nperseg, noverlap=noverlap)
t = t+tstart

# Truncate lower frequencies (avoid log(0) when converting to notes)
S = S[f>fmin,:]
f = f[f>fmin]


# Interpolate to guitar notes
guitar_notes = np.arange(40, 75)
n = freq_to_note(f)
f_int = interp2d(t, n, S)

S = np.zeros((len(guitar_notes), len(t)))
for j, note in enumerate(guitar_notes):
    S[j,:] = f_int(t, note)

# Scale frequencies to bring out notes equally
marginal_max = S.max(axis=1)
pk_loc = find_peaks(marginal_max)[0]
threshold = np.sort(marginal_max[pk_loc])[-5]/2
scale = np.where(marginal_max<threshold, threshold, marginal_max).reshape((-1,1))
S = S/scale

# Plot spectrogram
fig, ax = plt.subplots()
T, N = np.meshgrid(t, guitar_notes)
ax.pcolor(T, N, S, shading='nearest')
for note in open_midi_notes:
    ax.plot([tstart, tend], [note, note], 'k:')
ax.set_ylim([39, 76])
ax.set_xlim([tstart, tend])
ax.set_xlabel('Time (s)')
ax.set_ylabel('Note')

def plot_note_history(midi_note):
    idx = midi_note - guitar_notes.min()
    fig, ax = plt.subplots()
    ax.plot(t, S[idx,:], label=f'{note}')
    ax.legend()
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')


# Can I figure out the beat of the sample?
sample = np.array(sample, dtype=float)
window = round(fs/8)
intensity = np.convolve(sample**2, np.ones(window)/window, mode='valid')
plt.plot(intensity)
amp = np.abs(rfft(intensity))
freq = rfftfreq(len(intensity), 1/fs)


pk_loc = find_peaks(intensity, width=100, prominence=intensity.max()/15)[0]
# fig, ax = plt.subplots()
# ax.plot(intensity)
# ax.scatter(pk_loc, intensity[pk_loc])




diff = np.diff(pk_loc)
diff = diff[np.abs(diff-diff.mean())<2*diff.std()] #drop outliers
bpm = 60*fs/diff.mean()

dy = diff.mean()
xi = pk_loc
xi2 = ((xi-xi[0]+dy/2) % dy) - dy/2
y = xi[0] + xi2[np.abs(xi2)<dy/4].mean()
yi = np.arange(y, len(intensity), dy)
for val in np.round(yi):
    ax.plot([t[val], t[val]], [0, intensity.max()], 'k:')





