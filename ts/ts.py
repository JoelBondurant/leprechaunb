#!/usr/bin/env python3
"""
Time series builder.
"""

import os
import json
import time
import datetime

import pandas as pd

from util import logger
from util import rock


# The period of the ts phase, time series writes must complete within the ts PERIOD:
PERIOD = 20


def rtdb():
	"""
	Get a connection to rtdb.
	"""
	db = rock.Rock("rtdb")
	return db


def tsdbrocks():
	"""
	Get a connection to tsdbrocks.
	"""
	db = rock.Rock("tsdbrocks")
	return db


rtdb_keys = rtdb().get("keys")


with open("/data/tsdb/rtdb_keys.json", "w") as fout:
	json.dump(rtdb_keys, fout)


periods = ["minutely", "daily"]
for period in periods:
	path = f"/data/tsdb/{period}"
	if not os.path.exists(path):
		os.makedirs(path)


def ts_rt():
	"""
	Pump rt data down the pipeline.
	"""
	logger.info("<ts_rt>")
	global rtdb_keys
	rtdb_data = {}
	for key in rtdb_keys:
		rtdb_data[key] = rtdb().get(key)
	rtdb_data["timestamp"] = int(time.time())
	tsdbrocks().put("rtdb_data", rtdb_data)
	logger.info("</ts_rt>")


def ts_minutely():
	logger.info("<ts_minutely>")
	now = datetime.datetime.now().replace(second=0, microsecond=0)
	for key in rtdb_keys:
		try:
			val = rtdb().get(key)
			fname = f"/data/tsdb/minutely/{key}.parq"
			if os.path.exists(fname):
				logger.info("Append to: " + fname)
				df = pd.read_parquet(fname)
				nvals = len(df)
				if type(val) == dict:
					nowpie = val
					nowpie["date"] = now
				else:
					nowpie = {"date": now, "value": val}
				df = df.append(nowpie, ignore_index=True)
				df.drop_duplicates(subset=["date"], keep="last", inplace=True)
				if len(df) != nvals:
					df.to_parquet(fname)
			else:
				logger.info("Create: " + fname)
				if type(val) == dict:
					nowpie = {k:[v] for k,v in val.items()}
					nowpie["date"] = [now]
				else:
					nowpie = {"date": [now], "value": [val]}
				df = pd.DataFrame(nowpie)
				df.to_parquet(fname)
		except Exception as ex:
			logger.info("ts_minutely.exception")
			logger.exception(ex)
	logger.info("</ts_minutely>")



def ts_daily():
	logger.info("<ts_daily>")
	now = datetime.datetime.now().date()
	for key in rtdb_keys:
		try:
			val = rtdb().get(key)
			fname = f"/data/tsdb/daily/{key}.parq"
			if os.path.exists(fname):
				df = pd.read_parquet(fname)
				nvals = len(df)
				if type(val) == dict:
					nowpie = val
					nowpie["date"] = now
				else:
					nowpie = {"date": now, "value": val}
				df = df.append(nowpie, ignore_index=True)
				df.date = pd.to_datetime(df.date)
				df.drop_duplicates(subset=["date"], keep="first", inplace=True)
				if len(df) != nvals:
					df.to_parquet(fname)
			else:
				logger.info("Create: " + fname)
				if type(val) == dict:
					nowpie = {k:[v] for k,v in val.items()}
					nowpie["date"] = [now]
				else:
					nowpie = {"date": [now], "value": [val]}
				df = pd.DataFrame(nowpie)
				df.date = pd.to_datetime(df.date)
				df.to_parquet(fname)
		except Exception as ex:
			logger.info("ts_daily.exception")
			logger.exception(ex)
	logger.info("</ts_daily>")



def main():
	"""
	Main ts entry point.
	"""
	logger.info("ts started.")
	import schedule
	schedule.every(10).seconds(ts_rt)
	schedule.every(20).seconds(ts_minutely)
	schedule.every(600).seconds(ts_daily)
	t0 = time.time()
	while True:
		time.sleep(1)
		schedule.run_pending()
		if time.time() - t0 > 120:
			t0 = time.time()
			logger.info("heartbeat")


if __name__ == "__main__":
	main()

