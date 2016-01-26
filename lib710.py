#!/usr/bin/python
import sys
import os
sys.path.append(os.getcwd())
import random
import time
import string
import json
import httplib, urllib
import cx_Oracle
import conf
'''
710 Module
'''

# -*- coding: utf-8 -*-


def httpReq(ip, port, url, params):
  res = ""
  headers = {}
  url = url + params
  headers["charset"] = "utf-8"
##  print url
  try:
    con = httplib.HTTPConnection(ip, port, timeout = 30)
    con.request("POST", url, None, headers)
    resp = con.getresponse()
    res = urllib.unquote(resp.read())
  except Exception, e:
    print e
  finally:
    if con:
      con.close()
  return res

def createP(dJson):
  tp = {}
  ps = ""
  for k in dJson.keys():
    if k!="url":
      tp[k] = dJson[k]
    ps = json.dumps(tp)
  ps = ps.replace(" ","")
  return ps

def queryPoolAmount(poolId):
	a = 0.0
	con = cx_Oracle.connect(conf.db)
	cur = con.cursor()
	cur.execute("""
				SELECT * FROM (WITH INPUT AS (
        SELECT POOL_ID, SUM(AMOUNT) AS AMOUNT
				FROM T_GAME_POOL_DETAIL WHERE FUND_TYPE = 0 GROUP BY POOL_ID),
        OUTPUT AS (
        SELECT POOL_ID, SUM(AMOUNT) AS AMOUNT
		    FROM T_GAME_POOL_DETAIL WHERE FUND_TYPE = 1 GROUP BY POOL_ID)
        SELECT C.POOL_ID, 0 + NVL(A.AMOUNT,0) - NVL(B.AMOUNT,0) AS AMOUNT
        FROM INPUT A FULL JOIN OUTPUT B ON A.POOL_ID = B.POOL_ID
        FULL JOIN T_GAME_POOL C ON A.POOL_ID = C.POOL_ID)
				WHERE POOL_ID = :arg""",
				arg = poolId)
	for x,y in cur:
		a = y
	con.close()
	return a

def queryByPrizeLevelId(pId):
	prizeReferAmount = 0.0
	prizeAmount = 0.0
	con = cx_Oracle.connect(conf.db)
	cur = con.cursor()
	cur.execute("""
			SELECT PRIZE_REFER_AMOUNT, PRIZE_AMOUNT
			FROM T_GAME_PRIZE_LEVEL t WHERE t.PRIZE_LEVEL_ID = :arg""",
			arg = pId)
	for x,y in cur:
		prizeReferAmount = x
		prizeAmount = y
	return prizeReferAmount, prizeAmount

def logResult(tc,res):
	if len(tc["caseId"]):
	  print tc["caseId"], res
##  rId = "0"
##  cId = 469
##  ver = 4
##  h = {"Content-Type":"application/x-www-form-urlencoded"}
##  p = ("?m=testtask"
##			"&f=runCase"
##			"&runId=%s"
##			"&caseId=%s"
##			"&version=%s"
##      "&result=%s"
##      "&case=%s"
##      "&version=%s") % (rId, cId, ver, res, cId, ver)
##  url = conf.tlurl + p
##  print url
##  f = urllib.urlencode({"result":res,
##												"case":cId,
##												"version":ver})
##  try:
##    con = httplib.HTTPConnection(conf.tlip, conf.tlport, timeout = 30)
##    con.request("POST", url, None, headers=h)
##    resp = con.getresponse()
##    print resp.status
##    res = resp.read()
##    print res
##    con.close()
##  except Exception,e:
##    print e
##  finally:
##    con.close()
