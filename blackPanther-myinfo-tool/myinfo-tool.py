#!/usr/bin/env python

import os, sys

from progress import *

program_name = os.path.basename(sys.argv[0])
#if os.path.basename(sys.argv[1]):
#    option_name = os.path.basename(sys.argv[1])

sys.path.append('/usr/share/myinfo-tool')

if len(sys.argv) == 2:
    if sys.argv[1] == 'mac':
	run='kdesu'+" myinfo-tool mac"
	print run
	if not os.geteuid()==0:
	    os.popen(run)
	    sys.exit()
	os.popen('python /usr/share/myinfo-tool/makchanger.py ')
    elif sys.argv[1] == 'addhw':
	run='kdesu'+" myinfo-tool addhw"
	if not os.geteuid()==0:
	    os.popen(run)
    	    sys.exit()
	os.popen('default-terminal -e \"/usr/sbin/dkms_autoinstaller start && /usr/share/harddrake/service_harddrake && sleep 3\"')

elif program_name == 'myinfo-tool':
    os.popen('python /usr/share/myinfo-tool/progress.py &')
    os.system('cd /usr/share/myinfo-tool/ ; ./core.py')
#elif len(sys.argv) == 2:
#    if sys.argv[1] == 'mac':
#        os.popen('cd /usr/share/myinfo-tool && python ./makchanger.py ')
    
 