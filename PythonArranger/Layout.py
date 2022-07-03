# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Layout.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Layout(object):
    def setupUi(self, Layout):
        Layout.setObjectName("Layout")
        Layout.resize(400, 300)
        self.canvas = PlotWidget(Layout)
        self.canvas.setGeometry(QtCore.QRect(10, 10, 371, 271))
        self.canvas.setObjectName("canvas")

        self.retranslateUi(Layout)
        QtCore.QMetaObject.connectSlotsByName(Layout)

    def retranslateUi(self, Layout):
        _translate = QtCore.QCoreApplication.translate
        Layout.setWindowTitle(_translate("Layout", "Form"))

from pyqtgraph import PlotWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Layout = QtWidgets.QWidget()
    ui = Ui_Layout()
    ui.setupUi(Layout)
    Layout.show()
    sys.exit(app.exec_())

