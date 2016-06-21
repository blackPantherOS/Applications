# -*- coding: utf-8 -*-
#


from PyQt4 import QtGui
from PyQt4.QtGui import QFileDialog

from PyQt4.QtCore import *
from PyKDE4.kdecore import ki18n, KStandardDirs, KGlobal, KConfig
import os, sys, subprocess

from module_gui.ScreenWidget import ScreenWidget
from module_gui.recommendWidget import Ui_recommendWidget
from widgetsrecomm import RecommendItemWidget
from ui_widgetsrecomm import Ui_ServiceItemWidget
from desktopparser import DesktopParser
from ConfigParser import ConfigParser

import time
import threading

currentDir = os.path.dirname(os.path.realpath(__file__))
moduleDir = os.path.dirname(os.getcwd()) + '/blackPanther-profiler/'
sys.path.append(moduleDir)

class InstallTimeThread(QThread):
  def __init__(self, parent, applist):
    QThread.__init__(self)
    self.parent = parent
    self.applist = applist
  def run(self):
    for app in self.applist:
      if os.popen("rpm -q "+app).read().find("is not installed") != -1:
        self.parent.emit(SIGNAL("disable"), app, False)
      else:
        self.parent.emit(SIGNAL("disable"), app, True)

class Widget(QtGui.QWidget, ScreenWidget):
    title = ki18n("Insert some catchy title about apps..")
    desc = ki18n("Wonderful more apps! \m/")
    #tooltip = ki18n("Wonderful more apps! \m/")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_recommendWidget()
        self.ui.setupUi(self)
        self.check_update = checkUpdateThread(self)
        self.check_update.start()

        self.catLang = KGlobal.locale().language()

#        self.ui.listRecommendApp.connect(self.ui.listRecommendApp, SIGNAL("itemSelectionChanged()"), self.setInstall)
        self.connect(self, SIGNAL("disable"), self.disableInstallButton)
#        it = threading.Thread(target=self.init, args=(self))
#        it.start()
        
#    def init(self):
        plugnum = "0"
	config = ConfigParser()

	userConf = os.path.expanduser("~/.config/profiler/recommend.cfg")
	if not os.path.exists(userConf):
	    print "System list found.."
	    config.read('recommend.cfg')
	else:
	    config.read(userConf)
	    print "User list found.."

	applist = config.sections()

	grouplist = []

	for app in applist:
	    try:
		group = config.get(app, "group")
		if group not in grouplist:
		    grouplist.append(group)
	    except:
		print "Not found for", app
        print "Csoport lista kész:",
        applist.sort()
        grouplist.sort()
        print grouplist

        self.install_time_thread = InstallTimeThread(self, applist)

        for group in grouplist:
          self.new_tab(group, group)

	for app in applist:
            group = config.get(app, "group")
	    try:
		Title = app
		Desc = config.get(app, "desc")
		Summary = config.get(app, "summary")
#		Thumb = app+".jpg"
		Size = config.get(app, "size")
		InstallTime = 1
		#config.get(app, "installtime")
		favor = eval(config.get(app, "favorite"))
	    except:
		print "Not found for", app
		continue

            thumbFolder = os.listdir(os.path.join("./module_gui/pics", "screenshots"))
            Thumb = os.path.join("./module_gui/pics/screenshots/" + app + ".png")
            
	    if group == "Plugins":
		Thumb = "./module_gui/pics/plugins.png"
		print "Plugins detected..."


	    if not os.path.exists(Thumb):
		print "Empty App Thumbnail detected..."
		Thumb = "./module_gui/pics/blackPanther_shield200.png"

            Tooltip = "<img src="+Thumb+"/><br /><br /><b>\nName:</b> "+app+"<br /><br /><b>\nDescription:</b> "+Desc+"<br />"

            item = QtGui.QListWidgetItem(self.ui.__dict__[group+"_listRecommendApp"])
            self.__dict__["RIW_"+group+"_"+app] = RecommendItemWidget(unicode(Title, "utf8", "replace"), unicode(Summary, "utf8", "replace"), Size, unicode(Tooltip, "utf8", "replace"), Thumb, self.ui.__dict__[group+"_listRecommendApp"])
            item.setSizeHint(QSize(38,110))
            self.ui.__dict__[group+"_listRecommendApp"].setItemWidget(item, self.__dict__["RIW_"+group+"_"+app])
            self.connect(self.__dict__["RIW_"+group+"_"+app].ui.installButton, SIGNAL("clicked()"), lambda x=app: self.setInstall(x))

            if favor:
              item = QtGui.QListWidgetItem(self.ui.listRecommendApp)
              self.__dict__["RIW_default_"+app] = RecommendItemWidget(unicode(Title, "utf8", "replace"), unicode(Summary, "utf8", "replace"), Size, unicode(Tooltip, "utf8", "replace"), Thumb, self.ui.listRecommendApp)
              item.setSizeHint(QSize(38,110))
              self.ui.listRecommendApp.setItemWidget(item, self.__dict__["RIW_default_"+app])
              self.connect(self.__dict__["RIW_default_"+app].ui.installButton, SIGNAL("clicked()"), lambda x=app: self.setInstall(x))

    	    self.ui.checkBox.connect(self.ui.checkBox, SIGNAL("stateChanged(int)"), self.disableWidgets)

        #self.ui.pushInstallButton.connect(self.ui.pushInstallButton, SIGNAL("clicked()"), self.goInstall)
        self.ui.pushUpdateButton.connect(self.ui.pushUpdateButton, SIGNAL("clicked()"), self.goUpdate)
        
        self.install_time_thread.start()
        
    def disableInstallButton(self, appname, status):
      keys = []
      for key in self.__dict__.keys():
        if key.find("RIW_") != -1:
          pos = key.find("_",4)+1
          if key[pos:] == appname:
            if status:
              self.__dict__[key].set_status("Installed", False)
              self.__dict__[key].setDisabled(True)
            else:
              self.__dict__[key].set_status("Not Installed", True)
              self.__dict__[key].setDisabled(False)

    def installState(self, pstate):
	print "Install state of ", app

    def new_listRecommendApp(self, section_name):
        name = section_name + "_listRecommendApp"
        self.ui.__dict__[name] = QtGui.QListWidget(self.ui.__dict__["tab_"+section_name])
        self.ui.__dict__[name].setGeometry(QRect(0, 0, 511, 411))
        self.ui.__dict__[name].setMinimumSize(QSize(0, 300))
        self.ui.__dict__[name].setStyleSheet("#"+name+"""{background-color: 
          qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 81),   
          stop:0.00537634 rgba(0, 0, 0, 80), stop:1 rgba(250, 250, 230, 80));\n\n
          border: 1px solid rgb(236, 236, 236, 80);}""")                            
        self.ui.__dict__[name].setFrameShape(QtGui.QFrame.NoFrame)
        self.ui.__dict__[name].setFrameShadow(QtGui.QFrame.Sunken)
        self.ui.__dict__[name].setAlternatingRowColors(False)
        self.ui.__dict__[name].setTextElideMode(Qt.ElideRight)
        self.ui.__dict__[name].setProperty("isWrapping", False)
        self.ui.__dict__[name].setResizeMode(QtGui.QListView.Fixed)
        self.ui.__dict__[name].setLayoutMode(QtGui.QListView.SinglePass)
        self.ui.__dict__[name].setSpacing(0)
        self.ui.__dict__[name].setGridSize(QSize(0, 110))
        self.ui.__dict__[name].setViewMode(QtGui.QListView.ListMode)
        self.ui.__dict__[name].setModelColumn(0)
        self.ui.__dict__[name].setUniformItemSizes(False)
        self.ui.__dict__[name].setBatchSize(100)
        self.ui.__dict__[name].setObjectName(name)
#        self.ui.__dict__[name].connect(self.ui.__dict__[name], SIGNAL("itemSelectionChanged()"), self.setInstall)
                                                                                                   
    def new_tab(self, section_name, tab_label):
      self.ui.__dict__["tab_"+section_name] = QtGui.QWidget()

      icon = QtGui.QIcon()
      icon.addPixmap(QtGui.QPixmap("/usr/share/icons/"+section_name+"_section.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
      self.ui.tabWidget.addTab(self.ui.__dict__["tab_"+section_name], icon, tab_label)
      self.new_listRecommendApp(section_name)

    def disableWidgets(self, state):
        keys = []
        for key in self.ui.__dict__.keys():
          if key.find("listRecommendApp") != -1:
            keys.append(key)
        if state:
	    #print "CHECKBOX ON"
            #self.ui.pushInstallButton.setDisabled(True)
            for key in keys:
              self.ui.__dict__[key].setDisabled(True)
        else:
    	    #print "CHECKBOX OFF"
            #self.__class__.screenSettings["hasChanged"] = True
            #self.ui.pushInstallButton.setDisabled(False)
            for key in keys:
              self.ui.__dict__[key].setDisabled(False)


    def setInstall(self, app):
	print "Select install to System", app
    	p = subprocess.Popen(['gurpmi2', '-p', app], stdout=subprocess.PIPE)
    	#p = subprocess.Popen(['apper', '--install-package-name', app], stdout=subprocess.PIPE)

    def goUpdate(self):
	print "GO UPDATE CFG from Internet"
    	#p = subprocess.Popen(['programtelepito', 'update.rpm'], stdout=subprocess.PIPE)
    	print moduleDir
    	#p = subprocess.Popen(['python '+moduleDir+'module_update/downloader.py'], stdout=subprocess.PIPE)
    	self.ui.pushUpdateButton.setDisabled(True)

    def shown(self):
        self.check_update.get_status()

    def execute(self):
        return True

class checkUpdateThread(QThread):
  def __init__(self, parent): 
    QThread.__init__(self)
    self.parent = parent
  def run(self):
    try:
    	self.updateStat = False
    	#self.updateStat = os.popen('python ' +moduleDir+'module_update/update.py').read().find("Failed")
    except:
	print "Skipped: Update module not available"
	self.updateStat = False
	#self.parent.ui.pushUpdateButton.setDisabled(True)

  def get_status(self):
	print self.updateStat
    	if self.updateStat:
	    print "Update is fine"
	    self.parent.ui.pushUpdateButton.setDisabled(False)    
	    self.parent.ui.labelUpdate.setText("(Updates available)")    
	else:
	#import update
	    print "Update is fail"
	    self.parent.ui.pushUpdateButton.setDisabled(True)
	    self.parent.ui.labelUpdate.setText("(Updates not found)")    

def encode(text):
    return text.encode('utf-8')
