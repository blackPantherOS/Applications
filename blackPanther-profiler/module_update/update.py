#!/usr/bin/env python

import os, sys, time,  urllib2, subprocess

# kikapcsolva gtk fuggoseg miatt
import pynotify

icon = "profiler.png"
warn = "warning.png"
updateStat = False

def downloadUpdate(self):
            print "Try download update file here: ",url
            #time.sleep(5)
	    try:
		#os.system('gurpmi2 '+ url)
		f = urllib2.urlopen(url)
		with open('profiler-cfgdata-update.rpm', "wb") as local_file:
			local_file.write(f.read())

		#os.system("gurpmi2 profiler-cfgdata-update.rpm")
		#os.system("unzip -q profiler-updates.zip -d Updates")
		#os.system("mkdir -p"+os.path.dirname("~/config/profiler"))
		#os.system("cp -af Updates/*" "~/config/profiler/")
		#os.system("rm Updates -r -f")
		#os.system("rm update.zip")
		print "New version downloaded!"
		#finishUpdate(id)
    	    except:
    		#time.sleep(5)
    		print "Update Failed: URL or Archive Not Available!"
		pynotify.init("Profiler Update")
		n = pynotify.Notification("Update Failed","An unknown error occured while downloading!",warn)
		n.show()
    		print "Failed"
    		sys.exit()

def finishUpdate(self):
    	    print "Version checking.."
    	    ver = os.popen("rpmquery firefox --queryformat='%{version}.%{release}'").read().replace("bP","")
    	    #ver = os.popen("rpmquery blackPanther-profiler-cfgdata --queryformat='%{version}.%{release}'").read().replace("bP","")
            print ver,"rpmversion, last:",id

	    if id == ver:
		print "Last profiler data installed!"
		lines = []
		with open("modules_update/update.cfg",'r') as data:
			for l in data.read().split("\n"):
				lines.append(l)
		with open("modules_update/update.cfg",'w') as data:
			for l in lines:
				if l.startswith("UPDATEID="):
					data.write("UPDATEID="+str(id)+"\n")
				else:
					if l != '\n':
						data.write(l+"\n")
	    #else:
		#print "..."
    		#downloadUpdate(self)

def notifUpdate(self):
		print "Recommend Apps Update found!"
		pynotify.init("Profiler Update")
		n = pynotify.Notification(title,text,icon)
		n.show()
		#downloadUpdate(f)
		finishUpdate(id)

try:
	#f = urllib2.urlopen("http://www.blackpantheros.eu/backend/profiler/updatemsg.txt", 'r')
	f = open("updatemsg.txt",'r')

	id,title,text,url = f.read().split("|")
	#with open("modules_update/update.cfg",'r') as data:
	with open("update.cfg",'r') as data:
		for l in data.read().split("\n"):
			if l.startswith("UPDATEID="):
				lastId = l.replace("\n",'').replace("UPDATEID=",'')

	#print id, "-", lastId, url
	if id > lastId:
	#if int(id) > int(lastId):
	    print "New Update Found!" 
	    updateStat = True
	    notifUpdate(f)
	    #downloadUpdate(f)
	    print id,'|',url
	else:
	    updateStat = False
	    #print "Update Not Found!"
	    print "Failed"
	    pynotify.init("Profiler Update")
	    n = pynotify.Notification(title,"Your list is upto date!",icon)
	    n.show()

except:
      print "Failed"
