#!/usr/bin/python
import sys
import os
sys.path.append(os.getcwd() +"/..")
import lib710
import json
import conf

def run(d, url):
  params = "?req=" + lib710.createP(d)
  r = lib710.httpReq(conf.gameServerIp, conf.gameServerPort,url,params)
  rj = json.loads(r)
  return rj

def checkRes(d, res):
  result = "fail"
  if d["code"]==res["code"]:
    result = "pass"
  if d["code"] == "000":
    pass
  lib710.logResult(d, result)
