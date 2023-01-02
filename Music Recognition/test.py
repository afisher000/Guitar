# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 15:19:11 2023

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


song_file = 'Songs\\naturals.jpg'
raw_music = uio.import_song(song_file)

# Get line_sep and n_lines
line_sep, n_lines = umm.get_line_data(raw_music)[2:]
cleaned_img = umm.strip_words(raw_music.copy(), line_sep, n_lines)
orig =  umm.equalize_music_lines(cleaned_img.copy(), margin=6)
line_height = orig.shape[0]//n_lines





# cs = um.get_image_contours(orig, model_type='awoefijaew')
# orig = cv.cvtColor(orig, cv.COLOR_GRAY2BGR)
# for c in cs:
#     cv.floodFill(orig, None, c[0,0,:], (0,255,0))
    
# uio.show_image(orig, reduce=2)
