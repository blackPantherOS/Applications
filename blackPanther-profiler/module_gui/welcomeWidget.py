# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'welcomeWidget.ui'
#
# Created: Mon Jun  8 22:54:14 2015
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

class Ui_welcomeWidget(object):
    def setupUi(self, welcomeWidget):
        welcomeWidget.setObjectName(_fromUtf8("welcomeWidget"))
        welcomeWidget.resize(569, 495)
        welcomeWidget.setStyleSheet(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(welcomeWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.label = QtGui.QLabel(welcomeWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("URW Gothic L"))
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(welcomeWidget)
        self.label_2.setMinimumSize(QtCore.QSize(34, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("FreeSans"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 1, QtCore.Qt.AlignTop)
        spacerItem1 = QtGui.QSpacerItem(25, 30, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 50, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 2, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 30, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 3, 0, 1, 1)
        self.labelProfilerIntro = QtGui.QLabel(welcomeWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelProfilerIntro.sizePolicy().hasHeightForWidth())
        self.labelProfilerIntro.setSizePolicy(sizePolicy)
        self.labelProfilerIntro.setMinimumSize(QtCore.QSize(351, 0))
        self.labelProfilerIntro.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("URW Gothic L"))
        font.setPointSize(11)
        self.labelProfilerIntro.setFont(font)
        self.labelProfilerIntro.setStyleSheet(_fromUtf8("color: rgb(234, 225, 228);"))
        self.labelProfilerIntro.setFrameShadow(QtGui.QFrame.Raised)
        self.labelProfilerIntro.setWordWrap(True)
        self.labelProfilerIntro.setObjectName(_fromUtf8("labelProfilerIntro"))
        self.gridLayout.addWidget(self.labelProfilerIntro, 3, 1, 1, 2)
        spacerItem4 = QtGui.QSpacerItem(25, 30, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 3, 3, 1, 1)
        self.frame_3 = QtGui.QFrame(welcomeWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 90))
        self.frame_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtGui.QFrame.Plain)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.labelStatus = QtGui.QLabel(self.frame_3)
        self.labelStatus.setGeometry(QtCore.QRect(400, 0, 90, 90))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelStatus.sizePolicy().hasHeightForWidth())
        self.labelStatus.setSizePolicy(sizePolicy)
        self.labelStatus.setMinimumSize(QtCore.QSize(90, 90))
        self.labelStatus.setMaximumSize(QtCore.QSize(90, 90))
        self.labelStatus.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.labelStatus.setAutoFillBackground(False)
        self.labelStatus.setStyleSheet(_fromUtf8(""))
        self.labelStatus.setLineWidth(0)
        self.labelStatus.setText(_fromUtf8(""))
        self.labelStatus.setPixmap(QtGui.QPixmap(_fromUtf8("module_gui/pics/logo2010.png")))
        self.labelStatus.setScaledContents(True)
        self.labelStatus.setMargin(0)
        self.labelStatus.setOpenExternalLinks(False)
        self.labelStatus.setObjectName(_fromUtf8("labelStatus"))
        self.frame_2 = QtGui.QFrame(self.frame_3)
        self.frame_2.setGeometry(QtCore.QRect(0, 40, 240, 40))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(240, 40))
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Plain)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.checkAutostart = QtGui.QCheckBox(self.frame_2)
        self.checkAutostart.setGeometry(QtCore.QRect(10, 10, 221, 21))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkAutostart.sizePolicy().hasHeightForWidth())
        self.checkAutostart.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("URW Gothic L"))
        font.setBold(True)
        font.setWeight(75)
        self.checkAutostart.setFont(font)
        self.checkAutostart.setObjectName(_fromUtf8("checkAutostart"))
        self.frame = QtGui.QFrame(self.frame_3)
        self.frame.setGeometry(QtCore.QRect(0, 10, 411, 20))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.HLine)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout.addWidget(self.frame_3, 4, 1, 1, 2)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem5, 5, 1, 1, 1)

        self.retranslateUi(welcomeWidget)
        QtCore.QMetaObject.connectSlotsByName(welcomeWidget)

    def retranslateUi(self, welcomeWidget):
        welcomeWidget.setWindowTitle(_translate("welcomeWidget", "Welcome", None))
        self.label.setStyleSheet(_translate("welcomeWidget", "color: rgb(234, 225, 228);", None))
        self.label.setText(_translate("welcomeWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'URW Gothic L\'; font-size:25pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:22pt;\">Welcome to blackPanther OS </span></p></body></html>", None))
        self.label_2.setText(_translate("welcomeWidget", "v14.x", None))
        self.labelProfilerIntro.setText(_translate("welcomeWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'URW Gothic L\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The blackPanther OS is a reliable, secure, fast and user friendly operating system. <br /><br />With blackPanther, you can connect to the internet, read your e-mails, work with your office documents, watch movies, play music, develop applications, play games and much more! <br /><br /><span style=\" font-weight:600;\">Wizard</span> will help you personalize your blackPanther workspace easily and quickly. Please click <span style=\" font-weight:600;\">next</span> in order to begin.</p></body></html>", None))
        self.labelStatus.setToolTip(_translate("welcomeWidget", "© Charles Barcza", None))
        self.checkAutostart.setText(_translate("welcomeWidget", "Run Profiler on System Startup", None))

