# %%
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
import utils_music_theory as umt
import cv2 as cv
from scipy import ndimage
import os
import pickle

# Load file
notes = pd.read_csv('notes.csv')
notations = pd.read_csv('notations.csv')
line_sep = 35

dots = notations[notations.state=='d']
dot = dots.iloc[0]
dists = dot[['cx','cy']] - notes.loc[:,['cx','cy']]
is_close_cx = dists.cx.between(0, 3*line_sep)
is_close_cy = dists.cy.between(-1*line_sep, line_sep)
# for index, row in dots.iterrows():
    

