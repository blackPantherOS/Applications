#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, glob

for filename in glob.glob1("gui", "*.ui"):
    print filename
    os.system("/usr/bin/pykdeuic4 -o gui/%s.py gui/%s" % (filename.split(".")[0], filename))

for filename in glob.glob1("gui", "*.qrc"):
    print filename
    os.system("/usr/bin/pyrcc4 gui/%s -o gui/%s_rc.py" % (filename, filename.split(".")[0]))
