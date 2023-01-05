# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 12:54:45 2023

@author: afisher
"""

# %%
import pandas as pd
import numpy as np
from scipy.io.wavfile import read, write
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq, irfft



def damped_harmonic_oscillator(freqs, f0s, dampings=None, forces=None):
    '''Uses solution of damped harmonic oscillator in terms of F0, m, b
    where we put damping and force in terms of mass. A small epsilon is used
    to avoid dividing by zero.'''
    eps = 1e-4
    amplitude = np.zeros_like(freqs)
    phase = np.zeros_like(freqs)
    spectrum = np.zeros_like(freqs)
    
    dampings = np.ones_like(f0s) if dampings is None else dampings
    forces = np.ones_like(f0s) if forces is None else forces
    for f0, damping, force in zip(f0s, dampings, forces):
        amplitude = force/np.sqrt((f0**2-freqs**2+eps)**2 + damping**2*freqs**2)
        phase = np.arctan(damping*freqs/(f0**2-freqs**2+eps))
        phase[freqs>f0] += np.pi
        spectrum = spectrum + amplitude * np.exp(-1j*phase)
    return spectrum

def unwind_phase(mod_phase):
    differences = np.diff(mod_phase, prepend=mod_phase[0])
    drop_correction = 2*np.pi*np.cumsum(differences<-np.pi)
    jump_correction = -2*np.pi*np.cumsum(differences>np.pi)
    return mod_phase + drop_correction + jump_correction


# Read files
sample_rate, raw_audio = read('guitarnote_A#.wav')
time = np.arange(len(raw_audio)) * 1/sample_rate

# Clip out from 1sec to 3sec
audio = raw_audio[1*sample_rate:3*sample_rate]
T = 5

# Take fourier transform
yf = rfft(audio)
freq = rfftfreq(len(audio), 1/sample_rate)
reals, imags = yf.real, yf.imag
f_r = interp1d(freq, reals)
f_i = interp1d(freq, imags)

new_freq = np.arange(freq[0], freq[-1], 1/T)
new_reals = f_r(new_freq)
new_imags = f_i(new_freq)
new_yf = new_reals + 1j*new_imags
new_audio = irfft(new_yf, T*sample_rate).astype(np.int16)

write('test.wav', sample_rate, new_audio)
# Make digital signal
# f0 = 233
# f0s = f0*np.arange(1,8)
# dampings = [0.5, 0.5, 0.5, 0.5, 0.5, 1, 1]
# forces = [10, 4, 3.6, 0, 5, 5.4, 4.9]
# digital_spectrum = damped_harmonic_oscillator(freq, f0s, dampings, forces)
# amplitude = np.abs(digital_spectrum)
# phase = np.angle(digital_spectrum)

# # Convert digital spectrum to audio
# audio_digital = irfft(digital_spectrum, len(time))


# # Clip sec 1 to sec3
# audio_digital = audio_digital[sample_rate:3*sample_rate]

# # Scale audio to 32000 for int16
# audio_digital *= 32000/np.abs(audio_digital).max()
# audio_digital = audio_digital.astype(np.int16)

# # Write to file
# write('test_synthetic.wav', sample_rate, audio_digital)
# write('test_real.wav', sample_rate, audio)

# # Plot
# plt.close('all')
# fig, ax = plt.subplots()
# # f0 = 3*233
# scn = (freq>.95*f0)&(freq<1.05*10*f0)
# ax.plot(freq[scn], np.abs(yf[scn])/np.abs(yf[scn]).max())
# # ax.plot(freq[scn], unwind_phase(np.angle(yf[scn])))
# ax.plot(freq[scn], amplitude[scn]/amplitude[scn].max())
# # ax.plot(freq[scn], unwind_phase(phase[scn]))


# ax.set_xlim([f0s[0]*.95, f0s[-1]*1.05])
# ax.plot(freq, amplitude/amplitude.max()*np.abs(yf).max())
# ax.plot(freq, np.abs(yf))

# ax.plot(freq, phase)
# ax.plot(freq, np.angle(yf))
# ax.plot(time[sample_rate:3*sample_rate],audio_digital)
# 