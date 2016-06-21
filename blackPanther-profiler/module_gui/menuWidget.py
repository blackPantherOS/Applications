# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menuWidget2.ui'
#
# Created: Fri May 29 09:01:06 2015
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_menuWidget(object):
    def setupUi(self, menuWidget):
        menuWidget.setObjectName(_fromUtf8("menuWidget"))
        menuWidget.resize(579, 519)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(menuWidget.sizePolicy().hasHeightForWidth())
        menuWidget.setSizePolicy(sizePolicy)
        menuWidget.setStyleSheet(_fromUtf8("\n"
"QLabel#labelMenuDescription{\n"
"     border-style: outset;\n"
"     border-color: beige;\n"
"     border-width: 1px;\n"
"}"))
        self.gridLayout = QtGui.QGridLayout(menuWidget)
        self.gridLayout.setMargin(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(menuWidget)
        self.label.setMinimumSize(QtCore.QSize(487, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("URW Gothic L"))
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(menuWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("URW Gothic L"))
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pictureMenuStyles = QtGui.QLabel(menuWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pictureMenuStyles.sizePolicy().hasHeightForWidth())
        self.pictureMenuStyles.setSizePolicy(sizePolicy)
        self.pictureMenuStyles.setMinimumSize(QtCore.QSize(320, 260))
        self.pictureMenuStyles.setMaximumSize(QtCore.QSize(320, 260))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("URW Gothic L"))
        font.setPointSize(10)
        self.pictureMenuStyles.setFont(font)
        self.pictureMenuStyles.setFrameShape(QtGui.QFrame.NoFrame)
        self.pictureMenuStyles.setText(_fromUtf8(""))
        self.pictureMenuStyles.setScaledContents(False)
        self.pictureMenuStyles.setWordWrap(True)
        self.pictureMenuStyles.setObjectName(_fromUtf8("pictureMenuStyles"))
        self.horizontalLayout_3.addWidget(self.pictureMenuStyles)
        spacerItem1 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.menuLabel = QtGui.QLabel(menuWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("URW Gothic L"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.menuLabel.setFont(font)
        self.menuLabel.setStyleSheet(_fromUtf8("color: rgb(234, 225, 228);"))
        self.menuLabel.setObjectName(_fromUtf8("menuLabel"))
        self.verticalLayout_3.addWidget(self.menuLabel)
        self.menuStyles = QtGui.QComboBox(menuWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("URW Gothic L"))
        font.setPointSize(10)
        self.menuStyles.setFont(font)
        self.menuStyles.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.menuStyles.setObjectName(_fromUtf8("menuStyles"))
        self.menuStyles.addItem(_fromUtf8(""))
        self.menuStyles.addItem(_fromUtf8(""))
        self.menuStyles.addItem(_fromUtf8(""))
        self.menuStyles.addItem(_fromUtf8(""))
        self.verticalLayout_3.addWidget(self.menuStyles)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem2)
        self.labelMenuDescription = QtGui.QLabel(menuWidget)
        self.labelMenuDescription.setMinimumSize(QtCore.QSize(0, 150))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.labelMenuDescription.setFont(font)
        self.labelMenuDescription.setStyleSheet(_fromUtf8("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 81), stop:0.00537634 rgba(0, 0, 0, 80), stop:1 rgba(250, 250, 230, 80));\n"
"border: 1px solid rgb(236, 236, 236, 80);\n"
"padding:5px;\n"
"color: rgb(234, 225, 228);"))
        self.labelMenuDescription.setScaledContents(False)
        self.labelMenuDescription.setWordWrap(True)
        self.labelMenuDescription.setIndent(0)
        self.labelMenuDescription.setObjectName(_fromUtf8("labelMenuDescription"))
        self.verticalLayout_3.addWidget(self.labelMenuDescription)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem3, 0, 1, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 50, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem4, 2, 1, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(30, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 1, 0, 1, 1)
        spacerItem6 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem6, 1, 2, 1, 1)

        self.retranslateUi(menuWidget)
        QtCore.QMetaObject.connectSlotsByName(menuWidget)

    def retranslateUi(self, menuWidget):
        menuWidget.setWindowTitle(_translate("menuWidget", "Menu", None))
        self.label.setStyleSheet(_translate("menuWidget", "color: rgb(234, 225, 228);", None))
        self.label.setText(_translate("menuWidget", "Choose a Menu Style", None))
        self.label_2.setStyleSheet(_translate("menuWidget", "color: rgb(234, 225, 228);", None))
        self.label_2.setText(_translate("menuWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'URW Gothic L\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You can also customize your<span style=\" font-weight:600;\"> Desktop Menu</span> as you like. Please choose one from the following styles.</p></body></html>", None))
        self.pictureMenuStyles.setStyleSheet(_translate("menuWidget", "#pictureMenuStyles{\n"
"border: 1px solid rgb(255, 255, 255);\n"
"}", None))
        self.menuLabel.setText(_translate("menuWidget", "Menu Styles:", None))
        self.menuStyles.setItemText(0, _translate("menuWidget", "Kick-off Menu", None))
        self.menuStyles.setItemText(1, _translate("menuWidget", "Simple Menu", None))
        self.menuStyles.setItemText(2, _translate("menuWidget", "Lancelot Menu", None))
        self.menuStyles.setItemText(3, _translate("menuWidget", "App Menu", None))
        self.labelMenuDescription.setText(_translate("menuWidget", "Sample", None))

