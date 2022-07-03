# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'load_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(383, 279)
        self.song_menu = QtWidgets.QComboBox(Form)
        self.song_menu.setGeometry(QtCore.QRect(140, 40, 69, 22))
        self.song_menu.setObjectName("song_menu")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(80, 10, 201, 20))
        self.label.setObjectName("label")
        self.load_song_button = QtWidgets.QPushButton(Form)
        self.load_song_button.setGeometry(QtCore.QRect(230, 40, 75, 23))
        self.load_song_button.setObjectName("load_song_button")
        self.new_song_button = QtWidgets.QPushButton(Form)
        self.new_song_button.setGeometry(QtCore.QRect(230, 70, 75, 23))
        self.new_song_button.setObjectName("new_song_button")
        self.songname = QtWidgets.QLineEdit(Form)
        self.songname.setGeometry(QtCore.QRect(110, 70, 111, 20))
        self.songname.setObjectName("songname")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(40, 70, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(30, 40, 91, 16))
        self.label_3.setObjectName("label_3")
        self.bpm_input = QtWidgets.QSpinBox(Form)
        self.bpm_input.setGeometry(QtCore.QRect(140, 110, 42, 22))
        self.bpm_input.setMinimum(2)
        self.bpm_input.setMaximum(8)
        self.bpm_input.setProperty("value", 4)
        self.bpm_input.setObjectName("bpm_input")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(40, 110, 91, 16))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Load Existing Song or Create New"))
        self.load_song_button.setText(_translate("Form", "Load"))
        self.new_song_button.setText(_translate("Form", "Create"))
        self.label_2.setText(_translate("Form", "New Song Name"))
        self.label_3.setText(_translate("Form", "Existing Songs"))
        self.label_4.setText(_translate("Form", "Beats in Measure"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

