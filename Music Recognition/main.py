# %%
# # -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 19:11:53 2022

@author: afisher
"""
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import utils_model as um
import utils_io as uio
import utils_music_munging as umm
import utils_image_processing as uip
import cv2 as cv
from scipy import ndimage
import os
import pickle

# Use shapes as well as color to distinguish labels
# Make sure pitches are correct by applying shifts for modifiers as needed
# No need for manually adding measures at end of line
# Trouble shoot pitches, best to have unit test of sorts?


staff_margin = 4

# Import and clean music
song_file = 'Songs\\flats.jpg'
raw_music = uio.import_song(song_file)
orig, line_sep, n_lines = umm.clean_music(raw_music.copy())
cv.imwrite('Test\\original.jpg', orig)

# Fill notes and flats
filled_img, _ = um.run_model(orig.copy(), line_sep, model_type='filling')
fill_mask = cv.bitwise_and(orig, cv.bitwise_not(filled_img))
cv.imwrite('Test\\filled_image.jpg', filled_img)

# Remove staff lines
nostaff_img = umm.remove_staff_lines(filled_img.copy())
cv.imwrite('Test\\no_staff.jpg', nostaff_img)

# Identify notations, separate into structures
_, notations = um.run_model(nostaff_img.copy(), line_sep, 'notations')
measures, rests, modifiers, timesig = umm.separate_notations(notations, orig.copy(), line_sep)

# Remove notations
no_notations_img = umm.remove_nonnotes(nostaff_img, notations, line_sep)    
cv.imwrite('Test\\no notations.jpg', no_notations_img)


# Close to remove lines all lines
closed_img = uip.morphology_operation(
    no_notations_img.copy(), (.25*line_sep, .25*line_sep), cv.MORPH_CLOSE
)

# Identify notes and separate with kmeans clustering
_, grouped_notes = um.run_model(closed_img.copy(), line_sep, 'notes')
notes = umm.separate_grouped_notes(closed_img.copy(), grouped_notes)

# Perform computations on notes
notes = umm.compute_stems_and_tails(no_notations_img.copy(), notes, line_sep)
notes = umm.compute_is_filled(fill_mask, notes)
notes, keysig = umm.apply_note_modifiers(notes, modifiers, line_sep)
notes = umm.apply_keysignature(notes, orig, keysig, measures, line_sep)
notes['duration'] = 2.0**(1+notes.is_filled - notes.is_stemmed - notes.tails) * (1+0.5*notes.is_dotted)
notes = umm.compute_beats(notes, rests, line_sep)
uio.write_to_WAV(notes)
# %%

def check_note_booleans(img, notes, col):
    color_img = cv.cvtColor(orig, cv.COLOR_GRAY2BGR)
    mcolors = [(0,0,255),(0,255,0)]
    for index, row in notes.iterrows():
        x,y,w,h = row[['x','y','w','h']]
        if col.startswith('is_'):
            cv.rectangle(color_img, (x,y), (x+w,y+h), mcolors[int(row[col])], 5)
        elif col=='duration':
            scale = round(np.log(row.duration/4)/np.log(0.5)*255/3)
            color = (0, 255-scale, scale)
            cv.rectangle(color_img, (x,y), (x+w,y+h), color, 5)

        # cv.rectangle(color_img, (x,y), (x+w,y+h), mcolors[int(row.is_filled)], 5)
        # cv.circle(color_img, (x+w//2,y+h//2), 10, mcolors[row.tails], thickness=-1)
        
    uio.show_image(color_img, reduce=2)
    return
check_note_booleans(orig, notes, 'duration')

# %%


# %%


    

# Close image to remove lines
# uio.show_image(no_nonnotes_img, reduce=2)
# test = FillingValidation(orig)
# test = NotationValidation(nostaff_img)
# test = NoteValidation(closed_img)
# %%
