#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import QHttp

import time,sys,os

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

#import update
version, url_to_download = os.popen('python ./update.py').read().replace('\n','').split(" | ")

if not url_to_download:
    print "Download URL not found!"
    cancelDownload()
    sys.exit(1)
#url_to_download = sys.argv[1]
#version = sys.argv[2:]

if not version:
    version = "unknown"

class Downloader(QDialog):
    def __init__(self, parent=None):
        super(Downloader, self).__init__(parent)
        self.setMaximumSize(400, 200)
        self.setMinimumSize(400, 200)
        self.resize(400, 200)

        Box = QDialogButtonBox()
        anime = QLabel('Dialog', self)
        anime.setMaximumSize(60, 60)
        anime.setGeometry(QRect(0, 0, 71, 71))
        anime.sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        anime.sizePolicy.setHorizontalStretch(0)
        anime.sizePolicy.setVerticalStretch(0)
        anime.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred)
        anime.setScaledContents(True)
        anime.setObjectName(_fromUtf8("Downloadgif"))

        movie = QMovie("dw.gif", QByteArray(), self) 
        movie.setCacheMode(QMovie.CacheAll) 
        movie.setSpeed(100) 
        anime.setMovie(movie) 

        self.httpGetId = 0
        self.httpRequestAborted = False
        self.statusLabel = QLabel('Downloading...\nThe New version (%s)' % version +' of Profiler')
        # setGeometry(x_pos, y_pos, width, height)
        self.statusLabel.setGeometry(QRect(90, 20, 221, 41))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusLabel.sizePolicy().hasHeightForWidth())
        self.statusLabel.setSizePolicy(sizePolicy)
        self.statusLabel.setAlignment(Qt.AlignLeft) 
        font = QFont()
        font.setFamily(_fromUtf8("URW Gothic L"))
        font.setPointSize(11)
        font.setWeight(75)
        font.setItalic(True)
        font.setBold(True)
        self.statusLabel.setFont(font)
        self.statusLabel.setWordWrap(True)
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))

        self.closeButton = QPushButton("Close")
        self.closeButton.setAutoDefault(False)

        self.progressBar = QProgressBar()

        Box.addButton(self.closeButton, QDialogButtonBox.RejectRole)

        self.http = QHttp(self)
        self.http.requestFinished.connect(self.httpRequestFinished)
        self.http.dataReadProgress.connect(self.updateDataReadProgress)
        self.http.responseHeaderReceived.connect(self.readResponseHeader)
        self.closeButton.clicked.connect(self.cancelDownload)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(anime) 
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addWidget(self.progressBar)
        mainLayout.addWidget(Box)
        self.setLayout(mainLayout)

        movie.start() 

        self.setWindowTitle('Profiler Updates Download')
        self.downloadFile()
        self.retranslateUi(Downloader)
        #QMetaObject.connectSlotsByName(Downloader)

    def downloadFile(self):
        url = QUrl(url_to_download)
        fileInfo = QFileInfo(url.path())
        fileName = fileInfo.fileName()

        if QFile.exists(fileName):
            QFile.remove(fileName)

        self.outFile = QFile(fileName)
        if not self.outFile.open(QIODevice.WriteOnly):
            QMessageBox.information(self, 'Error',
                    'Unable to save the file %s: %s.' % (fileName, self.outFile.errorString()))
            self.outFile = None
            return

        mode = QHttp.ConnectionModeHttp
        port = url.port()
        if port == -1:
            port = 0
        self.http.setHost(url.host(), mode, port)
        self.httpRequestAborted = False

        path = QUrl.toPercentEncoding(url.path(), "!$&'()*+,;=:@/")
        if path:
            path = str(path)
        else:
            path = '/'

        self.httpGetId = self.http.get(path, self.outFile)

    def cancelDownload(self):
        self.statusLabel.setText("Download canceled.")
        self.httpRequestAborted = True
        self.http.abort()
        self.close()

    def httpRequestFinished(self, requestId, error):
        if requestId != self.httpGetId:
            return

        if self.httpRequestAborted:
            if self.outFile is not None:
                self.outFile.close()
                self.outFile.remove()
                self.outFile = None
            return

        self.outFile.close()

        if error:
            self.outFile.remove()
            QMessageBox.information(self, 'Error',
                    'Download failed: %s.' % self.http.errorString())

        self.statusLabel.setText('Finished!')

    def readResponseHeader(self, responseHeader):
        # Check for genuine error conditions.
        if responseHeader.statusCode() not in (200, 300, 301, 302, 303, 307):
            QMessageBox.information(self, 'Error',
                    'Download failed: %s.' % responseHeader.reasonPhrase())
            self.httpRequestAborted = True
            self.http.abort()

    def updateDataReadProgress(self, bytesRead, totalBytes):
        if self.httpRequestAborted:
            return
        self.progressBar.setMaximum(totalBytes)
        self.progressBar.setValue(bytesRead)


    def retranslateUi(self, Downloader):
        self.setWindowTitle(QApplication.translate("Downloader", "Downloader", None, QApplication.UnicodeUTF8))
        self.statusLabel.setText(QApplication.translate("Downloader", 'Downloading...\nThe New version (%s)' % version +' of Profiler', None, QApplication.UnicodeUTF8))
        self.closeButton.setText(QApplication.translate("Downloader", "Cancel", None, QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    downloader = Downloader()
    downloader.show()
    sys.exit(app.exec_())
