#! /usr/bin/env python
#***************************************************************************
# *   Copyright (C) jofko by jofko   *
# *   joffko@gmail.com
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU General Public License for more details.                          *
# *                                                                         *
# *   You should have received a copy of the GNU General Public License     *
# *   along with this program; if not, write to the                         *
# *   Free Software Foundation, Inc.,                                       *
# *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
# ***************************************************************************


#ver.0.2.13

import os, sys, popen2
from PyQt4 import QtCore, QtGui
from StringIO import StringIO
from datetime import datetime

pwd=os.popen('pwd').read()
run='kdesu'+' '+pwd.strip()+"/"+"makchanger.py"

if not os.geteuid()==0:
	os.popen(run)
	sys.exit()


def get(): #save curent state to temp file 
 
 default=open('config.tmp', 'w') 
 output = os.popen('ifconfig -a|grep HWaddr').read()
 a=str(output)
 default.write(a)
 default.close()

get()

def prepare():
	os.popen("rm config.mak")
	os.popen("rm mac.log")
	def1=open('config.tmp', 'r+') 
	out = open('config.mak', 'w')
	for line in def1: #delete whitespaces loop
		print >> out,line.strip().strip()
	def1.close()
	os.popen ('rm config.tmp')
	out.close()
	now=datetime.now()
	f=open("mac.log",'w')
	f.writelines("*******************************\n")
	f.writelines("Mac changer started at:\n")
	f.writelines(str(now))
	f.writelines("\n")
	f.writelines("*******************************\n")
	
	f.flush()
	f.close()

prepare()

# UI initialize
app = QtGui.QApplication(sys.argv)

MainWindow = QtGui.QMainWindow()
MainWidget=QtGui.QWidget(MainWindow)

MainWindow.setGeometry(338,252,564,458)
#MainWindow.setMaximumHeight(658)

MainWindow.setCentralWidget(MainWidget)
MainWindow.setWindowTitle("MaK changer")
layout=QtGui.QGridLayout(MainWidget)

macLabel=QtGui.QLabel("<h1>MaK changer</h1>",MainWidget)
macLabel.setAlignment(QtCore.Qt.AlignLeft)
saveLabel=QtGui.QLabel("<b>Set<b>",MainWidget)
layout.addWidget(macLabel,0,0,1,2)
layout.addWidget(saveLabel,1,2,1,2)




default1=open('config.mak','r')
c=0
name=[]
adr=[]
for line in default1: #filling names an mac
	
	c=c+1
	a=line
	aname=a[0:5]
	madr=a[-18:]
	name.append(aname)
	adr.append(madr)

#print name
#print adr
	
#Very long UI

if c==1: 
	Label1=QtGui.QLabel(name[0], MainWidget)
	layout.addWidget (Label1,2,0,QtCore.Qt.AlignRight)
	CBox1=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox1,2,2)
	Mac1=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac1,2,1)
	Mac1.setText(adr[0])
	
if c==2:
	Label1=QtGui.QLabel(name[0], MainWidget)
	layout.addWidget (Label1,2,0,QtCore.Qt.AlignRight)
	CBox1=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox1,2,2)
	Mac1=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac1,2,1)
	Mac1.setText(adr[0])
	
	
	Label2=QtGui.QLabel(name[1], MainWidget)
	layout.addWidget (Label2,3,0,QtCore.Qt.AlignRight)
	CBox2=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox2,3,2)
	Mac2=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac2,3,1)
	Mac2.setText(adr[1])

if c==3:

	Label1=QtGui.QLabel(name[0], MainWidget)
	layout.addWidget (Label1,2,0,QtCore.Qt.AlignRight)
	CBox1=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox1,2,2)
	Mac1=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac1,2,1)
	Mac1.setText(adr[0])
	
	Label2=QtGui.QLabel(name[1], MainWidget)
	layout.addWidget (Label2,3,0,QtCore.Qt.AlignRight)
	CBox2=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox2,3,2)
	Mac2=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac2,3,1)
	Mac2.setText(adr[1])
	
	Label3=QtGui.QLabel(name[2], MainWidget)
	layout.addWidget (Label3,4,0,QtCore.Qt.AlignRight)
	CBox3=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox3,4,2)
	Mac3=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac3,4,1)
	Mac3.setText(adr[2])

if c==4:
	
	Label1=QtGui.QLabel(name[0], MainWidget)
	layout.addWidget (Label1,2,0,QtCore.Qt.AlignRight)
	CBox1=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox1,2,2)
	Mac1=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac1,2,1)
	Mac1.setText(adr[0])
	
	Label2=QtGui.QLabel(name[1], MainWidget)
	layout.addWidget (Label2,3,0,QtCore.Qt.AlignRight)
	CBox2=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox2,3,2)
	Mac2=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac2,3,1)
	Mac2.setText(adr[1])
	
	Label3=QtGui.QLabel(name[2], MainWidget)
	layout.addWidget (Label3,4,0,QtCore.Qt.AlignRight)
	CBox3=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox3,4,2)
	Mac3=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac3,4,1)
	Mac3.setText(adr[2])
	
	Label4=QtGui.QLabel(name[3], MainWidget)
	layout.addWidget (Label4,5,0,QtCore.Qt.AlignRight)
	CBox4=QtGui.QCheckBox(MainWidget)
	Mac4=QtGui.QLineEdit(MainWidget)
	layout.addWidget (CBox4,5,2)
	layout.addWidget (Mac4,5,1)
	Mac4.setText(adr[3])

if c==5:
	
	Label1=QtGui.QLabel(name[0], MainWidget)
	layout.addWidget (Label1,2,0,QtCore.Qt.AlignRight)
	CBox1=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox1,2,2)
	Mac1=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac1,2,1)
	Mac1.setText(adr[0])
	
	Label2=QtGui.QLabel(name[1], MainWidget)
	layout.addWidget (Label2,3,0,QtCore.Qt.AlignRight)
	CBox2=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox2,3,2)
	Mac2=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac2,3,1)
	Mac2.setText(adr[1])
	
	Label3=QtGui.QLabel(name[2], MainWidget)
	layout.addWidget (Label3,4,0,QtCore.Qt.AlignRight)
	CBox3=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox3,4,2)
	Mac3=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac3,4,1)
	Mac3.setText(adr[2])
	
	Label4=QtGui.QLabel(name[3], MainWidget)
	layout.addWidget (Label4,5,0,QtCore.Qt.AlignRight)
	CBox4=QtGui.QCheckBox(MainWidget)
	Mac4=QtGui.QLineEdit(MainWidget)
	layout.addWidget (CBox4,5,2)
	layout.addWidget (Mac4,5,1)
	Mac4.setText(adr[3])
	
	Label5=QtGui.QLabel(name[4], MainWidget)
	layout.addWidget (Label5,6,0,QtCore.Qt.AlignRight)
	CBox5=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox5,6,2)
	Mac5=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac5,6,1)
	Mac5.setText(adr[4])

if c==6:
	
	Label1=QtGui.QLabel(name[0], MainWidget)
	layout.addWidget (Label1,2,0,QtCore.Qt.AlignRight)
	CBox1=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox1,2,2)
	Mac1=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac1,2,1)
	Mac1.setText(adr[0])
	
	Label2=QtGui.QLabel(name[1], MainWidget)
	layout.addWidget (Label2,3,0,QtCore.Qt.AlignRight)
	CBox2=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox2,3,2)
	Mac2=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac2,3,1)
	Mac2.setText(adr[1])
	
	Label3=QtGui.QLabel(name[2], MainWidget)
	layout.addWidget (Label3,4,0,QtCore.Qt.AlignRight)
	CBox3=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox3,4,2)
	Mac3=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac3,4,1)
	Mac3.setText(adr[2])
	
	Label4=QtGui.QLabel(name[3], MainWidget)
	layout.addWidget (Label4,5,0,QtCore.Qt.AlignRight)
	CBox4=QtGui.QCheckBox(MainWidget)
	Mac4=QtGui.QLineEdit(MainWidget)
	layout.addWidget (CBox4,5,2)
	layout.addWidget (Mac4,5,1)
	Mac4.setText(adr[3])
	
	Label5=QtGui.QLabel(name[4], MainWidget)
	layout.addWidget (Label5,6,0,QtCore.Qt.AlignRight)
	CBox5=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox5,6,2)
	Mac5=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac5,6,1)
	Mac5.setText(adr[4])
	
	Label6=QtGui.QLabel(name[5], MainWidget)
	layout.addWidget (Label6,7,0,QtCore.Qt.AlignRight)
	CBox6=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox6,7,2)
	Mac6=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac6,7,1)
	Mac6.setText(adr[5])

if c==7:
	
	Label1=QtGui.QLabel(name[0], MainWidget)
	layout.addWidget (Label1,2,0,QtCore.Qt.AlignRight)
	CBox1=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox1,2,2)
	Mac1=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac1,2,1)
	Mac1.setText(adr[0])
	
	Label2=QtGui.QLabel(name[1], MainWidget)
	layout.addWidget (Label2,3,0,QtCore.Qt.AlignRight)
	CBox2=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox2,3,2)
	Mac2=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac2,3,1)
	Mac2.setText(adr[1])
	
	Label3=QtGui.QLabel(name[2], MainWidget)
	layout.addWidget (Label3,4,0,QtCore.Qt.AlignRight)
	CBox3=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox3,4,2)
	Mac3=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac3,4,1)
	Mac3.setText(adr[2])
	
	Label4=QtGui.QLabel(name[3], MainWidget)
	layout.addWidget (Label4,5,0,QtCore.Qt.AlignRight)
	CBox4=QtGui.QCheckBox(MainWidget)
	Mac4=QtGui.QLineEdit(MainWidget)
	layout.addWidget (CBox4,5,2)
	layout.addWidget (Mac4,5,1)
	Mac4.setText(adr[3])
	
	Label5=QtGui.QLabel(name[4], MainWidget)
	layout.addWidget (Label5,6,0,QtCore.Qt.AlignRight)
	CBox5=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox5,6,2)
	Mac5=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac5,6,1)
	Mac5.setText(adr[4])
	
	Label6=QtGui.QLabel(name[5], MainWidget)
	layout.addWidget (Label6,7,0,QtCore.Qt.AlignRight)
	CBox6=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox6,7,2)
	Mac6=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac6,7,1)
	Mac6.setText(adr[5])
	
	Label7=QtGui.QLabel(name[6], MainWidget)
	layout.addWidget (Label7,8,0,QtCore.Qt.AlignRight)
	CBox7=QtGui.QCheckBox(MainWidget)
	layout.addWidget (CBox7,8,2)
	Mac7=QtGui.QLineEdit(MainWidget)
	layout.addWidget (Mac7,8,1)
	Mac7.setText(adr[6])
	
#print c
verLabel=QtGui.QLabel("ver 0.2.13", MainWidget)
layout.addWidget (verLabel,c+6,2,QtCore.Qt.AlignLeft)

logs=[]
def log(): #log function
 logEdit=QtGui.QTextEdit(MainWidget)
 logEdit.setReadOnly(True)
 f1=open('mac.log','r') #save old
 for line in f1:
 	logs.append(line)
 f1.flush
 f1.close
 f2=open('mac.log','w') # write new+old
 f2.writelines(logs)
 f2.flush()
 f2.close()
 f3=open("mac.log") #show 
 text=f3.read()
 logEdit.setPlainText(text)
 f3.flush()
 f3.close()
 layout.addWidget(logEdit,c+5,0,1,3)
log()



def do():
	log1=open('mac.log','w')
	
	now=datetime.now()
	log1.writelines("---------------\n")
	log1.writelines("Executed on:\n")
	log1.writelines(str(now))
	log1.writelines("\n")
	log1.writelines("---------------\n")
	#log1.writelines("\n")
	if c>0:
		if CBox1.isChecked():
			q1="macchanger"+" "+name[0]+" "+"-m"+" "+unicode(Mac1.text())	
			log1.writelines(q1)
			
			#log1.writelines("\n")
			command=popen2.Popen4(q1)
			outfile=command.fromchild
			log1.writelines(outfile.read())
			log1.writelines("\n")
			#if bot==1:
			#	log1.writelines("device added to boot script\n")
			#	kubuntu(name[0],Mac1.text())
		if c==1:
			log1.flush()
			log1.close()
			log()
			return;
	
	if c>1:
		if CBox2.isChecked():
			q2="macchanger"+" "+name[1]+" "+"-m"+" "+unicode(Mac2.text())
			log1.writelines(q2)
			log1.writelines("\n")
			command=popen2.Popen4(q2)
			outfile=command.fromchild
			log1.writelines(outfile.read())
			log1.writelines("\n")
			
		if c==2:
			log1.flush()
			log1.close()
			log()
			return
	if c>2:
		if CBox3.isChecked():
			q3="macchanger"+" "+name[2]+" "+"-m"+" "+unicode(Mac3.text())
			log1.writelines(q3)
			log1.writelines("\n")
			command=popen2.Popen4(q3)
			outfile=command.fromchild
			log1.writelines(outfile.read())
			log1.writelines("\n")
		if c==3:
			log1.flush()
			log1.close()
			log()
			return
	if c>3:
		if CBox4.isChecked():
			q4="macchanger"+" "+name[3]+" "+"-m"+" "+unicode(Mac4.text())
			log1.writelines(q4)
			log1.writelines("\n")
			command=popen2.Popen4(q4)
			outfile=command.fromchild
			log1.writelines(outfile.read())
			log1.writelines("\n")
			#if bot==1:
			#	kubuntu(name[3],Mac4.text())
		if c==4:
			log1.flush()
			log1.close()
			log()
			return
		
	if c>4:
		if CBox5.isChecked():
			q5="macchanger"+" "+name[4]+" "+"-m"+" "+unicode(Mac5.text())
			log1.writelines(q5)
			log1.writelines("\n")
			command=popen2.Popen4(q5)
			outfile=command.fromchild
			log1.writelines(outfile.read())
			log1.writelines("\n")
			#if bot==1:
			#	kubuntu(name[4],Mac5.text())
		if c==5:
			log1.flush()
			log1.close()
			log()
			return
	if c>5:	
		if CBox6.isChecked():
			q6="macchanger"+" "+name[5]+" "+"-m"+" "+unicode(Mac6.text())
			log1.writelines(q6)
			log1.writelines("\n")
			command=popen2.Popen4(q6)
			outfile=command.fromchild
			log1.writelines(outfile.read())
			log1.writelines("\n")
			#if bot==1:
			#	kubuntu(name[5],Mac6.text())
		if c==6:
			log1.flush()
			log1.close()
			log()
			return
	if c>6:
		if CBox7.isChecked():
			q7="macchanger"+" "+name[6]+" "+"-m"+" "+unicode(Mac7.text())
			log1.writelines(q7)
			log1.writelines("\n")
			command=popen2.Popen4(q7)
			outfile=command.fromchild
			log1.writelines(outfile.read())
			log1.writelines("\n")
			#if bot==1:
			#	kubuntu(name[6],Mac7.text())
		if c==7:
			log1.flush()
			log1.close()
			log()
			return

def exit():
	os.popen("rm config.mak")
	os.popen("rm mac.log")
	MainWindow.close()


#def clog():
#	f=open('mac.log','w')
#	f.clear()

PushButton = QtGui.QPushButton("Do it!",MainWidget)
PushButton1 = QtGui.QPushButton("exit",MainWidget)
#PushButton2 = QtGui.QPushButton("Clear log",MainWidget)


layout.addWidget (PushButton,c+4,0,QtCore.Qt.AlignTop)
layout.addWidget (PushButton1,c+4,2,QtCore.Qt.AlignTop)
#layout.addWidget (PushButton2,c+3,1,QtCore.Qt.AlignTop)

app.connect(PushButton,QtCore.SIGNAL("clicked()"),do)
app.connect(PushButton1,QtCore.SIGNAL("clicked()"),exit)
#app.connect(PushButton2,QtCore.SIGNAL("clicked()"),log)


MainWindow.show()
app.exec_()