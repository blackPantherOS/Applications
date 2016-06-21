# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#


from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyKDE4.kdecore import ki18n

from module_gui.ScreenWidget import ScreenWidget
from module_gui.welcomeWidget import Ui_welcomeWidget

import os, shutil, subprocess

class Widget(QtGui.QWidget, ScreenWidget):
    title = ki18n("Welcome")
    desc = ki18n("Welcome to Profiler")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_welcomeWidget()
        self.ui.setupUi(self)

        self.release = self.getRelease().split()[0] + " " + self.getRelease().split()[1]
        self.ext = ""

        if self.release.__len__() > 2:
            self.ext = self.getRelease().split()[3]

        #welcomeStr = "Welcome to " + self.release + " " + self.ext
        relStr = "v" + self.ext
        self.ui.label_2.setText(relStr)

    def getRelease(self):
    	try:
            p = subprocess.Popen(["cat","/etc/blackPanther-release"], stdout=subprocess.PIPE)
            release, err = p.communicate()
            return str(release)

        except:
            return "blackPanther OS"

        self.autofile = os.path.expanduser("~/.config/autostart/blackPanther-profiler.desktop")
        self.gautofile = "/usr/share/applications/blackPanther-profiler.desktop"

        self.ui.checkAutostart.setChecked(True)

    def shown(self):
        pass

    def execute(self):
        if not self.ui.checkAutostart.isChecked():
            try:
        	os.system("rm -f ~/.config/autostart/blackPanther-profiler.desktop")
                #os.remove(self.autofile)
            except OSError:
                pass
        else:
            if not os.path.isfile(self.autofile):
        	os.system("mkdir -p ~/.config/autostart")
                shutil.copyfile(self.gautofile, self.autofile)
        return True

