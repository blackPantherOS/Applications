#!/usr/bin/env python
# coding=UTF-8
#
# Generated by pykdeuic4 from src/migration/gui/ui/usersWidget.ui on Fri Jul  4 12:37:34 2014
#
# WARNING! All changes to this file will be lost.
from PyKDE4 import kdecore
from PyKDE4 import kdeui
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_usersWidget(object):
    def setupUi(self, usersWidget):
        usersWidget.setObjectName(_fromUtf8("usersWidget"))
        usersWidget.resize(600, 406)
        self.gridLayout = QtGui.QGridLayout(usersWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 18, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 3, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 17, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem3, 2, 2, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.listUsers = QtGui.QListWidget(usersWidget)
        self.listUsers.setObjectName(_fromUtf8("listUsers"))
        self.verticalLayout.addWidget(self.listUsers)
        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 2)

        self.retranslateUi(usersWidget)
        QtCore.QMetaObject.connectSlotsByName(usersWidget)

    def retranslateUi(self, usersWidget):
        usersWidget.setWindowTitle(kdecore.i18n("Users"))


def encode(text):
    return text.encode('utf-8')
    