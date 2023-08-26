# %%
import cv2 as cv
import numpy as np
import pandas as pd
import utils_io as uio
import utils_image_processing as uip
import os
import matplotlib.pyplot as plt
img_file = 'test.jpg'
img_folder = 'Images'

# Make sure image folder exists
if not os.path.exists(img_folder):
    os.mkdir(img_folder)

img = uio.import_song(img_file)

def draw_circles(orig, no_lines, ):
    color_img = cv.cvtColor(orig, cv.COLOR_GRAY2BGR)
    circles = cv.HoughCircles(no_lines, cv.HOUGH_GRADIENT, 1, 20, 
        param1=50, param2=10, minRadius=1, maxRadius=30
    )
    if circles is None:
        return color_img
    circles = np.uint16(np.around(circles))
    for j in circles[0,:]:
        print(j)
        cv.circle(color_img, (j[0], j[1]), j[2], (0,255,0), 2)
        cv.circle(color_img, (j[0], j[1]), 2, (0,0,255), 3)
    return color_img

def draw_lines(orig, lines_img):
    lines = cv.HoughLines(~lines_img, 1, np.pi/180, 800)
    color_img = cv.cvtColor(orig, cv.COLOR_GRAY2BGR)
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0, y0 = a*rho, b*rho
        line_length = 4000
        x1 = int(x0 + line_length*(-b))
        y1 = int(y0 + line_length*(a))
        x2 = int(x0 - line_length*(-b))
        y2 = int(y0 - line_length*(a))
        cv.line(color_img,(x1,y1),(x2,y2),(0,255,0),2)
    return color_img

# Find contours of staff
no_lines = uip.morphology_operation(img, (8,1), cv.MORPH_CLOSE)
cv.imwrite(os.path.join(img_folder, 'no lines.jpg'), no_lines)
hlines = cv.bitwise_or(img, ~no_lines)
hlines = uip.morphology_operation(hlines, (1, 50), cv.MORPH_CLOSE)
hlines = uip.morphology_operation(hlines, (1, 250), cv.MORPH_OPEN)

# Identify and draw lines
color_img = draw_lines(img, hlines)
# uio.show_image(color_img, reduce=0)


color_img = draw_circles(img, no_lines)
uio.show_image(color_img, reduce=1)
# Apply transformation so lines are horizontal (four corners)

# img = uip.morphology_operation(img, (10,15), cv.MORPH_OPEN)

# img = uip.morphology_operation(img, (1,8), cv.MORPH_CLOSE)

# img = uip.morphology_operation(img, (10,10), cv.MORPH_OPEN)
# cv.imshow('edges', edges)
# cv.waitKey(0)
# cv.destroyAllWindows()
cv.imwrite(os.path.join(img_folder, 'lines detected.jpg'), color_img)



# %%
