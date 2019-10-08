"""
Bitcoin price history.
"""
import datetime
import math
import os
import time

import numpy as np
import pandas as pd

from util import logger
from util import racoon
from util import rock
from util import stats


tsdb_keys = list(rock.rocks("tsdbrocks").get("tsdb_data").keys())

gold_spot_keys = [x for x in tsdb_keys if "_spot_btcxau" in x]
bitcoin_spot_keys = [x for x in tsdb_keys if "_spot_xaubtc" in x]
keys = tsdb_keys.copy()



def gold_minute_arrow():
	"""
	Maintain minutely spot aggregates for gold.
	"""
	global gold_spot_keys
	logger.info("<gold_spots_minutely>")
	gold_spot_keys = gold_spot_keys.copy()
	df = pd.read_parquet(f"/data/tsdb/minutely/{gold_spot_keys[0]}.parq")
	df["source"] = gold_spot_keys[0].split("_")[0]
	for spot_key in gold_spot_keys[1:]:
		df = pd.concat([df, pd.read_parquet(f"/data/tsdb/minutely/{spot_key}.parq")], ignore_index=True, sort=True)
		source = spot_key.split("_")[0]
		df.source = df.source.fillna(source)
	cutoff = datetime.datetime.utcnow().replace(second=0, microsecond=0)
	cutoff = cutoff - datetime.timedelta(hours=3*24)
	df = df[df.date >= cutoff]
	df = df.dropna()
	racoon.to_csv(df, "/data/adbcsv/spots_btcxau_minutely.csv")
	df = df.drop_duplicates(subset=["source"], keep="last")
	df = df.dropna()
	racoon.to_csv(df, "/data/adbcsv/spots_btcxau_minutely_tail.csv")
	logger.info("</gold_spots_minutely>")


def bitcoin_minute_arrow():
	"""
	Maintain minutely spot aggregates for bitcoin.
	"""
	global bitcoin_spot_keys
	logger.info("<bitcoin_spots_minutely>")
	bitcoin_spot_keys = bitcoin_spot_keys.copy()
	bitcoin_spot_keys = [x for x in bitcoin_spot_keys if "bisq" not in x]
	base_cutoff = datetime.datetime.utcnow().replace(second=0, microsecond=0)
	df = pd.read_parquet(f"/data/tsdb/minutely/{bitcoin_spot_keys[0]}.parq")
	df["source"] = bitcoin_spot_keys[0].split("_")[0]
	for spot_key in bitcoin_spot_keys[1:]:
		df = pd.concat([df, pd.read_parquet(f"/data/tsdb/minutely/{spot_key}.parq")], ignore_index=True, sort=True)
		source = spot_key.split("_")[0]
		df.source = df.source.fillna(source)
	cutoff = base_cutoff - datetime.timedelta(hours=3*24)
	df = df[df.date >= cutoff]
	for spot_key in bitcoin_spot_keys:
		df = pd.concat([df, pd.read_parquet(f"/data/tsdb/hourly/{spot_key}.parq")], ignore_index=True, sort=True)
		source = spot_key.split("_")[0]
		df.source = df.source.fillna(source)
	cutoff = base_cutoff - datetime.timedelta(hours=21*24)
	df = df[df.date >= cutoff]
	for spot_key in bitcoin_spot_keys:
		df = pd.concat([df, pd.read_parquet(f"/data/tsdb/daily/{spot_key}.parq")], ignore_index=True, sort=True)
		source = spot_key.split("_")[0]
		df.source = df.source.fillna(source)
	cutoff = base_cutoff - datetime.timedelta(hours=365*24)
	df = df[df.date >= cutoff]
	df = df.dropna()
	df = df.drop_duplicates(subset=["date", "source"], keep="last")
	df = df[df.source != "bisq"]
	df = df.sort_values("value", ascending=True, axis=0)
	racoon.to_csv(df, "/data/adbcsv/spots_xaubtc_minutely.csv")
	df = df.drop_duplicates(subset=["source"], keep="last")
	racoon.to_csv(df, "/data/adbcsv/spots_xaubtc_minutely_tail.csv")
	logger.info("</bitcoin_spots_minutely>")


def minute_arrow():
	"""
	Maintain minutely spot aggregates.
	"""
	logger.info("<spots_minutely>")
	gold_minute_arrow()
	bitcoin_minute_arrow()
	logger.info("</spots_minutely>")


def day_arrow():
	"""
	External day level wrapper.
	"""
	logger.info("<day_arrow>")
	for key in keys:
		if "timestamp" in key:
			continue
		fn = f"/data/tsdb/daily/{key}.parq"
		if os.path.exists(fn):
			df = pd.read_parquet(fn)
			racoon.to_csv(df, f"/data/adbcsv/{key}_daily.csv")
		else:
			logger.warn(f"/data/tsdb/daily/{key}.parq files are missing.")
	logger.info("</day_arrow>")


