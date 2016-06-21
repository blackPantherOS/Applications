#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import ConfigParser

short_groupnames = {}

with open('groups.txt', 'r') as groupfile:
  while True:
    line = groupfile.readline()[:-1]
    if line == "":
      break
    old, new = line.split(" @ ")
    short_groupnames[old] = new
  groupfile.close()

def group_convert(group):
  try:
    return short_groupnames[group]
  except:
    return group

applist_file = "applist.txt"

config = ConfigParser.RawConfigParser()

file = open(applist_file, "r")
while True:
  app = file.readline()[:-1]
  if app == "":
    break
  fav = False
  if app[0] == '*':
    app = app[2:]
    fav = True
  rpmq = os.popen("rpmquery " +app+ " --queryformat='%{summary}\t\n%{description}\t\n%{size}\t\n%{installtime:date}\t\n%{group}'").read().split("\t\n")
  if rpmq[0].find("not installed") == -1:
    config.add_section(app)
    config.set(app, "summary", rpmq[0][:40])
    config.set(app, "desc", rpmq[1][:300])
    config.set(app, "size", rpmq[2])
    config.set(app, "installtime", rpmq[3])
    config.set(app, "group", group_convert(rpmq[4]))
    config.set(app, "favorite", fav)
  else:
    print "Missing: "+app

file.close()

with open('example.cfg', 'wb') as configfile:
    config.write(configfile)
