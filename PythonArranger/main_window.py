# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Layout(object):
    def setupUi(self, Layout):
        Layout.setObjectName("Layout")
        Layout.resize(1113, 904)
        self.canvas = PlotWidget(Layout)
        self.canvas.setGeometry(QtCore.QRect(140, 20, 961, 871))
        self.canvas.setObjectName("canvas")
        self.save_button = QtWidgets.QPushButton(Layout)
        self.save_button.setGeometry(QtCore.QRect(10, 20, 111, 31))
        self.save_button.setObjectName("save_button")
        self.label = QtWidgets.QLabel(Layout)
        self.label.setGeometry(QtCore.QRect(10, 60, 81, 16))
        self.label.setObjectName("label")
        self.stepsize_display = QtWidgets.QLineEdit(Layout)
        self.stepsize_display.setGeometry(QtCore.QRect(90, 60, 41, 20))
        self.stepsize_display.setObjectName("stepsize_display")

        self.retranslateUi(Layout)
        QtCore.QMetaObject.connectSlotsByName(Layout)

    def retranslateUi(self, Layout):
        _translate = QtCore.QCoreApplication.translate
        Layout.setWindowTitle(_translate("Layout", "Form"))
        self.save_button.setText(_translate("Layout", "Save"))
        self.label.setText(_translate("Layout", "Stepsize (beats)"))

from pyqtgraph import PlotWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Layout = QtWidgets.QWidget()
    ui = Ui_Layout()
    ui.setupUi(Layout)
    Layout.show()
    sys.exit(app.exec_())

