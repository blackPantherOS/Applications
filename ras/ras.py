#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created: Tue Jul  1 16:41:11 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore,QtGui, uic
import rasrc

class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('ras.ui', self)
#        print dir(self)
#        help(self.tabWidget)
        self.ras_new_tab("internet", "Internet", 0)
        self.show()

    def ras_new_tab(self, section_name, tab_label, counter):
      self.ras_tab = QtGui.QWidget()

      # IDE KELL MAJD A TARTALOM GENERÁLÁSA
      
      icon = QtGui.QIcon()
      icon.addPixmap(QtGui.QPixmap("/usr/share/icons/"+section_name+"_section.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
      self.tabWidget.addTab(self.ras_tab, icon, tab_label)

    @QtCore.pyqtSlot()
    def on_pushButton_2_clicked(self):
	print "install button"


    @QtCore.pyqtSlot()
    def on_pushButton_clicked(self):
	print "Uninstall button"

    @QtCore.pyqtSlot()
    def on_checkBox_10_clicked(self):
	print "Check box 10"

    @QtCore.pyqtSlot()
    def on_checkBox_12_clicked(self):
	print "Check box 12"

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
