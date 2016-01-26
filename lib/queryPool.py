#!/usr/bin/python
import sys
import os
sys.path.append(os.getcwd() +"/..")
import lib710
import json
import conf

def run(d, url):
	params = "?req=" + lib710.createP(d)
##	print params
	r = lib710.httpReq(conf.gameServerIp, conf.gameServerPort,url,params)
	rj = json.loads(r)
	return rj

def checkRes(d, res):
	result = "fail"
##	print res
	if d["code"]==res["code"]:
		if d["code"] == "000":
			if d["gameId"] == "10001" or d["gameId"] == "10003":
				if res["poolId"]==1001 and round(res["poolAmount"],3)==round(lib710.queryPoolAmount(res["poolId"]),3):
					result = "pass"
				else:
					print res["poolAmount"], lib710.queryPoolAmount(res["poolId"])
			elif d["gameId"] == "10002":
				if res["poolId"]==1002 and round(res["poolAmount"],3)==round(lib710.queryPoolAmount(res["poolId"]),3):
					result = "pass"
				else:
					print res["poolAmount"], lib710.queryPoolAmount(res["poolId"])
		else:
			result = "pass"
	lib710.logResult(d, result)
