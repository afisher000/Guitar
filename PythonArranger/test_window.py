# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test_window.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(30, 90, 256, 192))
        self.graphicsView.setObjectName("graphicsView")
        self.slope_str = QtWidgets.QLineEdit(self.centralwidget)
        self.slope_str.setGeometry(QtCore.QRect(40, 60, 71, 20))
        self.slope_str.setObjectName("slope_str")
        self.intercept = QtWidgets.QLineEdit(self.centralwidget)
        self.intercept.setGeometry(QtCore.QRect(120, 60, 71, 20))
        self.intercept.setObjectName("intercept")
        self.plot_button = QtWidgets.QPushButton(self.centralwidget)
        self.plot_button.setGeometry(QtCore.QRect(210, 60, 56, 17))
        self.plot_button.setObjectName("plot_button")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 40, 35, 10))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(140, 40, 35, 10))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 18))
        self.menubar.setObjectName("menubar")
        self.menumainwindow = QtWidgets.QMenu(self.menubar)
        self.menumainwindow.setObjectName("menumainwindow")
        self.menuedit = QtWidgets.QMenu(self.menubar)
        self.menuedit.setObjectName("menuedit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menumainwindow.menuAction())
        self.menubar.addAction(self.menuedit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.plot_button.setText(_translate("MainWindow", "Plot"))
        self.label.setText(_translate("MainWindow", "Slope"))
        self.label_2.setText(_translate("MainWindow", "Intercept"))
        self.menumainwindow.setTitle(_translate("MainWindow", "file"))
        self.menuedit.setTitle(_translate("MainWindow", "edit"))
