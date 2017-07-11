# -*- coding: utf-8 -*-
import sys

from PyQt4 import QtCore, QtGui
#from timer import Ui_MainWindow

class progress(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super(progress, self).__init__(parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ctimer = QtCore.QTimer()
		self.stimer = QtCore.QTimer()
		#buttons
		self.constant()
		# constant timer
		QtCore.QObject.connect(self.ctimer, QtCore.SIGNAL("timeout()"), self.constantUpdate)
		
		QtCore.QMetaObject.connectSlotsByName(self)
	
	def constant(self):
		"""
		Start the constant timer
		"""
		self.ctimer.start(1000)
		
	def constantUpdate(self):
		"""
		slot for constant timer timeout
		"""
		val = self.ui.constantProgress.value() + 10
		if val > 100:
			sys.exit()
			val = 0
		self.ui.constantProgress.setValue(val)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(337, 151)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.constantProgress = QtGui.QProgressBar(self.centralwidget)
        self.constantProgress.setProperty("value", 0)
        self.constantProgress.setObjectName("constantProgress")
        self.gridLayout.addWidget(self.constantProgress, 1, 0, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setWeight(75)
        font.setItalic(True)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 337, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", " Reading System Parameters....", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = progress()
	myapp.show()
	sys.exit(app.exec_())
