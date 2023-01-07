# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 17:01:55 2022

@author: afisher
"""
import pickle
import cv2 as cv
import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
import utils_io as uio

training_columns = [
    'area','width','height','aspectratio','extent','solidity','angle'
    ]
data_columns = [
        'state', 'cx', 'cy','area', 'x','y','w','h','width',
        'height','aspectratio','extent','solidity', 'angle'
    ]

database_files = {
    'filling':'training_data_filling.csv',
    'notations':'training_data_notations.csv',
    'notes':'training_data_notes.csv'
}

model_files = { 
    'filling':'model_to_fill_contours.pkl',
    'notations':'model_to_identify_notations.pkl',
    'notes':'model_to_identify_notes.pkl'
}
notation_colors = { 
        's':(255,0,0), #sharp
        'n':(255,100,100), #natural
        'f':(255,200,200), #flat
        'm':(0,255,255), #measure
        'd':(100,255,255), #dot
        '2':(255,0,255),
        '3':(255,60,255),
        '4':(255,120,255),
        '6':(255,180,255),
        '8':(255,240,255),
        'q':(200,200,255), #1/16th rest
        'w':(100,100,255), #1/8th rest
        'e':(0,0,255), #1/4rest
        'r':(255,255,0), #half rest
        't':(255,255,100), #whole rest
        '\r':(100,100,100)
    }

note_colors = {
    '1':(255,0,0),
    '2':(0,255,0),
    '3':(0,0,255),
    '\r':(100,100,100)
    }

def annotate_contour(img, row, model_type, validation=False):
    if model_type == 'filling':
        if row.state!='\r':
            fill_value = 100 if validation else 0
            cv.floodFill(img, None, (int(row.cx), int(row.cy)), fill_value)
    elif model_type == 'notations':
        if len(img.shape)==2: #Is grayscale
            img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
        color = notation_colors[row.state]
        cv.circle(img, (int(row.cx), int(row.cy)), radius=15, color=color, thickness=-1)
    elif model_type == 'notes':
        if len(img.shape)==2: #Is grayscale
            img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
        color = note_colors[row.state]
        cv.circle(img, (int(row.cx), int(row.cy)), radius=15, color=color, thickness=-1)  
    return img


def get_image_contours(img, model_type=None):
    # Ensure outside border is white
    img[[0,img.shape[0]-1],:]=255
    img[:,[0,img.shape[1]-1]]=255
    
    # RETR_CCOMP returns only two hierarchy levels, so if contour has 
    # no parent, it is white enclosing
    cs, hs = cv.findContours(img, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    contours = []
    for j, c in enumerate(cs):
        if model_type is None:
            contours.append(c)
        elif model_type=='filling':
            if hs[0,j,3]==-1: #is white enclosing
                contours.append(c)
        else:
            if hs[0,j,3]!=-1: #is black enclosing
                 contours.append(c)
    return contours
    
def run_model(img, model_type, validation=False, verbose=False):
    
    # Get contour data from image
    contours = get_image_contours(img.copy(), model_type)
    data = get_contour_data(contours)
    
    # Apply model if exists
    model_file = model_files[model_type]
    if os.path.exists(model_file):
        model = pickle.load(open(model_file, 'rb'))
        X = data[training_columns].values
        data.state = model.predict(X)
    else:
        print(f'Model file {model_file} does not exist...')
        
    # Alter image
    for _, row in data.iterrows():
        img = annotate_contour(img, row, model_type, validation)

    if not verbose:    
        # Only return state, centroid, and boundingrect
        return_columns = ['state','cx','cy','x','y','w','h']
        data = data.loc[data.state!='\r', return_columns]
    return img, data.reset_index(drop=True)
    
    
def get_contour_data(contours):
    line_sep = uio.get_song_params(['line_sep'])
    
    contour_df = pd.DataFrame(columns=data_columns)
    for c in contours:
        # Faults can arise when m00=0 or len(c)<4 and ellipse cannot be fit.
        try:
            M = cv.moments(c)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00']) 
        except:
            continue
        
        area = cv.contourArea(c)
        x,y,w,h = cv.boundingRect(c)
        if area<50:
            continue
        
        hull = cv.convexHull(c)
        hull_area = cv.contourArea(hull)
        try:
            _,(MA,ma),angle = cv.fitEllipse(c)
        except:
            MA, ma, angle = 0, 0, 0
        
        # Normalize
        area = area/line_sep**2
        hull_area = hull_area/line_sep**2
        MA = MA/line_sep
        ma = ma/line_sep
        width = w/line_sep
        height = h/line_sep
        
        # Ratios
        aspect_ratio = float(w)/h
        extent = float(area)/(w*h)
        solidity = float(area)/hull_area

        
        # Append to dataframe
        contour_df.loc[len(contour_df)] = [
            '\r', cx, cy, area, x,y,w,h,width, height, 
            aspect_ratio, extent, solidity, angle
        ]

    return contour_df
    
class BaseValidation():
    def __init__(self, orig, model_type):
        self.orig = orig
        self.model_type = model_type

        # Run model
        self.img, self.data = run_model(
            orig.copy(), model_type=model_type, validation=True, verbose=True
        )
        
        # Main loop
        self.main_loop()
        
    def show_image(self):
        return cv.pyrDown(cv.pyrDown(self.img))
    
    def main_loop(self):
        cv.namedWindow = 'main'
        cv.imshow('main', self.show_image())
        cv.setMouseCallback('main', self.mouseCallback)
        
        while True:
            cv.imshow('main', self.show_image())
            k = cv.waitKey(20)
            if k==ord('s'):
                self.save_to_database()
                break
            elif k==ord('q'):
                # Quit without saving
                break
        cv.destroyWindow('main')
        
        
    def mouseCallback(self, event, x, y, flags, param):
        return
    
    def save_to_database(self):
        database_file = database_files[self.model_type]
        model_file = model_files[self.model_type]
        if os.path.exists(database_file):
            db_data = pd.read_csv(database_file)
        else:
            db_data = pd.DataFrame(columns=data_columns)

        db_data = pd.concat([db_data, self.data])
        db_data.to_csv(database_file, index=False)
        
        y = db_data.state
        X = db_data[training_columns].values
        model = RandomForestClassifier()
        model.fit(X,y)
        pickle.dump(model, open(model_file, 'wb'))
        return
    
    

class FillingValidation(BaseValidation):
    def __init__(self, orig):
        BaseValidation.__init__(self, orig, 'filling')
        
    def mouseCallback(self, event, x, y, flags, param):
        # Fill or unfill contour
        if event == cv.EVENT_LBUTTONDBLCLK:
            cv.namedWindow='zoomed'
            padh = 500
            padv = 200
            top = max(0, 4*y-padv)
            bottom = min(self.img.shape[0], 4*y+padv)
            left = max(0, 4*x-padh)
            right = min(self.img.shape[1], 4*x+padh)
            cv.imshow('zoomed', self.img[top:bottom, left:right])
            
            def inputCallback(event, x, y, flags, param):
                if event == cv.EVENT_LBUTTONDOWN:
                    # Get x,y pixels of orig
                    x += left
                    y += top

                    idx = np.argmin((self.data.cx-x)**2+(self.data.cy-y)**2)
                    cx, cy = self.data.loc[idx, ['cx','cy']]

                    if self.img[cy,cx]==255:
                        fill_value = 100
                        self.data.loc[idx, 'state'] = '1'
                    elif self.img[cy,cx]==100:
                        fill_value = 255
                        self.data.loc[idx, 'state'] = '\r'
                    else:
                        fill_value = 0
                    cv.floodFill(self.img, None, (cx,cy), fill_value)
                    cv.imshow('zoomed', self.img[top:bottom, left:right])
                return
            cv.setMouseCallback('zoomed', inputCallback)
        return
    
class NotationValidation(BaseValidation):
    def __init__(self, orig):
        BaseValidation.__init__(self, orig, 'notations')  
        
    def mouseCallback(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDBLCLK:
            cv.namedWindow = 'zoomed'
            idx = np.argmin((self.data.cx-4*x)**2+(self.data.cy-4*y)**2)
            x, y, w, h = self.data.loc[idx,['x','y','w','h']]
            
            # Show closeup, respond with keypress
            cv.imshow('zoomed', self.orig[y:y+h,x:x+w])
            key = cv.waitKey(0)
            cv.destroyWindow('zoomed')
            
            # Update color label
            if key in list(map(ord, 'sfnmd23468qwert\r')):
                self.data.loc[idx, 'state'] = chr(key)
                annotate_contour(self.img, self.data.loc[idx], model_type=self.model_type)
        return
    
    
class NoteValidation(BaseValidation):
    def __init__(self, orig):
        BaseValidation.__init__(self, orig, 'notes')  

    def mouseCallback(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDBLCLK:
            cv.namedWindow = 'zoomed'
            idx = np.argmin((self.data.cx-4*x)**2+(self.data.cy-4*y)**2)
            x, y, w, h = self.data.loc[idx,['x','y','w','h']]
            
            # Show closeup, respond with keypress
            cv.imshow('zoomed', self.orig[y:y+h,x:x+w])
            key = cv.waitKey(0)
            cv.destroyWindow('zoomed')
            
            # Update color label
            if key in list(map(ord, '1234\r')):
                self.data.loc[idx, 'state'] = chr(key)
                annotate_contour(self.img, self.data.loc[idx], model_type=self.model_type)
        return
