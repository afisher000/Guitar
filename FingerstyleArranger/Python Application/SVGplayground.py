# -*- coding: utf-8 -*-
"""
Testing how to put SVG data in Tkinter window
"""


import tkinter as tk
from tkinter import ttk
import io
import time
from svglib.svglib import svg2rlg
from PIL import Image,ImageTk
from reportlab.graphics import renderPDF, renderPM
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class SVG():
    def __init__(self):
        self.svg_list = []
        self.width = 0
        self.height = 0
        self.templates = self.__generate_templates()
        
    def __generate_templates(self):
        templates = {}
        templates["create"] = "<svg width='{}px' height='{}px' xmlns='http://www.w3.org/2000/svg' version='1.1' xmlns:xlink='http://www.w3.org/1999/xlink'>\n"
        templates["finalize"] = "</svg>"
        templates["circle"] = "    <circle stroke='{}' stroke-width='{}px' fill='{}' r='{}' cy='{}' cx='{}' />\n"
        templates["line"] = "    <line stroke='{}' stroke-width='{}px' y2='{}' x2='{}' y1='{}' x1='{}' />\n"
        templates["rectangle"] = "    <rect fill='{}' stroke='{}' stroke-width='{}px' width='{}' height='{}' y='{}' x='{}' ry='{}' rx='{}' />\n"
        templates["text"] = "    <text x='{}' y = '{}' font-size='{}px'>{}</text>\n"
        templates["ellipse"] = "    <ellipse cx='{}' cy='{}' rx='{}' ry='{}' fill='{}' stroke='{}' stroke-width='{}' />\n"
        return templates
    
    def __add_to_svg(self,text):
        self.svg_list.append(str(text))
        
    def create(self,width,height):
        self.width = width
        self.height = height
        self.svg_list.clear()
        self.__add_to_svg(self.templates["create"].format(width,height))

    def fill(self,Fill):
        self.rectangle(self.width,self.height,0,0,Fill,Fill,0,0,0)
    
    def circle(self, stroke, strokewidth, fill, r, cx, cy):
        self.__add_to_svg(self.templates["circle"].format(stroke, strokewidth, fill, r, cy, cx))
        
    def text(self,rx,ry):
        self.__add_to_svg(self.templates["text"].format(rx,ry,12,'x'))

    def rectangle(self, width, height, x, y, fill, stroke, strokewidth, radiusx, radiusy):
        self.__add_to_svg(self.templates["rectangle"].format(fill, stroke, strokewidth, width, height, y, x, radiusy, radiusx))


    def save(self, path):
        self.__add_to_svg(self.templates["finalize"])
        f = open(path, "w+")
        for idx in range(len(self.svg_list)):    
            f.write(str(self.svg_list[idx]))
        f.close()


def create_SVG():
    s = SVG()
    s.create(456,492)
    s.fill("#A0A0FF") 
    for j in range(500):
        #s.circle("#000080",4,"#0000FF",32,random.randrange(100,500,10),random.randrange(100,500,10))
        s.text(random.randrange(100,500,10),random.randrange(100,500,10))
    s.save("test.svg")


def get_coords(event):
    print(event.x,event.y)
    
root = tk.Tk()
root.geometry("600x600")
root.configure(background='grey')

create_SVG()
drawing = svg2rlg('test.svg')
renderPM.drawToFile(drawing,"test.png",fmt='PNG')
img = ImageTk.PhotoImage(Image.open('test.png'))
#label = tk.Label(root,image=img)
#label.pack()
tk.Label(root,text='Label').grid(row=0,column=1)

fig,ax = plt.subplots()
canvas = tk.Canvas(root,width=500,height=600)
canvas.grid(row=0,column=0)
canvas_image = canvas.create_image(0,0,image=img)


#def callback():
#    for idx in range(30):
#        print(idx)
#        create_SVG()
#        drawing = svg2rlg('test.svg')
#        renderPM.drawToFile(drawing,"test.png",fmt='PNG')
#        img = ImageTk.PhotoImage(Image.open('test.png'))
#        canvas.itemconfig(canvas_image,image=img)
#        root.update()
#callback()

canvas.bind('<Button-1>', get_coords) #Get coordinates on canvas

root.mainloop()





















