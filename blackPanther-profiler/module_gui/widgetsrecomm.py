#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
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

from ui_widgetsrecomm import Ui_ServiceItemWidget
class RecommendItemWidget(QtGui.QWidget):

    def __init__(self, title, desc, size, tooltip, pic, parent):
        QtGui.QWidget.__init__(self, parent)

        self.ui = Ui_ServiceItemWidget()
        self.ui.setupUi(self)

        self.ui.labelName.setText(title)
        self.ui.labelDesc.setText(desc)
        self.ui.labelSize.setText(size)
	self.ui.labelStatus.setToolTip(tooltip)
	self.ui.installButton.setVisible(False)

        try:
            self.ui.labelStatus.setPixmap(QtGui.QPixmap(pic))
        except:
            pass
    
    def set_status(self, message, button_visible):
	self.ui.message.setText(message)
	self.ui.installButton.setVisible(button_visible)
