#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created: Fri Dec 25 00:40:32 2009
#
# Copyrighted by Charles Barcza * blackPanther Europe
# kbarcza AT blackpanther DOT hu * www.blackpanther.hu
#

import sys, os
import commands

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *

class GetInternet():
    def __init__(self):
      self.checkInternet = commands.getoutput('test -n \"`ping -c 1 google.com | grep \'PING google.com\'`\" || echo NetNotFound')

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.Info = GetInternet()
	
	binDir = os.path.dirname(os.path.realpath( __file__ ))
	sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
        
	translator = QTranslator()
	translator.load('ds_' + QLocale.system().name(), binDir+'/lang')
	app.installTranslator(translator)

        DS.setObjectName("DS")
        DS.resize(800, 600)
        DS.setSizeGripEnabled(True)
        
        self.groupBox = QtGui.QGroupBox(DS)
        self.groupBox.setGeometry(QtCore.QRect(10, 50, 771, 541))
        self.groupBox.setObjectName("groupBox")

        self.select_kde4 = QtGui.QCommandLinkButton(self.groupBox)
        self.select_kde4.setGeometry(QtCore.QRect(70, 220, 211, 31))
        self.select_kde4.setObjectName("select_kde4")
	self.connect(self.select_kde4,QtCore.SIGNAL("clicked()"),self.slotSelectKde)

        self.select_gnome = QtGui.QCommandLinkButton(self.groupBox)
        self.select_gnome.setGeometry(QtCore.QRect(490, 220, 211, 31))
        self.select_gnome.setObjectName("select_gnome")
	self.connect(self.select_gnome,QtCore.SIGNAL("clicked()"),self.slotSelectGnome)

        self.kde_frame = QtGui.QFrame(self.groupBox)
        self.kde_frame.setGeometry(QtCore.QRect(30, 30, 291, 186))
        self.kde_frame.setStyleSheet("background-image: url(images/blackPanther-kde4.jpeg);")
        self.kde_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.kde_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.kde_frame.setObjectName("kde_frame")

        self.gnome_frame = QtGui.QFrame(self.groupBox)
        self.gnome_frame.setGeometry(QtCore.QRect(450, 30, 291, 186))
        self.gnome_frame.setStyleSheet("background-image: url(images/blackPanther-gnome3.jpeg);")
        self.gnome_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.gnome_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.gnome_frame.setObjectName("gnome_frame")

        self.toolBox = QtGui.QToolBox(self.groupBox)
        self.toolBox.setGeometry(QtCore.QRect(0, 250, 761, 291))
        self.toolBox.setObjectName("toolBox")
        self.page = QtGui.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 751, 225))
        self.page.setObjectName("page")

        self.select_other = QtGui.QCommandLinkButton(self.page)
        self.select_other.setGeometry(QtCore.QRect(480, 190, 211, 31))
        self.select_other.setObjectName("select_other")
        self.connect(self.select_other,QtCore.SIGNAL("clicked()"),self.slotSelectOther)

        self.select_openbox = QtGui.QCommandLinkButton(self.page)
        self.select_openbox.setGeometry(QtCore.QRect(50, 190, 211, 31))
        self.select_openbox.setObjectName("select_openbox")
	self.connect(self.select_openbox,QtCore.SIGNAL("clicked()"),self.slotSelectOpenbox)

        self.frame_windowmaker = QtGui.QFrame(self.page)
        self.frame_windowmaker.setGeometry(QtCore.QRect(440, 0, 291, 186))
        self.frame_windowmaker.setStyleSheet("background-image: url(images/blackPanther-other.jpeg);")
        self.frame_windowmaker.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_windowmaker.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_windowmaker.setObjectName("frame_windowmaker")

        self.openbox_frame = QtGui.QFrame(self.page)
        self.openbox_frame.setGeometry(QtCore.QRect(20, 0, 291, 186))
        self.openbox_frame.setStyleSheet("background-image: url(images/blackPanther-openbox.jpeg);")
        self.openbox_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.openbox_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.openbox_frame.setObjectName("openbox_frame")

        self.toolBox.addItem(self.page, "")
        self.page_2 = QtGui.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 751, 225))
        self.page_2.setObjectName("page_2")

        self.select_e17 = QtGui.QCommandLinkButton(self.page_2)
        self.select_e17.setGeometry(QtCore.QRect(480, 190, 211, 31))
        self.select_e17.setObjectName("select_e17")
	self.connect(self.select_e17,QtCore.SIGNAL("clicked()"),self.slotSelectE17)

        self.select_lxde = QtGui.QCommandLinkButton(self.page_2)
        self.select_lxde.setGeometry(QtCore.QRect(50, 190, 211, 31))
        self.select_lxde.setObjectName("select_lxde")
	self.connect(self.select_lxde,QtCore.SIGNAL("clicked()"),self.slotSelectLxde)

        self.e17_frame = QtGui.QFrame(self.page_2)
        self.e17_frame.setGeometry(QtCore.QRect(440, 0, 291, 186))
        self.e17_frame.setStyleSheet("background-image: url(images/blackPanther-e17.jpeg);")
        self.e17_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.e17_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.e17_frame.setObjectName("e17_frame")

        self.lxde_frame = QtGui.QFrame(self.page_2)
        self.lxde_frame.setGeometry(QtCore.QRect(20, 0, 291, 186))
        self.lxde_frame.setStyleSheet("background-image: url(images/blackPanther-lxde.jpeg);")
        self.lxde_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lxde_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.lxde_frame.setObjectName("lxde_frame")

        self.toolBox.addItem(self.page_2, "")
        self.frame = QtGui.QFrame(DS)
        self.frame.setGeometry(QtCore.QRect(10, 0, 771, 51))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(120, 0, 471, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setWeight(75)
        font.setItalic(False)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(50, 30, 631, 20))
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.settings_button = QtGui.QPushButton(self.frame)
        self.settings_button.setEnabled(True)
        self.settings_button.setGeometry(QtCore.QRect(680, 20, 81, 25))
        self.settings_button.setObjectName("settings_button")
        self.connect(self.settings_button,QtCore.SIGNAL("clicked()"),self.slotDevSettings)

        self.retranslateUi(DS)
        self.toolBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(DS)

    def retranslateUi(self, DS):
        DS.setWindowTitle(QtGui.QApplication.translate("DS", "blackPanther DS v0.1", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("DS", "Available desktop environments", None, QtGui.QApplication.UnicodeUTF8))
        self.select_kde4.setText(QtGui.QApplication.translate("DS",  "KDE4 (Default Installed)", None, QtGui.QApplication.UnicodeUTF8))
        self.select_gnome.setText(QtGui.QApplication.translate("DS",  "Gnome (for light PC)", None, QtGui.QApplication.UnicodeUTF8))
        self.select_other.setText(QtGui.QApplication.translate("DS",  "WindowMaker (other)", None, QtGui.QApplication.UnicodeUTF8))
        self.select_openbox.setText(QtGui.QApplication.translate("DS",  "Openbox (very poor PC)", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), QtGui.QApplication.translate("DS",  "Two more ultra easy desktops alternatives (click here...)", None, QtGui.QApplication.UnicodeUTF8))
        self.select_e17.setText(QtGui.QApplication.translate("DS",  "e17 (for poor PC)", None, QtGui.QApplication.UnicodeUTF8))
        self.select_lxde.setText(QtGui.QApplication.translate("DS",  "LXDE (for poor PC)", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QtGui.QApplication.translate("DS",  "Alternate desktops for poor machines", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DS", "blackPanther OS Desktop Selector", None, QtGui.QApplication.UnicodeUTF8))
        if (self.Info.checkInternet=='NetNotFound'):
    	    self.label_2.setText(QtGui.QApplication.translate("DS",  "Please select a desktop for your default desktop.(<u>you need</u> to install an active internet connection !).", None, QtGui.QApplication.UnicodeUTF8))
        else:
    	    self.label_2.setText(QtGui.QApplication.translate("DS",  "Please select a desktop for your default desktop. (To install the internet connection is <u>OK</u>).", None, QtGui.QApplication.UnicodeUTF8))
        self.settings_button.setText(QtGui.QApplication.translate("DS",  "Settings", None, QtGui.QApplication.UnicodeUTF8))

    def slotDevSettings(self):
	DS.hide()
        os.popen('drakconnect')
        os.popen('test -n \"`ping -c 1 google.com | grep \'PING google.com\'`\" || kdialog --error \"Error in internet connecion! Please try configure again..\"')
	DS.show()
 
    def slotSelectKde(self):
        sys.exit()

    def slotSelectGnome(self):
        os.popen('gurpmi2 gnome-desktop-environment-minimal|| kdialog --error "Install Aborted! The Default KDE4 Desktop Will Be Used"')
        sys.exit()

    def slotSelectLxde(self):
        os.popen('gurpmi2 lxde-desktop-environment|| kdialog --error "Install Aborted! The Default KDE4 Desktop Will Be Used"')
        sys.exit()

    def slotSelectE17(self):
        os.popen('gurpmi2 e17-desktop-environment-minimal || kdialog --error "Install Aborted! The Default KDE4 Desktop Will Be Used"')
        sys.exit()

    def slotSelectOpenbox(self):
        os.popen('gurpmi2 openbox|| kdialog --error "Install Aborted! The Default KDE4 Desktop Will Be Used"')
        sys.exit()

    def slotSelectOther(self):
        os.popen('gurpmi2 WindowMaker|| kdialog --error "Install Aborted! The Default KDE4 Desktop Will Be Used"')
        sys.exit()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DS = QtGui.QDialog()
    ui = MainWindow()
    DS.show()
    sys.exit(app.exec_())

