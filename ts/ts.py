#!/usr/bin/env python3
"""
Time series builder.
"""
import os
import time
import datetime
from multiprocessing import Process

import schedule
import pandas as pd

from util import logger
from util import rock


rt_keys = [
	"binance.spot",
	"coinbase.spot",
	"kraken.spot",
	"apmex.spot",
	"gold.spot",
	"spot",
	"spot.usd"
]


def ts_minutely():
	logger.info("ts_minutely.started")
	now = datetime.datetime.now().replace(second=0, microsecond=0)
	rtdb = rock.Rock("rtdb")
	for key in rt_keys:
		try:
			val = rtdb.get(key)
			fkey = key.replace(".", "_")
			fname = f"/data/tsdb/{fkey}_minutely.parq"
			if os.path.exists(fname):
				df = pd.read_parquet(fname)
				nvals = len(df)
				nowpie = {"date": now, "spot": val}
				df = df.append(nowpie, ignore_index=True)
				df.drop_duplicates(subset=["date"], keep="first", inplace=True)
				if len(df) != nvals:
					df.to_parquet(fname)
			else:
				nowpie = {"date": [now], "spot": [val]}
				df = pd.DataFrame(nowpie)
				df.to_parquet(fname)
		except Exception as ex:
			logger.info("ts_minutely.exception")
			logger.exception(ex)
	logger.info("ts_minutely.finished")



def ts_daily():
	logger.info("ts_daily.started")
	now = datetime.datetime.now().date()
	rtdb = rock.Rock("rtdb")
	for key in rt_keys:
		try:
			val = rtdb.get(key)
			fkey = key.replace(".", "_")
			fname = f"/data/tsdb/{fkey}_daily.parq"
			if os.path.exists(fname):
				df = pd.read_parquet(fname)
				nvals = len(df)
				nowpie = {"date": now, "spot": val}
				df = df.append(nowpie, ignore_index=True)
				df.date = pd.to_datetime(df.date)
				df.drop_duplicates(subset=["date"], keep="first", inplace=True)
				if len(df) != nvals:
					df.to_parquet(fname)
			else:
				nowpie = {"date": [now], "spot": [val]}
				df = pd.DataFrame(nowpie)
				df.date = pd.to_datetime(df.date)
				df.to_parquet(fname)
		except Exception as ex:
			logger.info("ts_daily.exception")
			logger.exception(ex)
	logger.info("ts_daily.finished")



schedule.every(30).seconds.do(ts_minutely)
schedule.every(20*60).seconds.do(ts_daily)



if __name__ == "__main__":
	logger.info("ts started.")
	while True:
		schedule.run_pending()
		time.sleep(1)

