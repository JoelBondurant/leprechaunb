#!/usr/bin/env python3
"""
Time series builder.
"""

import datetime
import importlib
import os
import subprocess as sp
import time

import pandas as pd
import schedule

from util import logger
from util import racoon
from util import rock


def peek():
	"""
	Interactive debugging in prod...
	"""
	return rock.rocks("tsdbrocks", read_only=True).get("tsdb_data")


rtdb_keys = rock.rocks("rtdb", read_only=True).get("keys")


periods = ["minutely", "hourly", "daily"]
for period in periods:
	path = f"/data/tsdb/{period}"
	if not os.path.exists(path):
		os.makedirs(path, mode=0o770, exist_ok=True)


def ts_rt():
	"""
	Pump rt data down the pipeline.
	"""
	logger.info("<ts_rt>")
	global rtdb_keys
	tsdb_data = {}
	for key in rtdb_keys:
		tsdb_data[key] = rock.rocks("rtdb", read_only=True).get(key)
	tsdb_data["tsdb_timestamp"] = int(time.time())
	rock.rocks("tsdbrocks").put("tsdb_data", tsdb_data)
	logger.info("</ts_rt>")


def ts_minutely():
	logger.info("<ts_minutely>")
	now = datetime.datetime.now().replace(second=0, microsecond=0)
	for key in rtdb_keys:
		try:
			val = rock.rocks("rtdb", read_only=True).get(key)
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
				df = df.dropna()
				df.drop_duplicates(subset=["date"], keep="last", inplace=True)
				if len(df) != nvals:
					racoon.to_parquet(df, fname)
			else:
				logger.info("Create: " + fname)
				if type(val) == dict:
					nowpie = {k:[v] for k,v in val.items()}
					nowpie["date"] = [now]
				else:
					nowpie = {"date": [now], "value": [val]}
				df = pd.DataFrame(nowpie)
				racoon.to_parquet(df, fname)
		except Exception as ex:
			logger.info(f"ts_minutely.exception.{key}")
			logger.exception(ex)
	logger.info("</ts_minutely>")


def ts_hourly():
	logger.info("<ts_hourly>")
	now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
	for key in rtdb_keys:
		try:
			val = rock.rocks("rtdb", read_only=True).get(key)
			fname = f"/data/tsdb/hourly/{key}.parq"
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
				df = df.dropna()
				df.drop_duplicates(subset=["date"], keep="first", inplace=True)
				if len(df) != nvals:
					racoon.to_parquet(df, fname)
			else:
				logger.info("Create: " + fname)
				if type(val) == dict:
					nowpie = {k:[v] for k,v in val.items()}
					nowpie["date"] = [now]
				else:
					nowpie = {"date": [now], "value": [val]}
				df = pd.DataFrame(nowpie)
				df.date = pd.to_datetime(df.date)
				racoon.to_parquet(df, fname)
		except Exception as ex:
			logger.info(f"ts_hourly.exception.{key}")
			logger.exception(ex)
	logger.info("</ts_hourly>")


def ts_daily():
	logger.info("<ts_daily>")
	now = datetime.datetime.now().date()
	for key in rtdb_keys:
		try:
			val = rock.rocks("rtdb", read_only=True).get(key)
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
				df = df.dropna()
				df.drop_duplicates(subset=["date"], keep="first", inplace=True)
				if len(df) != nvals:
					racoon.to_parquet(df, fname)
			else:
				logger.info("Create: " + fname)
				if type(val) == dict:
					nowpie = {k:[v] for k,v in val.items()}
					nowpie["date"] = [now]
				else:
					nowpie = {"date": [now], "value": [val]}
				df = pd.DataFrame(nowpie)
				df.date = pd.to_datetime(df.date)
				racoon.to_parquet(df, fname)
		except Exception as ex:
			logger.info(f"ts_daily.exception.{key}")
			logger.exception(ex)
	logger.info("</ts_daily>")



def main():
	"""
	Main ts entry point.
	"""
	logger.warn("ts started.")

	time.sleep(1)
	ts_rt()
	ts_minutely()
	ts_hourly()
	ts_daily()

	while True:
		try:
			# schedule crash guard:
			importlib.reload(schedule)
			schedule.every(11).seconds.do(ts_rt)
			schedule.every(21).seconds.do(ts_minutely)
			schedule.every(701).seconds.do(ts_hourly)
			schedule.every(1701).seconds.do(ts_daily)
			while True:
				try:
					time.sleep(2)
					schedule.run_pending()
				except Exception as ex:
					logger.exception(ex)
					time.sleep(2)
		except Exception as ex:
			logger.exception(ex)
			time.sleep(2)


if __name__ == "__main__":
	main()

