#!/usr/bin/env python3
"""
Time series builder.
"""

import os
import time
import datetime

import pandas as pd

from util import logger
from util import rock


# The period of the ts phase, time series writes must complete within the ts PERIOD:
PERIOD = 30


rtdb = rock.Rock("rtdb")
rtdb_keys = rtdb.get("keys")


periods = ["minutely", "daily"]
for period in periods:
	path = f"/data/tsdb/{period}"
	if not os.path.exists(path):
		os.makedirs(path)


def ts_minutely():
	logger.info("ts_minutely.started")
	now = datetime.datetime.now().replace(second=0, microsecond=0)
	for key in rtdb_keys:
		try:
			val = rtdb.get(key)
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
	logger.info("ts_minutely.finished")



def ts_daily():
	logger.info("ts_daily.started")
	now = datetime.datetime.now().date()
	for key in rtdb_keys:
		try:
			val = rtdb.get(key)
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
	logger.info("ts_daily.finished")



def main():
	"""
	Main ts entry point.
	"""
	started = int(time.time()) - 3600
	while True:
		try:
			elapsed = int(time.time())
			time.sleep(1)
			if int(time.time()) - started > 600:
				logger.info("heartbeat")
				ts_daily()
				started = int(time.time())
			ts_minutely()
			elapsed = int(time.time()) - elapsed
			time.sleep(max(0, PERIOD - elapsed))
		except Exception as ex:
			logger.exception(ex)


if __name__ == "__main__":
	main()

