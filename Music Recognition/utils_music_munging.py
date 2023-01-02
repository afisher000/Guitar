import cv2 as cv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import utils_image_processing as uip
import utils_music_theory as umt
import utils_model as um


def remove_staff_lines(img):
     # Turn white if pixel above and below line is white
    line_starts, line_ends, _, _ = get_line_data(img)
    for start, end in zip(line_starts, line_ends):
        line_fill = (img[start,:])&(img[end+1,:])
        img[start:end+1,:] = line_fill
    return img

def get_line_data(img):
    is_line = (img.sum(axis=1)/img.shape[1]) < 127
    is_line_start = np.logical_and(~is_line[:-1], is_line[1:])
    is_line_end = np.logical_and(is_line[:-1], ~is_line[1:])
    line_starts = np.where(is_line_start)[0]
    line_ends = np.where(is_line_end)[0]
    line_sep = np.diff(line_starts[:5]).mean()
    n_lines = len(line_starts)//5
    return line_starts, line_ends, line_sep, n_lines

    
def strip_words(img, line_sep, n_lines):
    # Remove long line connecting staff and treble
    long_vert_lines = uip.morphology_operation(img.copy(), (10*line_sep, 1), cv.MORPH_CLOSE)
    words_img = ~((~img)&(long_vert_lines))
    
    # Fill bounding rects of staff contours, then floodfill white
    contours, _ = cv.findContours(~words_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cs = sorted(contours, key=cv.contourArea)[::-1]
    for c in cs[:n_lines]:
        x,y,w,h = cv.boundingRect(c)
        words_img[y:y+h, :] = 0
        cv.floodFill(words_img, None, (int(x+w/2), int(y+h/2)), 255)
    cleaned_img = ~((~img)&(words_img))
    return cleaned_img

def equalize_music_lines(img, margin=4):
    # Remove all-white columns
    non_white_cols = img.sum(axis=0)<255*img.shape[0]
    img = img[:, non_white_cols]

    
    # Get image for each staff
    line_starts, line_ends, line_sep, n_lines = get_line_data(img)
    staff_imgs = []
    for j in range(n_lines):
        top = int(line_starts[5*j] - margin*line_sep)
        bottom = int(line_starts[4+5*j] + margin*line_sep)
        left = int(3.5*line_sep)
        right = int(-1.0*line_sep)
        
        # For each line, flood fill any black pixels on top/bottom edge
        staff_img = img[top:bottom, left:right].copy()
        for col in range(staff_img.shape[1]):
            if staff_img[-1,col]==0:
                cv.floodFill(staff_img, None, (col,staff_img.shape[0]-1),255)
            if staff_img[0,col]==0:
                cv.floodFill(staff_img, None, (col,0),255)
        staff_imgs.append(staff_img)
    img = np.vstack(staff_imgs)
    return img

def compute_note_tails(img, notes, line_sep):
    stems = uip.morphology_operation(img, (3*line_sep,1), cv.MORPH_CLOSE)
    dilated_stems = uip.morphology_operation(
        stems, (.25*line_sep, .25*line_sep), cv.MORPH_ERODE
    )
    stem_contours, _ = cv.findContours(~dilated_stems, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    notes = notes[notes.state!='\r']
    
    for c in stem_contours:
        x,y,w,h = cv.boundingRect(c)
        is_overlapping = uip.check_rectange_overlap(
            (x,y,w,h), (notes.x,notes.y,notes.w,notes.h)
        )
    
        ymin = notes.y[is_overlapping].min()
        ymax = notes.loc[is_overlapping, ['y','h']].sum(axis=1).max()
        
        y_idx = np.arange(y, y+h)
        y_idx = y_idx[(y_idx<ymin)|(y_idx>ymax)]
        left_column = img[y_idx, x]
        right_column = img[y_idx, x+w]
        left_tails = len(np.diff(left_column).nonzero()[0])//2
        right_tails = len(np.diff(right_column).nonzero()[0])//2
        tails = max(left_tails, right_tails)
        notes.loc[is_overlapping, ['tails']] = tails
    return notes

def remove_nonnotes(img, nonnotes, line_sep):
    for _, row in nonnotes.iterrows():
        if row.state!='\r':
            x,y,width,height = row[['x','y','width','height']]
            x,y,w,h = int(x), int(y), int(width*line_sep), int(height*line_sep)
            cv.rectangle(img, (x,y), (x+w,y+h), 255, -1)
    return img

def munge_blob_data(closed_img, blobs, line_sep, line_height):
    blobs = blobs[blobs.state!='none']
    blobs['raw_line'] = blobs.cy.floordiv(line_height)
    blobs['line'] = blobs.raw_line.floordiv(2)
    blobs['is_bass'] = blobs.raw_line.mod(2).astype(bool)
    blobs['time'] = blobs.raw_line*blobs.cx.max() + blobs.cx
    blobs = blobs.sort_values(by=['raw_line','cx'])
    
    song_input = pd.DataFrame(columns=['state','cx','cy','line','measure','staff_pitch','pitch'])
    for index, row in blobs.iterrows():
        # CLEANUP?
        measure = sum((blobs.state=='m')&(blobs.is_bass==row.is_bass)&(blobs.time<row.time))
        
        # If multiple notes, apply kmeans clustering before saving
        if row.state in '234':
            rect = [row.x, row.y, row.width*line_sep, row.height*line_sep]
            n_clusters = int(row.state)
            cluster_centers = uip.get_cluster_centers(rect, closed_img, n_clusters)
            for (cy0,cx0) in cluster_centers:
                staff_pitch = umt.get_staff_pitch(cy0, line_sep, line_height, row.is_bass)
                pitch = umt.get_pitch_from_staff_pitch(staff_pitch)
                song_input.loc[len(song_input)] = [
                    '1', cx0, cy0, row.line, measure, staff_pitch, pitch
                ]
        else:
            staff_pitch = umt.get_staff_pitch(row.cy, line_sep, line_height, row.is_bass)
            pitch = umt.get_pitch_from_staff_pitch(staff_pitch)
            song_input.loc[len(song_input)] = [
                row.state, row.cx, row.cy, row.line, measure, staff_pitch, pitch
            ]
      
    return song_input
            

def parse_song_notes(song_input, line_sep):
    # Initialize key signals and dictionary maps
    measure_start_x = 0
    keysig = {}
    acc = {}
    acc_map = {'s':1, 'f':-1, 'n':0}
    song_input = song_input.sort_values(by=['line','measure','cx'])

    # Apply key signal and accidentals to notes
    notes = pd.DataFrame(columns=['line', 'measure','pitch','x'])
    for index, row in song_input.iterrows():
        if row.state in 'sfn':
            # CLEANUP?
            has_target = np.any( 
                    (song_input.line==row.line)&
                    (song_input.measure==row.measure)&
                    (song_input.staff_pitch==row.staff_pitch)&
                    (song_input.cx - row.cx<2*line_sep)&
                    (song_input.cx - row.cx>0)
                )
            if has_target:
                # If accidental has target, add to temporary accidentals dict
                acc[row.staff_pitch] = acc_map[row.state]
            else:
                # If no target, add to permanent keysignature. Define as measure start
                keysig[row.staff_pitch%7] = acc_map[row.state]
                measure_start_x = row.cx

        if row.state in '1':
            # Check if note pitch should be influenced by accidentals or keysignature
            # If accidental applies, do not apply keysignature
            pitch = row.pitch
            if row.staff_pitch in acc.keys():
                pitch = row.pitch + acc[row.staff_pitch]
            elif row.staff_pitch%7 in keysig.keys():
                pitch = row.pitch + keysig[row.staff_pitch%7]
                # I choose to leave as full x
            notes.loc[len(notes)] = [int(row.line), int(row.measure), int(pitch), row.cx]
        if row.state == 'm':
            # Reset accidentals on new measure. Reset measure_start_x
            accidentals = {}
            measure_start_x = row.cx

    # Create string labels
    notes['string'] = notes.pitch.apply(
        lambda x: umt.get_pitch_as_string(x, sum(keysig.values()))
    )
    

    # Group cx into chords
    # CLEANUP?
    notes = notes.sort_values(by=['line','x'])
    xmin, xmax, dx = 0, 0, 2*line_sep
    xarr = notes.x.values
    for j in range(len(xarr)):
        x = xarr[j]
        if x>xmax or x<xmin:
            xmin = int(x)
            xmax = x+dx
        xarr[j] = xmin
    
    # Sort output for grouping chords
    notes = notes.sort_values(by=['line','measure','x','pitch'])
    return notes

