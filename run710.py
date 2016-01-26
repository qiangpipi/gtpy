#!/usr/bin/python
import sys
import os
sys.path.append(os.getcwd())
sys.path.append(os.getcwd() + "/" + "lib/")
import random
import time
import string
import json
import httplib, urllib
import conf
import lib710
import queryDraw
import queryPool
import queryPrize
import bet

'''
710 Module
'''

# -*- coding: utf-8 -*-

def execTc(tc):
  f = open(os.getcwd() + "/" + "testdata/" + tc)
  tcd = f.read().strip("\n")
  ds = json.loads(tcd)
  for d in ds:
    url = d["url"]
    if url == "/incubator/bc/bet/pool.do":
####-----Query bet pool-------
      res = queryPool.run(d, url)
      queryPool.checkRes(d, res)
    elif url == "/incubator/bc/bet/bet.do":
####-----Bet------------------
      res = bet.run(d, url)
      bet.checkRes(d, res)
    elif url == "/incubator/bc/bet/saleDraw.do":
####-----Query Draw ID--------
      res = queryDraw.run(d, url)
      queryDraw.checkRes(d, res)
    elif url == "/incubator/bc/bet/prizeLevel.do":
####-----Query Prize Level----
      res = queryPrize.run(d, url)
      queryPrize.checkRes(d, res)
