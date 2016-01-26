#!/usr/bin/python
import sys
import os
sys.path.append(os.getcwd())
import string
import run710
import conf

'''
710 function test
'''

# -*- coding: utf-8 -*-

gameServerIp = "192.169.23.24"
gameServerPort = 8080
testList = "flist"

try:
  fl = open(os.getcwd() + "/" +testList)
  tc = fl.readline().strip("\n")
  while tc:
    run710.execTc(tc)
    tc = fl.readline().strip("\n")
  fl.close()
except Exception,e:
  print e
