# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'profilerMain2.ui'
#
# Created: Fri May 29 09:14:04 2015
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

class Ui_profilerUI(object):
    def setupUi(self, profilerUI):
        profilerUI.setObjectName(_fromUtf8("profilerUI"))
        profilerUI.resize(790, 570)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(profilerUI.sizePolicy().hasHeightForWidth())
        profilerUI.setSizePolicy(sizePolicy)
        profilerUI.setMinimumSize(QtCore.QSize(790, 570))
        profilerUI.setMaximumSize(QtCore.QSize(790, 570))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("URW Gothic L"))
        font.setPointSize(10)
        profilerUI.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/raw/pics/cr64-app-profiler.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        profilerUI.setWindowIcon(icon)
        profilerUI.setStyleSheet(_fromUtf8("#profiler{\n"
"    background-image: url(:/raw/pics/bg.png);\n"
"       background-repeat: no-repeat;\n"
"       background-position: left top;\n"
"       background-color: #642437;\n"
"       alternate-background-color: gray;\n"
"       selection-background-color: gray;\n"
"}\n"
""))
        self.gridLayout_3 = QtGui.QGridLayout(profilerUI)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.profiler = QtGui.QWidget(profilerUI)
        self.profiler.setObjectName(_fromUtf8("profiler"))
        self.gridLayout_2 = QtGui.QGridLayout(self.profiler)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(-1)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.labelMenu = QtGui.QLabel(self.profiler)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("URW Gothic L"))
        font.setPointSize(11)
        self.labelMenu.setFont(font)
        self.labelMenu.setAutoFillBackground(False)
        self.labelMenu.setStyleSheet(_fromUtf8("color: rgb(36, 42, 58);\n"
"padding-top: 10px;"))
        self.labelMenu.setLineWidth(2)
        self.labelMenu.setText(_fromUtf8(""))
        self.labelMenu.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelMenu.setIndent(20)
        self.labelMenu.setObjectName(_fromUtf8("labelMenu"))
        self.gridLayout.addWidget(self.labelMenu, 1, 0, 3, 2)
        spacerItem = QtGui.QSpacerItem(180, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 80, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.mainStack = QtGui.QStackedWidget(self.profiler)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainStack.sizePolicy().hasHeightForWidth())
        self.mainStack.setSizePolicy(sizePolicy)
        self.mainStack.setStyleSheet(_fromUtf8("QStackedWidget#mainStack{background-color:rgba(255, 255, 255,0);\n"
"margin: 0px;\n"
"border-radius: 0px;\n"
"color: white;\n"
"}"))
        self.mainStack.setFrameShape(QtGui.QFrame.NoFrame)
        self.mainStack.setFrameShadow(QtGui.QFrame.Plain)
        self.mainStack.setLineWidth(0)
        self.mainStack.setObjectName(_fromUtf8("mainStack"))
        self.page = QtGui.QWidget()
        self.page.setObjectName(_fromUtf8("page"))
        self.mainStack.addWidget(self.page)
        self.verticalLayout_4.addWidget(self.mainStack)
        self.gridLayout_2.addLayout(self.verticalLayout_4, 0, 1, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(1)
        self.horizontalLayout_2.setContentsMargins(0, 0, -1, 0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.buttonCancel = QtGui.QPushButton(self.profiler)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("URW Gothic L"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.buttonCancel.setFont(font)
        self.buttonCancel.setCheckable(False)
        self.buttonCancel.setFlat(False)
        self.buttonCancel.setObjectName(_fromUtf8("buttonCancel"))
        self.horizontalLayout_2.addWidget(self.buttonCancel)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.buttonBack = QtGui.QPushButton(self.profiler)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("URW Gothic L"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.buttonBack.setFont(font)
        self.buttonBack.setCheckable(False)
        self.buttonBack.setFlat(False)
        self.buttonBack.setObjectName(_fromUtf8("buttonBack"))
        self.horizontalLayout_2.addWidget(self.buttonBack)
        self.buttonNext = QtGui.QPushButton(self.profiler)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("URW Gothic L"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.buttonNext.setFont(font)
        self.buttonNext.setCheckable(False)
        self.buttonNext.setFlat(False)
        self.buttonNext.setObjectName(_fromUtf8("buttonNext"))
        self.horizontalLayout_2.addWidget(self.buttonNext)
        self.buttonFinish = QtGui.QPushButton(self.profiler)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("URW Gothic L"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.buttonFinish.setFont(font)
        self.buttonFinish.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.buttonFinish.setCheckable(False)
        self.buttonFinish.setFlat(False)
        self.buttonFinish.setObjectName(_fromUtf8("buttonFinish"))
        self.horizontalLayout_2.addWidget(self.buttonFinish)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 2)
        self.gridLayout_3.addWidget(self.profiler, 0, 0, 1, 1)

        self.retranslateUi(profilerUI)
        self.mainStack.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(profilerUI)

    def retranslateUi(self, profilerUI):
        profilerUI.setWindowTitle(_translate("profilerUI", "Wizard Desktop", None))
        self.buttonCancel.setStyleSheet(_translate("profilerUI", "color: rgb(255, 255, 255);", None))
        self.buttonCancel.setText(_translate("profilerUI", "Cancel", None))
        self.buttonBack.setStyleSheet(_translate("profilerUI", "color: rgb(255, 255, 255);", None))
        self.buttonBack.setText(_translate("profilerUI", "Back", None))
        self.buttonNext.setStyleSheet(_translate("profilerUI", "color: rgb(255, 255, 255);", None))
        self.buttonNext.setText(_translate("profilerUI", "Next", None))
        self.buttonFinish.setText(_translate("profilerUI", "Finish", None))

import raw_rc
