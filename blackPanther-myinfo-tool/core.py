#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
## Feature and Written by Charles Barcza kbarcza@blackpanther.hu
##    blackPanther OS - www.blackpanther.hu
##


import sys, re, os, string, signal, socket, array, struct, fcntl, locale
import commands
from pycpu import deltaTime
from threading import Thread
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *

#from kuick_ui import Kuick_UI

class Cpu(Thread):  # Ez az uj szal kellett ahhoz, hogy a hibat kijavitsam.
  def __init__(self):
    Thread.__init__(self)
    self.get_cpu_usage = 0
  def run(self):
    while True:
      dt = deltaTime(2)
      self.get_cpu_usage = 100 - (dt[len(dt) - 1] * 100.0 / sum(dt))

def lspcian(inp):
  net = ''
  for line in inp:
    if 'DISPLAY_VGA' in line:
      vga = line[line.find('|')+1:line.find('[')]
    elif 'NETWORK' in line:
      net += line[line.find('|')+1:line.rfind('[')]
  return [vga, net]

def ds(inp):
  n = int(inp)
  if n < 1000:
    return str(n)+' KB'
  elif n < 1000000:
    return str((n/1000))+' MB'
  else:
    return str((n/1000000))+' GB'

def dl(inp):
  sl = inp.split()
  disks_n = 0
  partitions_n = 0
  disks = []
  partitions = []
  l = len(sl)
  i = 0
  while i < l:
    p = len(sl[i])-1
    if sl[i][p] in '0123456789':
      if sl[i+1] != '1':
        partitions_n += 1
        partitions.append([sl[i], sl[i+1]])
    else:
      disks_n += 1
      disks.append([sl[i], sl[i+1]])
    i += 2
  i = 0
  out = ''
  if disks_n == 1:
    vp = partitions_n
  elif partitions_n < 10:
    vp = partitions_n
  else:
    vp = disks_n
  x = 0
  while True:
    if disks_n == 1:
      out += '<b>' + partitions[i][0] + ':</b> ' + ds(partitions[i][1])
    elif partitions_n < 10:
      out += '<b>' + partitions[i][0] + ':</b> ' + ds(partitions[i][1])
    else:
      out += '<b>' + disks[i][0] + ':</b> ' + ds(disks[i][1])
    x += 1
    if x == 3:
      x = 0
      out += '<br>'
    else:
      out += '\t' 
    i += 1
    if i == vp:
      break
  return out


class GetInfo():
    def __init__(self):
      lspcidrake = lspcian(commands.getoutput('lspcidrake').split('\n'))
      self.system_os_name = commands.getoutput("cat /etc/blackPanther-release | awk -Frelease '{ print $1 }'")
      if (self.system_os_name==""):
          self.system_os_name = commands.getoutput("cat /etc/release | awk -Frelease '{ print $1 }'")
      self.system_release = commands.getoutput("cat /etc/blackPanther-release | awk -Frelease '{ print $2 }'|sed 's|for.*||'")
      self.system_user_name = commands.getoutput("cat /etc/passwd | grep $USER| awk -F: '{ print $5\" \\n(\"$1\")\" }'")
      self.system_serial_name = commands.getoutput("cat /etc/sysconfig/edition-release | grep SN:")
      self.system_computer_name = commands.getoutput("uname -a|awk '{print $13\" \"$14\" (\"$2\")\"}'")
      self.system_processor_name = commands.getoutput("uname -p|awk '{print $4\" \"$5\" \"$6}'")
      self.system_memory_name = commands.getoutput("cat /proc/meminfo| grep MemTotal | awk -F: '{print $2}'| sed 's|       ||'")
      self.system_disks_name = dl(commands.getoutput("cat /proc/partitions| sed -e 's|major.*||'|grep d| awk '{print $4 \" \" $3}'"))
      self.system_video_name = lspcidrake[0]
      self.system_netdevice_name = lspcidrake[1]
      
      self.network_computer_name = commands.getoutput("echo $HOSTNAME")
      self.network_workgroup_name = commands.getoutput("cat /etc/samba/smb.conf | sed 's|#.*||'|grep workgroup|awk -F= '{ print $2 }'|sed 's| ||'")
      self.network_samba_status = commands.getoutput("[[ -n $(pidof smbd 2>/dev/null) ]]&& echo Running ")
      self.network_share_level = commands.getoutput("cat /etc/samba/smb.conf | sed 's|#.*||'|grep security|awk -F= '{ print $2 }'|sed 's| ||'")
      self.network_computer_name = commands.getoutput("echo $HOSTNAME")
      self.network_firewall_state = 'Unknown'
      self.video_memory =  commands.getoutput("cat /var/log/Xorg.0.log|grep \"VideoRam\"|sed 's|.*: ||'| awk '{ print $1 \" \" $2 }'")
      if (self.video_memory==""):
          self.video_memory =  commands.getoutput("cat /var/log/Xorg.0.log|grep \"VideoRAM\"|sed 's|.*: ||'| awk '{ print $1 \" \" $2 }'")
      #self.video_driver =  commands.getoutput("cat /var/log/Xorg.0.log|grep \"Driver for\"|sed 's|.*) ||'| awk -F: '{ print $1 }'")
      self.video_driver =  commands.getoutput("cat /var/log/Xorg.0.log|grep for |grep hipset|tail -n 1|awk -F: '{print $1}' | sed 's|.*)||'|tr [A-Z] [a-z]")
      if (self.video_driver==""):
    	 self.video_driver =  commands.getoutput("cat /var/log/Xorg.0.log|grep \"river for\" |tail -n 1|awk -F: '{print $1}' | sed 's|.*)||'|tr [A-Z] [a-z]")
      self.rendering_support = commands.getoutput("glxinfo | grep 'direct rendering' | sed 's|^d|D|'")
      self.desktop_effects = commands.getoutput("cat \"$HOME/.kde4/share/config/kwinrc\" | grep \"^Enabled=\"")
      if (self.desktop_effects==""):
          self.desktop_effects = commands.getoutput("Enabled=false")
      self.network_details = commands.getoutput("for i in `/sbin/ifconfig | grep Ethernet | awk '{print $1}'` ; do  ip=`/sbin/ifconfig $i | grep -e 'inet addr' -e 'Mask' | awk  '{print $2 \" \"$4}' | sed 's|addr|IP|'` && [ -n \"$ip\" ]||ip='Wait DHCP or not started' && echo \"$i $ip\"; done ")
      self.network_route = commands.getoutput("/sbin/route | grep default | awk '{print \"Gateway Device: \" $8 \" IP: \" $2 }'")
      #self.network_details = commands.getoutput("/sbin/ifconfig|grep Ethernet | sed 's|Link encap:Ethernet||'")
      self.hardware_list = commands.getoutput("lspci -v")
      self.core_data = commands.getoutput("uname -r")
      self.top_info = commands.getoutput("top -b | head -n 10 | tail -n 3 | awk '{print \"*: \"$2 \"  \"$9 \"% \" $12}'")
      #self.info_cpu_bar = commands.getoutput("while i=$(cat /proc/cpuinfo | grep MHz | head -n 1 |awk -F\": \" '{prin $2}');do sleep 2 && echo $i ; done ")



class WirelessStatus:

    ''' Signals '''
    SIOCGIWESSID = 0x8B1B # Get ESSID
    SIOCGIWMODE = 0x8B07  # Get Mode
    SIOCGIWRATE = 0x8B21  # Get Rate
    
    ''' Wireless Constans '''
    wKILO = 10**3
    wMEGA = 10**6
    wGIGA = 10**9

    ''' Byte constants '''
    bKILO = 2**10
    bMEGA = 2**20
    bGIGA = 2**30
    
    modes = ['Auto', 'Ad-Hoc', 'Managed', 'Master', 'Repeat', 'Second', 'Monitor']

    def __init__(self):
        ''' Constuctor '''
        self.class_path = '/sys/class/net'
        self.device = self.findWirelessInterface()
        self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    	self.wireless = "Found"
        if not self.device:
        #    QMessageBox.information(None, _("No Wireless Interface"), _("You don't have any wireless interface..."), QMessageBox.Ok)
    	    self.wireless = "None"
    	    self.signal = "0"
    	    print "None Wireless: " + self.wireless
	    #sys.exit()
        
    def findWirelessInterface(self):
        ''' Finds wireless interface '''
        fileName = 'wireless'
        for interface in os.listdir(self.class_path):
            if os.path.exists(os.path.join(self.class_path, interface, fileName)):
                return interface

    def returnInterfaceStatus(self):
        fileName = 'carrier'
        try:
            self.status = file(os.path.join(self.class_path, self.device, fileName)).readline().strip()
        except IOError:
            return 0
        return self.status

    def returnInterfaceName(self):
        ''' Returns the wireless interface name '''
        return self.device

    def returnLinkStatus(self):
        ''' Returns wireless link status % '''
        fileName = 'wireless/link'
        self.link = file(os.path.join(self.class_path, self.device, fileName)).readline().strip()
        return self.link
        #return int(self.link)
    
    def returnNoiseStatus(self):
        ''' Returns current noise level '''
        fileName = 'wireless/noise'
        self.noise = file(os.path.join(self.class_path, self.device, fileName)).readline().strip()
        #print "Wireless Nosie from 256: " + self.nosie
        return self.noise
        #return int(self.noise) - 256
    
    def returnSignalStatus(self):
        ''' Returns current signal level '''
        fileName = 'wireless/level'
        self.signal = file(os.path.join(self.class_path, self.device, fileName)).readline().strip()
        #print "Wireless Signal from 256: " + self.signal
        return self.signal
        #return int(self.signal) - 256
     
    def returnReceived(self):
        ''' Returns received bytes '''
        fileName = 'statistics/rx_bytes'
        self.rx = int(file(os.path.join(self.class_path, self.device, fileName)).readline().strip())
 
        if self.rx >= self.bGIGA:
            return "%i Gb" %(self.rx/self.bGIGA)

        if self.rx >= self.bMEGA:
            return "%i Mb" %(self.rx/self.bMEGA)

        return "%i Kb" %(self.rx/self.bKILO)

    def returnTransferred(self):
        ''' Returns transferred bytes '''
        fileName = 'statistics/tx_bytes'
        self.tx = int(file(os.path.join(self.class_path, self.device, fileName)).readline().strip())
 
        if self.tx >= self.bGIGA:
            return "%i Gb" %(self.tx/self.bGIGA)

        if self.tx >= self.bMEGA:
            return "%i Mb" %(self.tx/self.bMEGA)

        return "%i Kb" %(self.tx/self.bKILO)

    def returnESSID(self):
        ''' Returns essid of interface '''
        buffer, structure = self.__packRequest(32)
        i, result = self.__readInformation(self.SIOCGIWESSID, structure)
        if i > 0:
            return result
        return buffer.tostring().strip('\x00')

    def returnBitrate(self):
        ''' Returns bit rate of interface '''
        i, result = self.__readInformation(self.SIOCGIWRATE)
        if i > 0:
            return result

        size = struct.calcsize('ihbb')
        m, e, i, pad = struct.unpack('ihbb', result[:size])
        if e == 0:
            bitrate =  m
        else:
            bitrate = float(m) * 10**e

        if bitrate >= self.wGIGA:
            return "%i Gb/s" %(bitrate/self.wGIGA)

        if bitrate >= self.wMEGA:
            return "%i Mb/s" %(bitrate/self.wMEGA)

        if bitrate >= self.wKILO:
            return "%i Kb/s" %(bitrate/self.wKILO)

    def returnMode(self):
        ''' Returns operation mode of interface '''
        i, result = self.__readInformation(self.SIOCGIWMODE)
        if i > 0:
            return result
        mode = self.__unpackRequest('i', result[:4])[0]
        return self.modes[mode]

    ''' Internal Methods '''

    def __packRequest(self, bufferSize):
        """ Packs wireless request data for sending it to the kernel """
        buffer = array.array('c', '\0' * bufferSize)
        caddr_t, length = buffer.buffer_info()
        structure = struct.pack('Pi', caddr_t, length)
        return buffer, structure

    def __unpackRequest(self, format, packedRequest):
        """ Unpacks request with given format """
        return struct.unpack(format, packedRequest)

    def __readInformation(self, request, data = None):
        ''' Read information from interface '''
        if data is not None:
            buffer = 16 - len(self.device)
            requestedInterface = self.device + '\0' * buffer
            requestedInterface += data
        else:
            requestedInterface = (self.device + '\0' * 32)
        try:
            result = fcntl.ioctl(self.sockfd.fileno(), request, requestedInterface)
        except IOError, (i, e):
            return i, e

        return (0, result[16:])


      
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        self.CPU = Cpu()
        self.CPU.start()  # Itt inditom a szalat a CPU figyelesehez.
        self.wirelessStatus = WirelessStatus()
        self.Info = GetInfo()
        QtGui.QMainWindow.__init__(self)

	binDir = os.path.dirname(os.path.realpath( __file__ ))
	sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
        translator = QTranslator()
	translator.load('mit_' + QLocale.system().name(), binDir+'/translations')
	app.installTranslator(translator)

        MyInfo.setObjectName("MyInfo")
        MyInfo.resize(521, 538)
        MyInfo.setSizeGripEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MyInfo.sizePolicy().hasHeightForWidth())
        MyInfo.setSizePolicy(sizePolicy)
        MyInfo.setMinimumSize(QtCore.QSize(521, 538))
        MyInfo.setMaximumSize(QtCore.QSize(521, 538))
        MyInfo.setSizeGripEnabled(True)
        self.vboxlayout = QtGui.QVBoxLayout(MyInfo)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(11)
        self.vboxlayout.setObjectName("vboxlayout")
        self.tabWidget = QtGui.QTabWidget(MyInfo)
        self.tabWidget.setObjectName("tabWidget")
        self.Widget8 = QtGui.QWidget()
        self.Widget8.setObjectName("Widget8")
        self.groupBox = QtGui.QGroupBox(self.Widget8)
        self.groupBox.setGeometry(QtCore.QRect(220, 20, 251, 171))
        self.groupBox.setObjectName("groupBox")
        self.textLabel7 = QtGui.QLabel(self.groupBox)
        self.textLabel7.setGeometry(QtCore.QRect(10, 50, 90, 20))
        self.textLabel7.setWordWrap(False)
        self.textLabel7.setObjectName("textLabel7")
        self.os_name_text = QtGui.QLabel(self.groupBox)
        self.os_name_text.setGeometry(QtCore.QRect(90, 50, 100, 20))
        self.os_name_text.setWordWrap(False)
        self.os_name_text.setObjectName("os_name_text")
        self.textLabel9 = QtGui.QLabel(self.groupBox)
        self.textLabel9.setGeometry(QtCore.QRect(10, 70, 81, 20))
        self.textLabel9.setWordWrap(False)
        self.textLabel9.setObjectName("textLabel9")
        self.os_release_text = QtGui.QLabel(self.groupBox)
        self.os_release_text.setGeometry(QtCore.QRect(90, 70, 120, 20))
        self.os_release_text.setWordWrap(False)
        self.os_release_text.setObjectName("os_release_text")
        self.textLabel10 = QtGui.QLabel(self.groupBox)
        self.textLabel10.setGeometry(QtCore.QRect(10, 90, 61, 20))
        self.textLabel10.setWordWrap(False)
        self.textLabel10.setObjectName("textLabel10")
        self.os_user_text = QtGui.QLabel(self.groupBox)
        self.os_user_text.setGeometry(QtCore.QRect(70, 90, 171, 31))
        font = QtGui.QFont()
        font.setItalic(False)
        font.setUnderline(False)
        self.os_user_text.setFont(font)
        #self.os_user_text.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.os_user_text.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.os_user_text.setWordWrap(False)
        self.os_user_text.setObjectName("os_user_text")

        self.textLabel8 = QtGui.QLabel(self.groupBox)
        self.textLabel8.setGeometry(QtCore.QRect(10, 120, 181, 20))
        self.textLabel8.setWordWrap(False)
        self.textLabel8.setObjectName("textLabel8")
        self.os_serial_text = QtGui.QLabel(self.groupBox)
        self.os_serial_text.setGeometry(QtCore.QRect(10, 140, 230, 20))
        self.os_serial_text.setWordWrap(False)
        self.os_serial_text.setObjectName("os_serial_text")
        self.groupBox_2 = QtGui.QGroupBox(self.Widget8)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 200, 461, 251))
        self.groupBox_2.setObjectName("groupBox_2")
        self.progressBar = QtGui.QProgressBar(self.groupBox_2)
        self.progressBar.setGeometry(QtCore.QRect(30, 60, 191, 23))
        self.progressBar.setProperty("value", QtCore.QVariant(24))
        self.progressBar.setObjectName("progressBar")
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(30, 40, 131, 17))
        self.label.setObjectName("label")
        self.progressBar_2 = QtGui.QProgressBar(self.groupBox_2)
        self.progressBar_2.setGeometry(QtCore.QRect(250, 60, 191, 23))
        self.progressBar_2.setProperty("value", QtCore.QVariant(24))
        self.progressBar_2.setObjectName("progressBar_2")
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(250, 40, 191, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(30, 100, 191, 23))
        self.label_3.setObjectName("label_3")
        self.progressBar_3 = QtGui.QProgressBar(self.groupBox_2)
        #self.progressBar_3.setEnabled(False)
        self.progressBar_3.setGeometry(QtCore.QRect(30, 120, 191, 23))
        self.progressBar_3.setProperty("value", QtCore.QVariant(24))
        self.progressBar_3.setObjectName("progressBar_3")
        self.progressBar_4 = QtGui.QProgressBar(self.groupBox_2)
        self.progressBar_4.setGeometry(QtCore.QRect(250, 120, 191, 23))
        self.progressBar_4.setProperty("value", QtCore.QVariant(24))
        self.progressBar_4.setObjectName("progressBar_4")
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(250, 100, 191, 17))
        self.label_4.setObjectName("label_4")

        self.frame_2 = QtGui.QFrame(self.groupBox_2)
        self.frame_2.setEnabled(False)
        self.frame_2.setGeometry(QtCore.QRect(19, 99, 211, 141))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.wifi_data1 = QtGui.QLabel(self.frame_2)
        self.wifi_data1.setGeometry(QtCore.QRect(10, 50, 191, 16))
        self.wifi_data1.setObjectName("wifi_data1")
        self.wifi_data1_2 = QtGui.QLabel(self.frame_2)
        self.wifi_data1_2.setGeometry(QtCore.QRect(10, 70, 191, 16))
        self.wifi_data1_2.setObjectName("wifi_data1_2")
        self.wifi_data1_3 = QtGui.QLabel(self.frame_2)
        self.wifi_data1_3.setGeometry(QtCore.QRect(10, 90, 191, 16))
        self.wifi_data1_3.setObjectName("wifi_data1_3")
        self.wifi_data1_4 = QtGui.QLabel(self.frame_2)
        self.wifi_data1_4.setGeometry(QtCore.QRect(10, 110, 191, 16))
        self.wifi_data1_4.setObjectName("wifi_data1_4")

        self.other_datas_2 = QtGui.QLabel(self.groupBox_2)
        self.other_datas_2.setGeometry(QtCore.QRect(250, 170, 191, 20))
        self.other_datas_2.setObjectName("other_datas_2")
        self.other_datas_3 = QtGui.QLabel(self.groupBox_2)
        self.other_datas_3.setGeometry(QtCore.QRect(250, 190, 191, 51))
        self.other_datas_3.setObjectName("other_datas_3")
        self.other_datas_4 = QtGui.QLabel(self.groupBox_2)
        self.other_datas_4.setGeometry(QtCore.QRect(250, 220, 191, 20))
        self.other_datas_4.setObjectName("other_datas_4")
        self.frame_3 = QtGui.QFrame(self.groupBox_2)
        self.frame_3.setGeometry(QtCore.QRect(250, 149, 191, 21))
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.other_datas = QtGui.QLabel(self.frame_3)
        self.other_datas.setGeometry(QtCore.QRect(2, 0, 190, 20))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.other_datas.setFont(font)
        self.other_datas.setObjectName("other_datas")

        self.frame = QtGui.QFrame(self.Widget8)
        self.frame.setGeometry(QtCore.QRect(19, 29, 181, 161))
        self.frame.setStyleSheet("background-image: url(pics/logo.png);")
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.tabWidget.addTab(self.Widget8, "")
        self.TabPage = QtGui.QWidget()
        self.TabPage.setObjectName("TabPage")

        self.system_disks_name_text = QtGui.QGroupBox(self.TabPage)
        self.system_disks_name_text.setGeometry(QtCore.QRect(10, 220, 461, 231))
        self.system_disks_name_text.setObjectName("system_disks_name_text")
        self.textLabel2 = QtGui.QLabel(self.system_disks_name_text)
        self.textLabel2.setGeometry(QtCore.QRect(20, 30, 100, 20))
        self.textLabel2.setWordWrap(False)
        self.textLabel2.setObjectName("textLabel2")
        
        self.textLabel3 = QtGui.QLabel(self.system_disks_name_text)
        self.textLabel3.setGeometry(QtCore.QRect(20, 50, 100, 20))
        self.textLabel3.setWordWrap(False)
        self.textLabel3.setObjectName("textLabel3")
        
        self.textLabel4 = QtGui.QLabel(self.system_disks_name_text)
        self.textLabel4.setGeometry(QtCore.QRect(20, 70, 100, 20))
        self.textLabel4.setWordWrap(False)
        self.textLabel4.setObjectName("textLabel4")
        self.textLabel5 = QtGui.QLabel(self.system_disks_name_text)
        self.textLabel5.setGeometry(QtCore.QRect(20, 130, 100, 20))
        self.textLabel5.setWordWrap(False)
        self.textLabel5.setObjectName("textLabel5")
        self.textLabel12 = QtGui.QLabel(self.system_disks_name_text)
        self.textLabel12.setGeometry(QtCore.QRect(20, 90, 100, 20))
        self.textLabel12.setWordWrap(False)
        self.textLabel12.setObjectName("textLabel12")
        self.textLabel6 = QtGui.QLabel(self.system_disks_name_text)
        self.textLabel6.setGeometry(QtCore.QRect(20, 110, 131, 20))
        self.textLabel6.setWordWrap(False)
        self.textLabel6.setObjectName("textLabel6")
        self.system_computer_name_text = QtGui.QLabel(self.system_disks_name_text)
        self.system_computer_name_text.setGeometry(QtCore.QRect(150, 30, 261, 20))
        self.system_computer_name_text.setWordWrap(False)
        self.system_computer_name_text.setObjectName("system_computer_name_text")
        self.system_processor_name_text = QtGui.QLabel(self.system_disks_name_text)
        self.system_processor_name_text.setGeometry(QtCore.QRect(150, 50, 261, 20))
        self.system_processor_name_text.setWordWrap(False)
        self.system_processor_name_text.setObjectName("system_processor_name_text")

        self.system_memory_name_text = QtGui.QLabel(self.system_disks_name_text)
        self.system_memory_name_text.setGeometry(QtCore.QRect(150, 70, 261, 20))
        self.system_memory_name_text.setWordWrap(False)
        self.system_memory_name_text.setObjectName("system_memory_name_text")
        
        self.system_memory_name_text_2 = QtGui.QLabel(self.system_disks_name_text)
        self.system_memory_name_text_2.setGeometry(QtCore.QRect(150, 140, 291, 101))
        self.system_memory_name_text_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.system_memory_name_text_2.setWordWrap(False)
        self.system_memory_name_text_2.setObjectName("system_memory_name_text_2")

        self.system_video_name_text = QtGui.QLabel(self.system_disks_name_text)
        self.system_video_name_text.setGeometry(QtCore.QRect(150, 90, 261, 20))
        self.system_video_name_text.setWordWrap(False)
        self.system_video_name_text.setObjectName("system_video_name_text")

        self.system_netdevice_name_text = QtGui.QLabel(self.system_disks_name_text)
        self.system_netdevice_name_text.setGeometry(QtCore.QRect(150, 110, 281, 20))
        self.system_netdevice_name_text.setWordWrap(False)
        self.system_netdevice_name_text.setObjectName("system_netdevice_name_text")

        self.system_manage_disk_button = QtGui.QPushButton(self.system_disks_name_text)
        self.system_manage_disk_button.setGeometry(QtCore.QRect(10, 180, 121, 31))
        self.system_manage_disk_button.setObjectName("system_manage_disk_button")
        self.connect(self.system_manage_disk_button,QtCore.SIGNAL("clicked()"),self.slotPartedit)

        self.hardware_reviews = QtGui.QGroupBox(self.TabPage)
        self.hardware_reviews.setGeometry(QtCore.QRect(10, 10, 461, 201))
        self.hardware_reviews.setObjectName("hardware_reviews")

        self.device_manager_button = QtGui.QPushButton(self.hardware_reviews)
        self.device_manager_button.setGeometry(QtCore.QRect(260, 130, 180, 31))
        self.device_manager_button.setObjectName("device_manager_button")
        self.connect(self.device_manager_button,QtCore.SIGNAL("clicked()"),self.slotDevManButton)

        self.textLabel13 = QtGui.QLabel(self.hardware_reviews)
        self.textLabel13.setGeometry(QtCore.QRect(150, 30, 291, 60))
        self.textLabel13.setWordWrap(False)
        self.textLabel13.setObjectName("textLabel13")

        self.hardw_page_logo = QtGui.QFrame(self.hardware_reviews)
        self.hardw_page_logo.setGeometry(QtCore.QRect(10, 20, 125, 125))
        self.hardw_page_logo.setStyleSheet("background-image: url(pics/hwinfo.png);")
        self.hardw_page_logo.setFrameShape(QtGui.QFrame.StyledPanel)
        self.hardw_page_logo.setFrameShadow(QtGui.QFrame.Raised)
        self.hardw_page_logo.setObjectName("hardw_page_logo")

        self.tabWidget.addTab(self.TabPage, "")
        self.TabPage1 = QtGui.QWidget()
        self.TabPage1.setObjectName("TabPage1")

        self.pushButton7_2 = QtGui.QPushButton(self.TabPage1)
        self.pushButton7_2.setEnabled(False)
        self.pushButton7_2.setGeometry(QtCore.QRect(20, 430, 130, 20))
        self.pushButton7_2.setObjectName("pushButton7_2")

        self.pushButton8 = QtGui.QPushButton(self.TabPage1)
        self.pushButton8.setEnabled(False)
        self.pushButton8.setGeometry(QtCore.QRect(180, 430, 140, 20))
        self.pushButton8.setObjectName("pushButton8")

        self.button_hardw3 = QtGui.QPushButton(self.TabPage1)
        self.button_hardw3.setGeometry(QtCore.QRect(340, 429, 130, 21))
        self.button_hardw3.setObjectName("button_hardw3")
        self.connect(self.button_hardw3,QtCore.SIGNAL("clicked()"),self.slotHardw3)

        self.treeView = QtGui.QTextBrowser(self.TabPage1)
        #self.treeView.setEnabled(False)
        self.treeView.setGeometry(QtCore.QRect(20, 10, 451, 401))
        self.treeView.setObjectName("treeView")

        self.tabWidget.addTab(self.TabPage1, "")
        self.Widget9 = QtGui.QWidget()
        self.Widget9.setObjectName("Widget9")
        self.groupBox7 = QtGui.QGroupBox(self.Widget9)
        self.groupBox7.setGeometry(QtCore.QRect(10, 210, 471, 221))
        self.groupBox7.setObjectName("groupBox7")

        self.netdev_config_button = QtGui.QPushButton(self.groupBox7)
        self.netdev_config_button.setGeometry(QtCore.QRect(340, 30, 110, 31))
        self.netdev_config_button.setObjectName("netdev_config_button")
        self.connect(self.netdev_config_button,QtCore.SIGNAL("clicked()"),self.slotDevConfig)

        self.netdev_macchg_button = QtGui.QPushButton(self.groupBox7)
        self.netdev_macchg_button.setGeometry(QtCore.QRect(340, 70, 110, 31))
        self.netdev_macchg_button.setObjectName("netdev_macchg_button")
        self.connect(self.netdev_macchg_button,QtCore.SIGNAL("clicked()"),self.slotMacConfig)

        self.network_wakeon_button = QtGui.QPushButton(self.groupBox7)
        self.network_wakeon_button.setGeometry(QtCore.QRect(340, 110, 110, 31))
        self.network_wakeon_button.setObjectName("network_wakeon_button")
        self.connect(self.network_wakeon_button,QtCore.SIGNAL("clicked()"),self.slotWakeOnLan)

        self.network_details = QtGui.QLabel(self.groupBox7)
        self.network_details.setGeometry(QtCore.QRect(20, 40, 280, 140))
        self.network_details.setWordWrap(False)
        self.network_details.setObjectName("network_details")

        self.groupBox6 = QtGui.QGroupBox(self.Widget9)
        self.groupBox6.setGeometry(QtCore.QRect(17, 18, 451, 201))
        self.groupBox6.setObjectName("groupBox6")

        self.textLabel1_6 = QtGui.QLabel(self.groupBox6)
        self.textLabel1_6.setGeometry(QtCore.QRect(20, 150, 150, 20))
        self.textLabel1_6.setWordWrap(False)
        self.textLabel1_6.setObjectName("textLabel1_6")
        self.textLabel4_2 = QtGui.QLabel(self.groupBox6)
        self.textLabel4_2.setGeometry(QtCore.QRect(20, 120, 150, 20))
        self.textLabel4_2.setWordWrap(False)
        self.textLabel4_2.setObjectName("textLabel4_2")
        self.textLabel3_2 = QtGui.QLabel(self.groupBox6)
        self.textLabel3_2.setGeometry(QtCore.QRect(20, 90, 150, 20))
        self.textLabel3_2.setWordWrap(False)
        self.textLabel3_2.setObjectName("textLabel3_2")
        self.textLabel2_2 = QtGui.QLabel(self.groupBox6)
        self.textLabel2_2.setGeometry(QtCore.QRect(20, 60, 150, 20))
        self.textLabel2_2.setWordWrap(False)
        self.textLabel2_2.setObjectName("textLabel2_2")
        self.textLabel1 = QtGui.QLabel(self.groupBox6)
        self.textLabel1.setGeometry(QtCore.QRect(20, 30, 150, 20))
        self.textLabel1.setWordWrap(False)
        self.textLabel1.setObjectName("textLabel1")

        
        self.network_computer_name_text = QtGui.QLabel(self.groupBox6)
        self.network_computer_name_text.setGeometry(QtCore.QRect(200, 30, 280, 20))
        self.network_computer_name_text.setWordWrap(False)
        self.network_computer_name_text.setObjectName("network_computer_name_text")
        self.network_workgroup_name_text = QtGui.QLabel(self.groupBox6)
        self.network_workgroup_name_text.setGeometry(QtCore.QRect(200, 60, 280, 20))
        self.network_workgroup_name_text.setWordWrap(False)
        self.network_workgroup_name_text.setObjectName("network_workgroup_name_text")
        self.network_samba_status_text = QtGui.QLabel(self.groupBox6)
        self.network_samba_status_text.setGeometry(QtCore.QRect(200, 90, 280, 20))
        self.network_samba_status_text.setWordWrap(False)
        self.network_samba_status_text.setObjectName("network_samba_status_text")
        self.network_share_level_text = QtGui.QLabel(self.groupBox6)
        self.network_share_level_text.setGeometry(QtCore.QRect(200, 120, 280, 20))
        self.network_share_level_text.setWordWrap(False)
        self.network_share_level_text.setObjectName("network_share_level_text")
        self.network_firewall_state_text = QtGui.QLabel(self.groupBox6)
        self.network_firewall_state_text.setGeometry(QtCore.QRect(200, 150, 280, 20))
        self.network_firewall_state_text.setWordWrap(False)
        self.network_firewall_state_text.setObjectName("network_firewall_state_text")

        self.tabWidget.addTab(self.Widget9, "")
        self.TabPage2 = QtGui.QWidget()
        self.TabPage2.setObjectName("TabPage2")
        self.groupBox5 = QtGui.QGroupBox(self.TabPage2)
        self.groupBox5.setGeometry(QtCore.QRect(10, 300, 470, 100))
        self.groupBox5.setObjectName("groupBox5")
        self.groupBox4 = QtGui.QGroupBox(self.TabPage2)
        self.groupBox4.setGeometry(QtCore.QRect(10, 20, 470, 291))
        self.groupBox4.setObjectName("groupBox4")
        self.textLabel6_2 = QtGui.QLabel(self.groupBox4)
        self.textLabel6_2.setGeometry(QtCore.QRect(30, 60, 410, 20))
        self.textLabel6_2.setWordWrap(False)
        self.textLabel6_2.setObjectName("textLabel6_2")
        self.textLabel5_2 = QtGui.QLabel(self.groupBox4)
        self.textLabel5_2.setGeometry(QtCore.QRect(30, 30, 410, 20))
        self.textLabel5_2.setWordWrap(False)
        self.textLabel5_2.setObjectName("textLabel5_2")
        self.textLabel7_2 = QtGui.QLabel(self.groupBox4)
        self.textLabel7_2.setGeometry(QtCore.QRect(30, 90, 410, 20))
        self.textLabel7_2.setWordWrap(False)
        self.textLabel7_2.setObjectName("textLabel7_2")

        self.textLabel8_2 = QtGui.QLabel(self.groupBox4)
        self.textLabel8_2.setGeometry(QtCore.QRect(30, 120, 410, 20))
        self.textLabel8_2.setWordWrap(False)
        self.textLabel8_2.setObjectName("textLabel8_2")

        self.textAbout = QtGui.QLabel(self.groupBox5)
        # a mezo parameterei	(tav balrol |felso tav| szelessege |mezomagassag )
        self.textAbout.setGeometry(QtCore.QRect(40, 24, 440, 80))
        self.textAbout.setWordWrap(False)
        self.textAbout.setObjectName("textAbout")

        self.tabWidget.addTab(self.TabPage2, "")
        self.vboxlayout.addWidget(self.tabWidget)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")
        self.buttonHelp = QtGui.QPushButton(MyInfo)
        self.buttonHelp.setAutoDefault(True)
        self.buttonHelp.setObjectName("buttonHelp")
        self.hboxlayout.addWidget(self.buttonHelp)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.buttonOk = QtGui.QPushButton(MyInfo)
        self.buttonOk.setEnabled(False)
        self.buttonOk.setAutoDefault(True)
        self.buttonOk.setDefault(True)
        self.buttonOk.setObjectName("buttonOk")
        self.hboxlayout.addWidget(self.buttonOk)
        self.buttonCancel = QtGui.QPushButton(MyInfo)
        self.buttonCancel.setAutoDefault(True)
        self.buttonCancel.setObjectName("buttonCancel")
        self.hboxlayout.addWidget(self.buttonCancel)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(MyInfo)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonOk, QtCore.SIGNAL("clicked()"), MyInfo.accept)
        QtCore.QObject.connect(self.buttonCancel, QtCore.SIGNAL("clicked()"), MyInfo.reject)
        QtCore.QMetaObject.connectSlotsByName(MyInfo)

        self.time = QtCore.QTimer()
        QtCore.QObject.connect(self.time, QtCore.SIGNAL("timeout()"), self.timeoutSlot)
        self.time.start(2000)


    def retranslateUi(self, MyInfo):
        MyInfo.setWindowTitle(QtGui.QApplication.translate("MyInfo", "blackPanther OS MyInfo", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MyInfo", "System infromations", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel7.setText(QtGui.QApplication.translate("MyInfo", "<b>OS name:</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.os_name_text.setText(QtGui.QApplication.translate("MyInfo","<u> "+ self.Info.system_os_name+"</u>", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel9.setText(QtGui.QApplication.translate("MyInfo", "<b>Release:</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.os_release_text.setText(QtGui.QApplication.translate("MyInfo", self.Info.system_release, None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel10.setText(QtGui.QApplication.translate("MyInfo", "<b>User:</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.os_user_text.setText(QtGui.QApplication.translate("MyInfo", self.Info.system_user_name, None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel8.setText(QtGui.QApplication.translate("MyInfo", "<b>Serial number:</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.os_serial_text.setText(QtGui.QApplication.translate("MyInfo", self.Info.system_serial_name, None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MyInfo", "System usage", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MyInfo", "CPU usage", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MyInfo", "Memory usage", None, QtGui.QApplication.UnicodeUTF8))
        #if (self.wirelessStatus.returnInterfaceName()=="None"):
        #    print "1" + wirelessStatus.device
	#self.label_3.setText(QtGui.QApplication.translate("MyInfo", "Not Available any Wifi Device", None, QtGui.QApplication.UnicodeUTF8))
    	#else:
    	    #print "2" + self.wirelessStatus.findWirelessInterface()
    	    #print self.wirelessStatus.returnInterfaceName()
    	    #self.label_3.setText(QtGui.QApplication.translate("MyInfo", "Wireless signal ["+ self.wirelessStatus.returnInterfaceName() +"]", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MyInfo", "Swap usage", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Widget8), QtGui.QApplication.translate("MyInfo", "Main page", None, QtGui.QApplication.UnicodeUTF8))
        self.system_disks_name_text.setTitle(QtGui.QApplication.translate("MyInfo", "System review", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel2.setText(QtGui.QApplication.translate("MyInfo", "<b>Computer: </b>", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel3.setText(QtGui.QApplication.translate("MyInfo", "<b>Processor: </b>", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel4.setText(QtGui.QApplication.translate("MyInfo", "<b>Memory: </b>", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel5.setText(QtGui.QApplication.translate("MyInfo", "<b>Disks: </b>", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel12.setText(QtGui.QApplication.translate("MyInfo", "<b>Video: </b>", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel6.setText(QtGui.QApplication.translate("MyInfo", "<b>Network  device: </b>", None, QtGui.QApplication.UnicodeUTF8))
        self.system_computer_name_text.setText(QtGui.QApplication.translate("MyInfo", self.Info.system_computer_name, None, QtGui.QApplication.UnicodeUTF8))
        self.system_processor_name_text.setText(QtGui.QApplication.translate("MyInfo", self.Info.system_processor_name, None, QtGui.QApplication.UnicodeUTF8))
        self.system_memory_name_text.setText(QtGui.QApplication.translate("MyInfo", self.Info.system_memory_name, None, QtGui.QApplication.UnicodeUTF8))
        self.system_memory_name_text_2.setText(QtGui.QApplication.translate("MyInfo", self.Info.system_disks_name, None, QtGui.QApplication.UnicodeUTF8))
        self.system_video_name_text.setText(QtGui.QApplication.translate("MyInfo", self.Info.system_video_name, None, QtGui.QApplication.UnicodeUTF8))
        self.system_netdevice_name_text.setText(QtGui.QApplication.translate("MyInfo", self.Info.system_netdevice_name, None, QtGui.QApplication.UnicodeUTF8))
        self.hardware_reviews.setTitle(QtGui.QApplication.translate("MyInfo", "Hardwares reviews", None, QtGui.QApplication.UnicodeUTF8))
        self.device_manager_button.setText(QtGui.QApplication.translate("MyInfo", "Device manager", None, QtGui.QApplication.UnicodeUTF8))
        self.system_manage_disk_button.setText(QtGui.QApplication.translate("MyInfo", "Manage disks", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel13.setText(QtGui.QApplication.translate("MyInfo", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Toga Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:x-large; font-weight:600;\"><span style=\" font-size:x-large;\">Here available the device </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:x-large; font-weight:600;\"><span style=\" font-size:x-large;\">configuration tool...</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TabPage), QtGui.QApplication.translate("MyInfo", "Hardwares", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton7_2.setText(QtGui.QApplication.translate("MyInfo", "Propeties", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton8.setText(QtGui.QApplication.translate("MyInfo", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.button_hardw3.setText(QtGui.QApplication.translate("MyInfo", "Add new ", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TabPage1), QtGui.QApplication.translate("MyInfo", "Device lists", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox7.setTitle(QtGui.QApplication.translate("MyInfo", "Configuration and Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.netdev_config_button.setText(QtGui.QApplication.translate("MyInfo", "Configure", None, QtGui.QApplication.UnicodeUTF8))
        self.netdev_macchg_button.setText(QtGui.QApplication.translate("MyInfo", "Mac change", None, QtGui.QApplication.UnicodeUTF8))
        self.network_wakeon_button.setText(QtGui.QApplication.translate("MyInfo", "WakeOn", None, QtGui.QApplication.UnicodeUTF8))
        self.network_details.setText(QtGui.QApplication.translate("MyInfo", "Network Devices Details: \n\n" 
        + self.Info.network_details + "\n\n" + self.Info.network_route, 
    					None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox6.setTitle(QtGui.QApplication.translate("MyInfo", "Status", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel4_2.setText(QtGui.QApplication.translate("MyInfo", " <b>Share level:  </b>", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel3_2.setText(QtGui.QApplication.translate("MyInfo", " <b>Samba service: </b>", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel2_2.setText(QtGui.QApplication.translate("MyInfo", " <b>Workgroup: </b>", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1.setText(QtGui.QApplication.translate("MyInfo", " <b>Computer name: </b>", None, QtGui.QApplication.UnicodeUTF8))
        self.network_computer_name_text.setText(QtGui.QApplication.translate("MyInfo", self.Info.network_computer_name, None, QtGui.QApplication.UnicodeUTF8))
        self.network_workgroup_name_text.setText(QtGui.QApplication.translate("MyInfo",  self.Info.network_workgroup_name, None, QtGui.QApplication.UnicodeUTF8))

        if (self.Info.network_samba_status=="Running"):
    	    self.network_samba_status_text.setText(QtGui.QApplication.translate("MyInfo", "Available", None, QtGui.QApplication.UnicodeUTF8))
        else:
    	    self.network_samba_status_text.setText(QtGui.QApplication.translate("MyInfo", "Not available", None, QtGui.QApplication.UnicodeUTF8))
    	    
        self.network_share_level_text.setText(QtGui.QApplication.translate("MyInfo", self.Info.network_share_level, None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_6.setText(QtGui.QApplication.translate("MyInfo", "<b>Firewall state: </b>", None, QtGui.QApplication.UnicodeUTF8))
        self.network_firewall_state_text.setText(QtGui.QApplication.translate("MyInfo", self.Info.network_firewall_state, None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Widget9), QtGui.QApplication.translate("MyInfo", "Network", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox5.setTitle(QtGui.QApplication.translate("MyInfo", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.textAbout.setText(QtGui.QApplication.translate("MyInfo", "The MyInfo-tool the under development by blackPanther Europe.<b> <br>If You have any ide, please send for me:</br><br><br> info@blackpanther.hu", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox4.setTitle(QtGui.QApplication.translate("MyInfo", "Status", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel6_2.setText(QtGui.QApplication.translate("MyInfo", "<b>Used Video Driver: </b>" + self.Info.video_driver, None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel5_2.setText(QtGui.QApplication.translate("MyInfo", "<b>Available Video Memory: </b>" + self.Info.video_memory, None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel7_2.setText(QtGui.QApplication.translate("MyInfo", "<b>Use 3D </b>" + self.Info.rendering_support, None, QtGui.QApplication.UnicodeUTF8))
        
        self.other_datas.setText(QtGui.QApplication.translate("MyInfo", "* "+ self.Info.core_data, None, QtGui.QApplication.UnicodeUTF8))
    	self.other_datas_2.setText(QtGui.QApplication.translate("MyInfo", "<u> Top process: user  -  cpu  -  app</u>", None, QtGui.QApplication.UnicodeUTF8))

        if (self.Info.desktop_effects=="Enabled=true"):
    	    self.textLabel8_2.setText(QtGui.QApplication.translate("MyInfo", "<b>Dektop Effects Usage: </b> " "Enabled", None, QtGui.QApplication.UnicodeUTF8))
        elif (self.Info.desktop_effects=="Enabled=false"):
    	    self.textLabel8_2.setText(QtGui.QApplication.translate("MyInfo", "<b>Dektop Effects Usage: </b> " "Disabled", None, QtGui.QApplication.UnicodeUTF8))
        else:
    	    self.textLabel8_2.setText(QtGui.QApplication.translate("MyInfo", "<b>Dektop Effects Usage: </b>" "Unknown or not available info", None, QtGui.QApplication.UnicodeUTF8))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TabPage2), QtGui.QApplication.translate("MyInfo", "Performance", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonHelp.setText(QtGui.QApplication.translate("MyInfo", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonHelp.setShortcut(QtGui.QApplication.translate("MyInfo", "F1", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonOk.setText(QtGui.QApplication.translate("MyInfo", "&OK", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonCancel.setText(QtGui.QApplication.translate("MyInfo", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.treeView.setText(QtGui.QApplication.translate("MyInfo", "" + self.Info.hardware_list, None, QtGui.QApplication.UnicodeUTF8))

    def get_memory_usage(self):
        self.m = commands.getoutput("free").split()
        mt = int(self.m[7])
        mu = int(self.m[8])
        mc = int(self.m[12])
        return int(((mu - mc)* 1.0 / mt) * 100)

    def get_swap_usage(self):
        mt = int(self.m[18])
        mu = int(self.m[19])
        return int((mu * 1.0 / mt) * 100)

#    def get_cpu_usage(self):
#        print int(float(commands.getoutput("ps aux | awk 'NR > 0 {s += $3}; END {print s}'")))
#        print commands.getoutput("top -b | head -n 4 | grep Cpu | awk -F% '{print $1}' | sed 's|.*: ||'")
#        print deltaTime(2)
#        return int(float(commands.getoutput("ps aux | awk 'NR > 0 {s += $3}; END {print s}'")))
#        return deltaTime(2)

    def timeoutSlot(self):
	if  (self.wirelessStatus.wireless=="None"):
	    self.label_3.setText(QtGui.QApplication.translate("MyInfo", "Not Available Any Wifi Device", None, QtGui.QApplication.UnicodeUTF8))
    	    self.progressBar_3.setEnabled(False)
    	    self.progressBar_3.setProperty("value", QtCore.QVariant(0))
    	    self.progressBar.setProperty("value", QtCore.QVariant(self.CPU.get_cpu_usage)) # ITT VOLT A HIBA OKA!!!!!!!!!!!!!!!!!
    	    self.progressBar_2.setProperty("value", QtCore.QVariant(self.get_memory_usage()))
    	    self.progressBar_4.setProperty("value", QtCore.QVariant(self.get_swap_usage()))
    	else:
    	    self.progressBar_3.setEnabled(True)
    	    interfaceESSID = self.wirelessStatus.returnESSID()
    	    interfaceMode = self.wirelessStatus.returnMode()
    	    linkStatus = self.wirelessStatus.returnLinkStatus()
    	    noiseStatus = self.wirelessStatus.returnNoiseStatus()
    	    signalStatus = self.wirelessStatus.returnSignalStatus()
    	    bitRate = self.wirelessStatus.returnBitrate()
    	    received = self.wirelessStatus.returnReceived()
    	    transferred = self.wirelessStatus.returnTransferred()
	    self.interfaceName = self.wirelessStatus.returnInterfaceName()
    	    #print "Wireless data:\n * " + signalStatus + " Device: " + interfaceName + ", Mode: " + interfaceMode + 
    	    #", ID " + interfaceESSID + " Transferred: " + transferred + " Recevied: " + received + ", Signal " + signalStatus +", Nosie: "+ noiseStatus +" LinkStatus: " + linkStatus
    	    self.progressBar.setProperty("value", QtCore.QVariant(self.CPU.get_cpu_usage))  # ITT IS UGYANAZ VOLT A HIBA
    	    self.progressBar_2.setProperty("value", QtCore.QVariant(self.get_memory_usage()))
    	    self.progressBar_3.setProperty("value", QtCore.QVariant((int(signalStatus) / 256.0) * 100))
    	    self.progressBar_4.setProperty("value", QtCore.QVariant(self.get_swap_usage()))
    	    self.label_3.setText(QtGui.QApplication.translate("MyInfo", "Wireless signal   " + "  <b>["+ self.wirelessStatus.returnInterfaceName() +"]</b>", None, QtGui.QApplication.UnicodeUTF8))

    	    self.wifi_data1.setText(QtGui.QApplication.translate("MyInfo", "ESSID: " + interfaceESSID, None, QtGui.QApplication.UnicodeUTF8))
    	    self.wifi_data1_2.setText(QtGui.QApplication.translate("MyInfo", "Mode: "+interfaceMode+ " Rate: "+bitRate, None, QtGui.QApplication.UnicodeUTF8))
    	    self.wifi_data1_3.setText(QtGui.QApplication.translate("MyInfo", "Noise: "+noiseStatus+ " Link: "+linkStatus, None, QtGui.QApplication.UnicodeUTF8))
    	    self.wifi_data1_4.setText(QtGui.QApplication.translate("MyInfo", "In/Out: "+ transferred+" / "+received, None, QtGui.QApplication.UnicodeUTF8))
    	    self.other_datas_3.setText(QtGui.QApplication.translate("MyInfo", self.Info.top_info, None, QtGui.QApplication.UnicodeUTF8))
    	    #self.other_datas_4.setText(QtGui.QApplication.translate("MyInfo", "other_datas", None, QtGui.QApplication.UnicodeUTF8))

    def slotDevManButton(self):
        print "Launch device manager... \n>"
        os.popen("/usr/sbin/harddrake2")
        
    def slotDeleteDev(self):
        print "UI slotDeleteDev(): Not implemented yet\n>"

    def slotHardw3(self):
        print "Launch device manager... \n>"
        os.popen('myinfo-tool addhw')

    def slotPartedit(self):
        print "Launch Partition Editor... \n>"
        os.popen("kdesu default-partedit")

    def slotDevConfig(self):
        print "Launch network configure... \n>"
        os.popen("draknetcenter")

    def slotMacConfig(self):
        print "Launch MAC configure... \n>"
        os.popen("myinfo-tool mac")

    def slotWakeOnLan(self):
        print "Launc Wake On Lan... \n>"
        os.popen("./kwakeonlan.py")

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MyInfo = QtGui.QDialog()
    ui = MainWindow()
    #ui = Ui_MyInfo()
    #ui.setupUi(MyInfo)
    MyInfo.show()
    sys.exit(app.exec_())
