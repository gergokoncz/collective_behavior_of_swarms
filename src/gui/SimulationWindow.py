# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SimulationWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ForagingAntsSimulation(object):
    def setupUi(self, ForagingAntsSimulation):
        ForagingAntsSimulation.setObjectName("ForagingAntsSimulation")
        ForagingAntsSimulation.resize(700, 700)
        self.startButton = QtWidgets.QPushButton(ForagingAntsSimulation)
        self.startButton.setGeometry(QtCore.QRect(20, 10, 81, 25))
        self.startButton.setObjectName("startButton")
        self.stopButton = QtWidgets.QPushButton(ForagingAntsSimulation)
        self.stopButton.setGeometry(QtCore.QRect(110, 10, 81, 25))
        self.stopButton.setObjectName("stopButton")
        self.storedFoodLabel = QtWidgets.QLabel(ForagingAntsSimulation)
        self.storedFoodLabel.setGeometry(QtCore.QRect(230, 10, 91, 21))
        self.storedFoodLabel.setText("")
        self.storedFoodLabel.setObjectName("storedFoodLabel")

        self.retranslateUi(ForagingAntsSimulation)
        QtCore.QMetaObject.connectSlotsByName(ForagingAntsSimulation)

    def retranslateUi(self, ForagingAntsSimulation):
        _translate = QtCore.QCoreApplication.translate
        ForagingAntsSimulation.setWindowTitle(_translate("ForagingAntsSimulation", "Dialog"))
        self.startButton.setText(_translate("ForagingAntsSimulation", "start"))
        self.stopButton.setText(_translate("ForagingAntsSimulation", "stop"))
