#!/usr/bin/python
import sys
import os
sys.path.append(os.getcwd() +"/..")
import time
import random
import lib710
import json
import conf

def run(d, url):
	if d["gameId"] == 10002:
		d["drawId"] = conf.drawId
	d["serialNo"] = createSno()
	if d["gameId"] == 20004:
		d["oldSerialNo"] == createOldSno()
	params = "?req=" + lib710.createP(d)
	r = lib710.httpReq(conf.gameServerIp, conf.gameServerPort,url,params)
	rj = json.loads(r)
	return rj

def checkRes(d, res):
	result = "fail"
	if d["code"]==res["code"]:
		if d["code"] == "000":
			if d["gameId"] in ( 10001, 10002, 10003, 20004) and len(res["prizeLevel"]) ==1:
				if res["prizeLevel"][0]["prizeLevelId"] == 0 and \
						len(res["winTicket"]) == 0 and \
						res["prizeLevel"][0]["prizeAmount"] == 0:
					result = "pass"
				elif res["prizeLevel"][0]["prizeLevelId"] != 0 and \
						len(res["winTicket"]) !=0:
					result = checkAmount(d,res["prizeLevel"][0],res["winTicket"][0])
			elif d["gameId"] == 10002 and len(res["prizeLevel"]) > 1:
				result = "pass"
				if len(res["winTicket"]) == 0:
					for pLevel in res["prizeLevel"]:
						if pLevel["prizeLevelId"]!=0:
							result = "fail"
				else:
					for pLevel in res["prizeLevel"]:
						if pLevel["prizeLevelId"] == 0:
							if pLevel["prizeAmount"]!=0:
								result = "fail"
						else:
							for wTicket in res["winTicket"]:
								if pLevel["betNo"] == wTicket["betNo"]:
									result = checkAmount(d,pLevel,wTicket)
			elif d["gameId"] == 20004:
				pass
	lib710.logResult(d,result)

def checkAmount(d,prizeLevel, winTicket):
	res = "fail"
	prAmount, pAmount = lib710.queryByPrizeLevelId(prizeLevel["prizeLevelId"])
	if d["gameId"] == 10002:
		expAmount = (1.0/prAmount)*pAmount
	elif d["gameId"] == 20004:
		expAmount = d["betAmount"]*pAmount
	else:
		expAmount = (d["betAmount"]/prAmount)*pAmount
	if round(expAmount,3) == round(prizeLevel["prizeAmount"],3) and round(expAmount,3) == round(winTicket["prizeAmount"],3):
		res = "pass"
	elif prizeLevel["prizeLevelId"] in (15,31):
		res = "pass"
	else:
		print d["betAmount"],prAmount,pAmount,expAmount,prizeLevel["prizeAmount"],winTicket["prizeAmount"],res
	return res

def createSno():
	timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
	sno = timestamp + str(random.randint(1000,9999))
	return sno

def createOldSno():
	oldSno = "00000"
	return oldSno
