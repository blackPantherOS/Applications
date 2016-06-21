#!/usr/bin/python
# -*- coding: utf-8 -*-

# PyKDE
from PyKDE4.kdecore import KAboutData, ki18n

# Application Data
appName     = "profiler"
programName = ki18n("Profiler Desktop")
modName     = "profiler"
version     = "1.0"
description = ki18n("Profiler Desktop")
license     = KAboutData.License_GPL
copyright   = ki18n("(c) 2010-2015 blackPanther OS (froked Kaptan)")
text        = ki18n("blackPanther OS Profiler Wizard")
homePage    = "http://www.blackpantheros.eu"
bugEmail    = "bugs@blackpanther.hu"
catalog     = appName
aboutData   = KAboutData(appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)

# Author(s)
aboutData.addAuthor(ki18n("Charles Barcza, Miklos Horvath"), ki18n("Current Maintainer"))
