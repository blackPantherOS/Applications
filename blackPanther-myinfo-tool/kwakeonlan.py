#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2009 David Edmundson                                          
# This code is free software under the GPL    

from PyQt4 import QtCore, QtGui, uic 
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *
from PyKDE4.kio import *
import re,sys,struct,socket

class MacPushButton(QtGui.QPushButton):
  def __init__(self,parent=None):
    QtGui.QPushButton.__init__(self,parent)
    self.mac_addr = ""
    self.setText("Wake")
    self.setIcon(KIcon("computer"))

  def setMacAddr(self,addr):
    self.mac_addr = addr

  def mouseReleaseEvent(self,mouse):
    self.emit(QtCore.SIGNAL("released(QString)"),self.mac_addr)
    QtGui.QPushButton.mouseReleaseEvent(self,mouse)

(ui,base_class) = uic.loadUiType("kwakeonlan.ui")
class KWakeOnLan(ui,base_class):
  def __init__(self, parent=None):
    ui.__init__(self,parent) 
    base_class.__init__(self,parent)

    #setup stuff
    self.setupUi(self)
    self.ui_wakeButton.setEnabled(False)
    self.ui_wakeButton.setIcon(KIcon("computer"))
    self.ui_saveButton.setEnabled(False)
    self.ui_saveButton.setIcon(KIcon("document-save"))
    self.ui_statusText.setText("")

    config = KConfig("kwakeonlan")
    group = config.group("computers")

    for name,mac in group.entryMap().iteritems():
      self.addEntry(name,mac)

    self.ui_macAddr.setInputMask("HH:HH:HH:HH:HH:HH;_")
  
    #connections
    self.connect(self.ui_macAddr,QtCore.SIGNAL("textChanged(QString)"),self.textChanged)
    self.connect(self.ui_wakeButton,QtCore.SIGNAL("released()"),self.wakePressed)
    self.connect(self.ui_saveButton,QtCore.SIGNAL("released()"),self.savePressed)

  def addEntry(self,name,addr):
    #populate saved entries
    box = QtGui.QHBoxLayout()
    label = QtGui.QLabel(name)
    button = MacPushButton()
    button.setMacAddr(addr)
    box.addWidget(label)
    box.addStretch()
    box.addWidget(button)
    self.connect(button,QtCore.SIGNAL("released(QString)"),self.wake)
    self.layout().insertLayout(0,box)


  def textChanged(self):
    mac_addr = str(self.ui_macAddr.text())
    enable = False
    if(self.validMac(mac_addr)):
      enable = True
    self.ui_wakeButton.setEnabled(enable)
    self.ui_saveButton.setEnabled(enable)
    
  def savePressed(self):
    config = KConfig("kwakeonlan")
    group = config.group("computers")
    name =''
    while not name:
      (name,reponse) = QtGui.QInputDialog.getText(self,"Save Wake On Lan Entry","Please give a name for this computer")
      if not reponse:
        sys.exit(0)
    group.writeEntry(name,self.ui_macAddr.text())
    self.addEntry(name,str(self.ui_macAddr.text()))
    pass

  def wakePressed(self):
    self.wake(self.ui_macAddr.text())

  def wake(self,mac):
    mac_addr = str(mac)
    self.ui_statusText.setText("Wake sent to "+mac)

    #if it looks like a valid mac addr
    if(self.validMac(mac_addr)):
      print "Waking " +  mac_addr
      wakeOnLan(str(mac_addr))
    else:
      print "Invalid Mac Addr"

  def validMac(self,addr):
    #this is kind of useless since I put on the input mask
    #checks mac is valid, adds a colon on end of string to make the regex simpler :-)
    return re.match("([0-9A-Fa-f]{1,2}:){6}",addr+":") != None

#The processing code: 
# Copyright (C) 2002 by Micro Systems Marc Balmer                                                      
# Written by Marc Balmer, marc@msys.ch, http://www.msys.ch/                                            
# This code is free software under the GPL    

def wakeOnLan(ethernet_address):

  # Construct a six-byte hardware address

  addr_byte = ethernet_address.split(':')
  hw_addr = struct.pack('BBBBBB', int(addr_byte[0], 16),
    int(addr_byte[1], 16),
    int(addr_byte[2], 16),
    int(addr_byte[3], 16),
    int(addr_byte[4], 16),
    int(addr_byte[5], 16))

  # Build the Wake-On-LAN "Magic Packet"...

  msg = '\xff' * 6 + hw_addr * 16

  # ...and send it to the broadcast address using UDP

  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  s.sendto(msg, ('<broadcast>', 9))
  s.close()

#back to my code

if __name__ == '__main__':
  appName     = "KWakeOnLan"
  catalog     = ""
  programName = ki18n ("")
  version     = "0.1"
  description = ki18n ("")
  license     = KAboutData.License_GPL
  copyright   = ki18n ("(c) 2008 David Edmundson")
  text        = ki18n ("none")
  homePage    = "http://kde.org"
  bugEmail    = "kde@davidedmundson.co.uk"

  aboutData   = KAboutData (appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)

  KCmdLineArgs.init (sys.argv, aboutData)
  app = KApplication()
  widget=KWakeOnLan()
  #widget.setWindowModality(QtCore.Qt.WindowModal)ad
  widget.show()
  sys.exit(app.exec_())
