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
from PyQt4.QtGui import QFileDialog

from PyQt4.QtCore import *
from PyKDE4.kdecore import ki18n, KStandardDirs, KGlobal, KConfig
import os, sys, subprocess

from module_gui.ScreenWidget import ScreenWidget
from module_gui.wallpaperWidget import Ui_wallpaperWidget
from wallpaperWidgetList import WallpaperItemWidget

from desktopparser import DesktopParser
from ConfigParser import ConfigParser


class Widget(QtGui.QWidget, ScreenWidget):
    screenSettings = {}
    screenSettings["hasChanged"] = False

    # title and description at the top of the dialog window
    title = ki18n("Insert some catchy title about wallpapers..")
    desc = ki18n("Wonderful, awesome, superb wallpapers! \m/")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self, None)
        self.ui = Ui_wallpaperWidget()
        self.ui.setupUi(self)
        # Get system locale
        self.catLang = KGlobal.locale().language()

        # Get screen resolution
        # rect = QtGui.QDesktopWidget().screenGeometry() FIXME: where could
        # this be needed?

        # Get metadata.desktop files from shared wallpaper directory
        lst = KStandardDirs().findAllResources("wallpaper", "*metadata.desktop", KStandardDirs.Recursive)

        for desktopFiles in lst:
            parser = DesktopParser()
            parser.read(str(desktopFiles))

            try:
                wallpaperTitle = parser.get_locale('Desktop Entry', 'Name[%s]' % self.catLang, '')
            except:
                wallpaperTitle = parser.get_locale('Desktop Entry', 'Name', '')

            try:
                wallpaperDesc = parser.get_locale('Desktop Entry', 'X-KDE-PluginInfo-Author', '')
            except:
                wallpaperDesc = "Unknown"

            # Get all files in the wallpaper's directory
            try:
                thumbFolder = os.listdir(os.path.join(os.path.split(str(desktopFiles))[0], "contents"))
            except OSError:
                thumbFolder = os.listdir(os.path.join(os.path.split(str(desktopFiles))[0], "content"))

            """
            Appearantly the thumbnail names doesn't have a standard.
            So we get the file list from the contents folder and
            choose the file which has a name that starts with "scre".

            File names I've seen so far;
            screenshot.jpg, screnshot.jpg, screenshot.png, screnshot.png
            """

            wallpaperThumb = ""

            for thumb in thumbFolder:
                if thumb.startswith('scre'):
                    wallpaperThumb = os.path.join(os.path.split(str(desktopFiles))[0], "contents/" + thumb)

            if not wallpaperThumb:
            	    wallpaperThumb = os.path.join(os.path.split(str(desktopFiles))[0], "contents/images/1024x768.png")
            	    if not os.path.exists(wallpaperThumb):
            		wallpaperThumb = os.path.join("./module_gui/pics/logo2010.png")
            		print "Thumbnail missed swtitch to default:",wallpaperThumb

            wallpaperFile = os.path.split(str(desktopFiles))[0]

            # Insert wallpapers to listWidget.
            item = QtGui.QListWidgetItem(self.ui.listWallpaper)
            # Each wallpaper item is a widget. Look at widgets.py for more information.
            widget = WallpaperItemWidget(unicode(wallpaperTitle, "utf8", "replace"), unicode(wallpaperDesc, "utf8", "replace"), wallpaperThumb, self.ui.listWallpaper)
            item.setSizeHint(QSize(150, 180))
            self.ui.listWallpaper.setItemWidget(item, widget)
            # Add a hidden value to each item for detecting selected wallpaper's path.
            item.setStatusTip(wallpaperFile)

        self.ui.listWallpaper.itemSelectionChanged.connect(self.setWallpaper)
        self.ui.checkBox.stateChanged.connect(self.disableWidgets)
        self.ui.buttonChooseWp.clicked.connect(self.selectWallpaper)

    def disableWidgets(self, state):
        if state:
            self.__class__.screenSettings["hasChanged"] = False
            self.ui.buttonChooseWp.setDisabled(True)
            self.ui.listWallpaper.setDisabled(True)
        else:
            self.__class__.screenSettings["hasChanged"] = True
            self.ui.buttonChooseWp.setDisabled(False)
            self.ui.listWallpaper.setDisabled(False)

    def setWallpaper(self):
        self.__class__.screenSettings["selectedWallpaper"] = self.ui.listWallpaper.currentItem().statusTip()
        self.__class__.screenSettings["hasChanged"] = True

    def selectWallpaper(self):
        selectedFile = QFileDialog.getOpenFileName(None, "Open Image", os.environ["HOME"], 'Image Files (*.png *.jpg *.bmp)')

        if selectedFile.isNull():
            return
        else:
            item = QtGui.QListWidgetItem(self.ui.listWallpaper)
            wallpaperName = os.path.splitext(os.path.split(str(selectedFile))[1])[0]
            widget = WallpaperItemWidget(unicode(wallpaperName, "utf8", "replace"), unicode("Unknown"), selectedFile, self.ui.listWallpaper)
            item.setSizeHint(QSize(150, 180))
            self.ui.listWallpaper.setItemWidget(item, widget)
            item.setStatusTip(selectedFile)
            self.ui.listWallpaper.setCurrentItem(item)
            self.resize(150, 180)

    def shown(self):
        pass

    def execute(self):
        return True
