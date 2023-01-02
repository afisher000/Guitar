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

song_file = 'Songs\\dots, eights, and sixteenths.jpg'
raw_music = uio.import_song(song_file)

# Get line_sep and n_lines
line_sep, n_lines = umm.get_line_data(raw_music)[2:]
cleaned_img = umm.strip_words(raw_music.copy(), line_sep, n_lines)
orig =  umm.equalize_music_lines(cleaned_img.copy(), margin=5)
line_height = orig.shape[0]//n_lines

# Fill notes and flats
filled_img, _ = um.run_model(orig.copy(), line_sep, model_type='filling')
nostaff_img = umm.remove_staff_lines(filled_img.copy())
cv.imwrite('Test\\no_staff.jpg', nostaff_img)

# Identify nonnotes
_, nonnotes = um.run_model(nostaff_img.copy(), line_sep, 'nonnotes')

# Remove nonnotes
no_nonnotes = umm.remove_nonnotes(nostaff_img, nonnotes, line_sep)    
cv.imwrite('Test\\no_nonnotes.jpg', no_nonnotes)

# Close to remove lines, identify notes
closed_img = uip.morphology_operation(
    no_nonnotes.copy(), (.25*line_sep, .25*line_sep), cv.MORPH_CLOSE
)
_, notes = um.run_model(closed_img.copy(), line_sep, 'notes')


# Compute tails
umm.compute_note_tails(no_nonnotes, notes, line_sep)

# Compute is_filled column for notes
fill_mask = (orig&(~filled_img))
for index, (x,y,w,h) in notes[['x','y','w','h']].iterrows():
    is_filled = int(fill_mask[y:y+h, x:x+w].sum()>0)
    notes.loc[index, 'is_filled'] = is_filled

    
    

# umm.compute_note_filling(fill_mask, notes)

    

# Close image to remove lines
# uio.show_image(no_nonnotes_img, reduce=2)
# 
# test = FillingValidation(orig, line_sep)
# test = NonNoteValidation(nostaff_img, line_sep)
# test = NoteValidation(closed_img, line_sep)
# %%
