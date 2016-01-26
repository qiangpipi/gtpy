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
  if rj["code"] == "000":
    if rj["drawStatus"] == 1:
      conf.drawStatus = 1
      conf.drawId = rj["drawId"]
    else:
      conf.drawStatus = 0
      conf.drawId = "00000"
  return rj

def checkRes(d, res):
	result = "fail"
	if d["code"]==res["code"]:
		if d["code"] == "000":
			if res["drawId"]!=None and res["drawStatus"] == 1:
				result = "pass"
		else:
			result = "pass"
	lib710.logResult(d, result)
