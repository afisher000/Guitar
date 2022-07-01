from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time

plotitem = pg.PlotItem()
plotitem.plot([1,2,3],[2,3,4])
widget = pg.PlotWidget(plotItem=plotitem)

Ntext = 500
textitems=[]
for j in range(Ntext):
    textitem = pg.TextItem(text = 'a')
    textitem.setPos(0,0)
    widget.addItem(textitem)
    textitems.append(textitem) 
    
widget.setXRange(0,3)
widget.setYRange(0,4)
widget.show()

start_time = time()
for j in range(Ntext):
    textitems[j].setPos(1,1+j/Ntext)
end_time = time()
print(f'Elapsed: {end_time-start_time}')

start_time = time()
textitems[2].setPos(2,1)
end_time = time()
print(f'Elapsed: {end_time-start_time}')



start_time = time()
widget.removeItem(textitems[4])
end_time = time()
print(f'Elapsed: {end_time-start_time}')

