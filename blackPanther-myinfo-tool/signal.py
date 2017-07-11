# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'timer.ui'
#
# Created: Sat Dec 19 03:50:48 2009
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

#from PyQt4 import QtCore, QtGui
import sys, re, os, string, signal, socket, array, struct, fcntl

class WirelessStatus(object):

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
        #if not self.device:
        #    QMessageBox.information(None, _("No Wireless Interface"), _("You don't have any wireless interface..."), QMessageBox.Ok)
        #    sys.exit(1)
        
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
