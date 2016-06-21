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
import os
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyKDE4.kdecore import ki18n, KGlobal, KConfig
#from PyKDE4.kutils import KCModuleInfo, KCModuleProxy
import subprocess, sys
from module_gui.ScreenWidget import ScreenWidget
from module_gui.goodbyeWidget import Ui_goodbyeWidget
#import module_gui.ScrSmolt as smoltWidget

currentDir = os.path.dirname(os.path.realpath(__file__))
moduleDir = currentDir+'/../module_migration/'
sys.path.append(moduleDir)
#sys.path.append('/tmp/module_migration/')

from migration.utils import partition

class Widget(QtGui.QWidget, ScreenWidget):
    title = ki18n("Apply Settings")
    desc = ki18n("Congratulations!")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_goodbyeWidget()
        self.ui.setupUi(self)

        lang = KGlobal.locale().language()

        if lang == "hu":
            self.helpPageUrl = "http://www.facebook.com/blackpantheros"
        else:
            self.helpPageUrl = "http://www.blackpantheros.eu"

        self.smoltUrl = "http://backend.blackpanther.hu"

        users = partition.allUsers()
        
        # ittkapcsoldki
        if not users:
            self.ui.migrationGroupBox.hide()
        #idaig

        self.ui.buttonSystemSettings_2.connect(self.ui.buttonSystemSettings_2, SIGNAL("clicked()"), self.startSmolt)
        self.ui.buttonMigration.connect(self.ui.buttonMigration, SIGNAL("clicked()"), self.startMigration)
        self.ui.buttonSystemSettings.connect(self.ui.buttonSystemSettings, SIGNAL("clicked()"), self.startSystemSettings)
        self.ui.buttonHelpPages.connect(self.ui.buttonHelpPages, SIGNAL("clicked()"), self.startHelpPages)

    def startSystemSettings(self):
	print "System Settings"
        self.procSettings = QProcess()
        self.procSettings.start("systemsettings")

    def startMigration(self):
	print "Migration tool"
        self.procSettings = QProcess()
        self.procSettings.start("migration")

    def startHelpPages(self):
	print "Start Help Pages"
        self.procSettings = QProcess()
        command = "default-browser " + self.helpPageUrl
        self.procSettings.start(command)

    def startSmolt(self):
	print "Start HW Details Sending"
        self.procSettings = QProcess()
        command = "default-browser " + self.smoltUrl
        self.procSettings.start(command)

    #def setSmolt(self):
    #    if self.smoltSettings["profileSend"] == False:
     #       self.ui.smoltGroupBox.setVisible(False)

    #def shown(self):
       #self.smoltSettings = smoltWidget.Widget.screenSettings
       #self.setSmolt()

    def execute(self):
       return True


