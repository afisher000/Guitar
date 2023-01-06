import cv2 as cv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import utils_image_processing as uip
import utils_music_theory as umt
import utils_model as um
import utils_io as uio


def remove_staff_lines(img):
     # Turn line column white if pixel above and below line is white
    is_line = (img.sum(axis=1)/img.shape[1]) < 127
    line_starts = np.logical_and(~is_line[:-1], is_line[1:]).nonzero()[0]+1
    line_ends = np.logical_and(is_line[:-1], ~is_line[1:]).nonzero()[0]+1
    
    for start, end in zip(line_starts, line_ends):
        line_fill = (img[start-1,:])&(img[end,:])
        img[start:end+1,:] = line_fill
    return img

    
def clean_music(img):
    # Compute line_sep and number of music lines
    is_horz_line = img.sum(axis=1)/img.shape[1]<127
    line_starts = np.logical_and(~is_horz_line[:-1], is_horz_line[1:]).nonzero()[0]
    line_sep = int((line_starts[4]-line_starts[0])//4)
    n_lines = int(len(line_starts)//5)

    # Remove white columns and vertical line connecting treble and bass
    is_white_col = img.sum(axis=0)/img.shape[0]==255
    img = img[:, ~is_white_col]
    is_vert_line = (img.sum(axis=0)/img.shape[0]) < 170
    img[:, is_vert_line] = 255


    # Fill bounding rects of staff contours, then floodfill white to isolate words
    words_img = img.copy()
    contours, _ = cv.findContours(~words_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cs = sorted(contours, key=cv.contourArea)[-n_lines:]
    for c in cs:
        x,y,w,h = cv.boundingRect(c)
        words_img[y:y+h, :] = 0
        cv.floodFill(words_img, None, (x+w//2, y+h//2), 255)

    # Combine with original to remove words
    no_words_img = cv.bitwise_or(
        img,
        cv.bitwise_not(words_img)
    )
    cv.imwrite('Test\\no_words.jpg', no_words_img)

    # Use white rows to separate staffs
    is_white_row = no_words_img.sum(axis=1)/no_words_img.shape[1]==255
    is_staff_start = np.logical_and(is_white_row[:-1], ~is_white_row[1:])
    is_staff_end = np.logical_and(~is_white_row[:-1], is_white_row[1:])
    staff_starts = np.nonzero(is_staff_start)[0]+1
    staff_ends = np.nonzero(is_staff_end)[0]+1

    # Make new image with equal height staff lines
    line_height = 12*line_sep
    size = (n_lines*line_height, words_img.shape[1])
    cleaned_img = np.full(size, 255, dtype=np.uint8)
    for j, (staff_start, staff_end) in enumerate(zip(staff_starts, staff_ends)):
        staff_lines = is_horz_line[staff_start:staff_end].nonzero()[0]+1
        staff_center = staff_start + int(staff_lines.sum()/len(staff_lines))
        print(staff_center)
        staff_idxs = np.arange(staff_start, staff_end)
        cleaned_img[staff_idxs - staff_center + int((j+.5)*line_height), :] = no_words_img[staff_idxs, :]

    return cleaned_img, line_sep, n_lines
    

def compute_stems_and_tails(img, notes, line_sep):
    # Operations to isolate note stems
    no_stems = uip.morphology_operation(img, (.25*line_sep, .25*line_sep), cv.MORPH_DILATE)
    hollowed_notes = ~((~img)&(no_stems))
    stems = uip.morphology_operation(hollowed_notes, (1.5*line_sep,1), cv.MORPH_CLOSE)
    dilated_stems = uip.morphology_operation(
        stems, (.25*line_sep, .25*line_sep), cv.MORPH_ERODE
    )
    stem_contours, _ = cv.findContours(~dilated_stems, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    notes = notes[notes.state!='\r']
    notes[['tails', 'is_stemmed']] = 0
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
        notes.loc[is_overlapping, ['is_stemmed']] = 1

    return notes


def separate_notations(notations, orig, line_sep):
    # 
    notations['total_pixel'] = notations.cx + notations.cy//(24*line_sep)*orig.shape[1]
    
    # Reset state as index
    notations = notations.set_index('state')
    
    # Get measures
    measures = notations.loc['m'].reset_index()

    # Get rests, add time column based on state
    rest_duration_map = {'q':.25, 'w':.5, 'e':1, 'r':2, 't':4}
    rests = notations.loc[notations.index.intersection(list('qwert'))].reset_index()
    rests['duration'] = rests.state.map(rest_duration_map)
    
    # Modifiers include accidentals and dots
    modifiers = notations.loc[notations.index.intersection(list('sfdn'))].reset_index()
    modifiers.loc[modifiers.state=='f', 'cy'] += .3*line_sep
    
    # Time signature
    timesig = notations.loc[notations.index.intersection(list('23468'))].reset_index()
    return measures, rests, modifiers, timesig

def compute_is_filled(fill_mask, notes):
    # Compute is_filled column for notes
    for index, (x,y,w,h) in notes[['x','y','w','h']].iterrows():
        is_filled = int(fill_mask[y:y+h, x:x+w].sum()>0)
        notes.loc[index, 'is_filled'] = is_filled
    notes.is_filled = notes.is_filled.astype(int)
    return notes
    
def remove_nonnotes(img, nonnotes, line_sep):
    for _, row in nonnotes.iterrows():
        if row.state!='\r':
            x,y,w,h = row[['x','y','w','h']]
            cv.rectangle(img, (x,y), (x+w,y+h), 255, -1)
    return img


def apply_note_modifiers(notes, modifiers, line_sep):
    # Drop dots by 1/4 of line sep
    modifiers.loc[modifiers.state=='d', 'cy'] += 0.25*line_sep
    
    # Apply accidentals to closest note
    notes = notes.reset_index(drop=True)
    column_dict = {
        's':'is_sharped',
        'f':'is_flatted',
        'n':'is_naturaled',
        'd':'is_dotted'
    }
    for col in column_dict.values():
        notes[col] = 0
    
    keysig_idxs = []
    for index, row in modifiers.iterrows():
        dists = np.abs(row[['cx','cy']] - notes[['cx','cy']]).values
        is_valid_note = np.logical_and(
            dists[:,1]<0.5*line_sep,
            dists[:,0]<3*line_sep
        )
        if sum(is_valid_note)>1:
            print('Found two notes that are sufficiently close to modifer!')
        elif sum(is_valid_note)==1:
            note_idx = np.where(is_valid_note)[0]
            notes.loc[note_idx, column_dict[row.state]] = 1
        else:
            if row.state in 'sf':
                keysig_idxs.append(index)
    
    keysig = modifiers.loc[keysig_idxs]
    if len(keysig.state.unique())>1:
        raise ValueError('Multiple accidental types in key signature')
    
    # Detect treble clef keysig
    keysig = keysig[keysig.cy<12*line_sep].reset_index(drop=True)
    return notes, keysig   
        
def separate_grouped_notes(closed_img, grouped_notes):
    # Create new structure than contains correct centroid and bounding rects for notes
    notes = grouped_notes[grouped_notes.state=='1'].copy().reset_index(drop=True)
    for index, row in grouped_notes.iterrows():
        if row.state in '234':
            rect = row[['x','y','w','h']].to_list()
            n_clusters = int(row.state)
            centers, bounding_rects = uip.get_clusters(rect, closed_img, n_clusters)
            for center, bounding_rect in zip(centers, bounding_rects):
                notes.loc[len(notes)] = ['1', center[1], center[0], *bounding_rect] 
    return notes


def apply_keysignature(notes, orig, keysig, measures, line_sep):
    # Initialize key signals and dictionary maps
    acc_map = {'s':1, 'f':-1, 'n':0}
    acc_staff_pitches = {}
    keysig_pitches = {}
    for pitch in umt.get_pitch(keysig.cy.values, line_sep):
        keysig_pitches[pitch%12] = keysig.loc[0, 'state']
    
    notes['staff_pitch'] = umt.get_staff_pitch(notes.cy.values, line_sep)
    notes['pitch'] = umt.get_pitch(notes.cy.values, line_sep)
    notes['total_pixel'] = notes.cx + notes.cy//(24*line_sep)*orig.shape[1]
    
    for index, row in pd.concat([notes, measures]).sort_values(by='total_pixel').iterrows():
        # Reset accidentals for new measure
        if row.state=='m':
            acc_staff_pitches = {}
        else:
            # Check for accidentals
            if row.is_sharped:
                notes.loc[index, 'pitch'] += 1
                acc_staff_pitches[row.staff_pitch] = 's'
            elif row.is_flatted:
                notes.loc[index, 'pitch'] -= 1
                acc_staff_pitches[row.staff_pitch] = 'f'
            elif row.is_naturaled:
                acc_staff_pitches[row.staff_pitch] = 'n'
            
            # Check if in accidentals (must be exact line)
            elif row.staff_pitch in acc_staff_pitches.keys():
                notes.loc[index, 'pitch'] += acc_map[acc_staff_pitches[row.staff_pitch]]
            
            # Check if in keysig
            elif row.pitch%12 in keysig_pitches.keys():
                notes.loc[index, 'pitch'] += acc_map[keysig_pitches[row.pitch%12]]

    notes['label'] = notes.pitch.apply(lambda x: umt.get_pitch_as_string(x, keysig=-1))
    return notes

def compute_beats(notes, rests, line_sep):
    notes_and_rests = pd.concat([notes, rests]).sort_values(by='total_pixel').reset_index(drop=True)
    
    end_beats = {0}
    chord_idxs = np.hstack([
        -1, 
        np.where(np.diff(notes_and_rests.total_pixel.values)>1.5*line_sep)[0],
        len(notes_and_rests)
    ])
    for j in range(len(chord_idxs)-1):
        min_end_beat = min(end_beats)
        
        durations = notes_and_rests.loc[chord_idxs[j]+1:chord_idxs[j+1], 'duration']
        notes_and_rests.loc[chord_idxs[j]+1:chord_idxs[j+1],'beat'] = min_end_beat
        
        
        end_beats.remove(min_end_beat)
        end_beats.update(min_end_beat + np.unique(durations))
    
    notes = notes_and_rests[notes_and_rests.state=='1']
    return notes

