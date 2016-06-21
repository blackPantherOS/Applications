#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, getopt
from PyQt4 import QtCore, QtGui
from PyKDE4 import kdeui
from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs, KConfig

import module_gui, subprocess, os, dbus

from module_gui.profilerMain import Ui_profilerUI
import module_gui.ScrWelcome as welcomeWidget
import module_gui.ScrRecommend  as recommendWidget
import module_gui.ScrMouse as mouseWidget
import module_gui.ScrNetwork as networkWidget
import module_gui.ScrWallpaper  as wallpaperWidget
import module_gui.ScrGoodbye  as goodbyeWidget
import module_gui.ScrStyle  as styleWidget
import module_gui.ScrMenu  as menuWidget
import module_gui.ScrSearch  as searchWidget
import module_gui.ScrSummary  as summaryWidget
import module_gui.ScrKeyboard  as keyboardWidget
#import module_gui.ScrPackage as packageWidget
#import module_gui.ScrSmolt as smoltWidget

def usage() :
      print """
       -m <module1> <module2> <module3> <module4> <module5> """ % (sys.argv[0],sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])

def loadFile(_file):
    try:
        f = file(_file)
        d = [a.strip() for a in f]
        d = (x for x in d if x and x[0] != "#")
        f.close()
        return d
    except:
        return []

def isLiveCD():
    try:
        liveCDcheck = open('/var/run/livemedia')
    except IOError:
        return False

    return True

def profileSended():
    ''' Do not show screen if profile was already sended.'''
    #file = open("/etc/hardwarebm/blackPanther-hw", 'r')

    #if file.read() != '':
    #    return True

    #return False
def paramGet():
    dialogID = sys.argv[2:]

    if not sys.argv[1:]:
	return False
    else:
	print "Switch to recommend apps dialog"
	return True

if isLiveCD():
    availableScreens = [welcomeWidget, keyboardWidget, mouseWidget, styleWidget, menuWidget, wallpaperWidget, networkWidget, summaryWidget, goodbyeWidget]
#elif profileSended():
#    availableScreens = [welcomeWidget, mouseWidget, styleWidget, menuWidget, wallpaperWidget, searchWidget, networkWidget, packageWidget, summaryWidget, goodbyeWidget]
elif paramGet():
    # ide be lehet allitani majd, hogy csak a választott dialogok jelenjenek meg
    availableScreens = [recommendWidget, goodbyeWidget]
else:
    availableScreens = [welcomeWidget,  recommendWidget, keyboardWidget, mouseWidget, wallpaperWidget, styleWidget, menuWidget, networkWidget, searchWidget, summaryWidget, goodbyeWidget]

class Profiler(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_profilerUI()

        self.ui.setupUi(self)
        self.screens = availableScreens
        self.screenData = None
        self.moveInc = 1
        self.menuText = ""
        self.config = KConfig("profilerrc")
        self.createWidgets(self.screens)


        self.ui.labelMenu.setText(self.menuText)

        QtCore.QObject.connect(self.ui.buttonNext, QtCore.SIGNAL("clicked()"), self.slotNext)
        QtCore.QObject.connect(self.ui.buttonBack, QtCore.SIGNAL("clicked()"), self.slotBack)
        QtCore.QObject.connect(self.ui.buttonFinish, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT("quit()"))
        QtCore.QObject.connect(self.ui.buttonCancel, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT("quit()"))

    def slotFinished(self):
        if wallpaperWidget.Widget.selectedWallpaper:
            config =  KConfig("plasma-desktop-appletsrc")
            group = config.group("Containments")
            for each in list(group.groupList()):
                subgroup = group.group(each)
                subcomponent = subgroup.readEntry('plugin')
                if subcomponent == 'desktop' or subcomponent == 'folderview':
                    subg = subgroup.group('Wallpaper')
                    subg_2 = subg.group('image')
                    subg_2.writeEntry("wallpaper", wallpaperWidget.Widget.selectedWallpaper)
            self.killPlasma()
            QtGui.qApp.quit()
        else:
            QtGui.qApp.quit()

    def killPlasma(self):
        p = subprocess.Popen(["pidof", "-s", "plasma-desktop"], stdout=subprocess.PIPE)
        out, err = p.communicate()
        pidOfPlasma = int(out)

        try:
            os.kill(pidOfPlasma, 15)
            self.startPlasma()
        except OSError, e:
            print 'WARNING: failed os.kill: %s' % e
            print "Trying SIGKILL"
            os.kill(pidOfPlasma, 9)
            self.startPlasma()

    def startPlasma(self):
        p = subprocess.Popen(["plasma-desktop"], stdout=subprocess.PIPE)

    # returns the id of current stack
    def getCur(self, d):
        new   = self.ui.mainStack.currentIndex() + d
        total = self.ui.mainStack.count()
        if new < 0: new = 0
        if new > total: new = total
        return new

    # move to id numbered step
    def setCurrent(self, id=None):
        if id:
            self.stackMove(id)

    # execute next step
    def slotNext(self,dryRun=False):
        self.menuText = ""
        curIndex = self.ui.mainStack.currentIndex() +1

        for each in self.screenId:
            i = self.screenId.index(each)
            if  curIndex < len(self.screenId):
                if i == curIndex:
                    self.menuText += self.putBold(self.screenId[i])
                else:
                    self.menuText += self.putBr(self.screenId[i])

        self.ui.labelMenu.setText(self.menuText)

        _w = self.ui.mainStack.currentWidget()
        ret = _w.execute()
        if ret:
            self.stackMove(self.getCur(self.moveInc))
            self.moveInc = 1

    # execute previous step
    def slotBack(self):
        self.menuText = ""
        curIndex = self.ui.mainStack.currentIndex()
        for each in self.screenId:
            i = self.screenId.index(each)
            if i <= len(self.screenId) and not i == 0:
                if i == curIndex:
                    self.menuText += self.putBold(self.screenId[i -1])
                else:
                    self.menuText += self.putBr(self.screenId[i -1])

        self.menuText += self.putBr(self.screenId[-1])
        self.ui.labelMenu.setText(self.menuText)

        _w = self.ui.mainStack.currentWidget()
        _w.backCheck()
        self.stackMove(self.getCur(self.moveInc * -1))
        self.moveInc = 1

    #def putBr(self, item):
    #    return unicode("  ") + item + "<br>"
    #
    #def putBold(self, item):
    #    return "<b>" + unicode("  ") + item + "</b><br>"

    def putBr(self, item):
        #return "» " + item + "<br>"
        return unicode("» ", encoding='utf-8') + item + "<br>"

    def putBold(self, item):
        #return "<b>  " + item + "</b><br>"
        return "<b><u>" +  item + unicode(" »", encoding='utf-8') +"</u></b><br>"

    # move to id numbered stack
    def stackMove(self, id):
        if not id == self.ui.mainStack.currentIndex() or id==0:
            self.ui.mainStack.setCurrentIndex(id)
            _w = self.ui.mainStack.currentWidget()
            _w.update()
            _w.shown()

        if self.ui.mainStack.currentIndex() == len(self.screens)-1:
            self.ui.buttonNext.hide()
            self.ui.buttonFinish.show()
        else:
            self.ui.buttonNext.show()
            self.ui.buttonFinish.hide()

        if self.ui.mainStack.currentIndex() == 0:
            self.ui.buttonBack.hide()
        else:
            self.ui.buttonBack.show()

    # create all widgets and add inside stack
    def createWidgets(self, screens=[]):

        self.screenId = []

        self.ui.mainStack.removeWidget(self.ui.page)
        for screen in screens:
            _scr = screen.Widget()
            title = _scr.windowTitle()
            self.screenId.append(title)

            if self.screens.index(screen) == 0:
                self.menuText += self.putBold(title)
            else:
                self.menuText += self.putBr(title)
            self.ui.mainStack.addWidget(_scr)

        self.stackMove(0)

    def disableNext(self):
        self.buttonNext.setEnabled(False)

    def disableBack(self):
        self.buttonBack.setEnabled(False)

    def enableNext(self):
        self.buttonNext.setEnabled(True)

    def enableBack(self):
        self.buttonBack.setEnabled(True)

    def isNextEnabled(self):
        return self.buttonNext.isEnabled()

    def isBackEnabled(self):
        return self.buttonBack.isEnabled()

    def __del__(self):
        group = self.config.group("General")
        group.writeEntry("RunOnStart", "False")


if __name__ == "__main__":

    # About data
    appName     = "profiler"
    catalog     = ""
    programName = ki18n("profiler")
    version     = "4.0"
    description = ki18n("Profiler is a welcome wizard for blackPanther OS")
    license     = KAboutData.License_GPL
    copyright   = ki18n("(c) 2014")
    text        = ki18n("none")
    homePage    = ""
    bugEmail    = ""

    aboutData   = KAboutData(appName,catalog, programName, version, description,
                                license, copyright,text, homePage, bugEmail)
    try:
	optlist = getopt.getopt(sys.argv[0:], 'h', ['help','help-all', 'm','appname'])
    except getopt.GetoptError, err:
        print "ERROR:", str(err)
        usage()
        sys.exit(2)

    if not sys.argv[1:]:
    	sysarg = sys.argv
    else:
    	sysarg = sys.argv[1:]
    	for opt in optlist[1:]:
    	    if "-m" in opt:
    		sysarg = sys.argv[1:]
    	    else:
    		sysarg = sys.argv


    KCmdLineArgs.init(sysarg, aboutData)
    app =  kdeui.KApplication()

    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    profiler = Profiler()
    profiler.show()
    rect  = QtGui.QDesktopWidget().screenGeometry()
    profiler.move(rect.width()/2 - profiler.width()/2, rect.height()/2 - profiler.height()/2)
    app.exec_()

