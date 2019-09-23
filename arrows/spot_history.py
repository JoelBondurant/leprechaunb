"""
Bitcoin price history.
"""
import datetime
import math
import os
import json
import time

import pandas as pd

from util import logger


with open("/data/tsdb/rtdb_keys.json", "r") as fin:
	rtdb_keys = json.load(fin)


spot_keys = [x for x in rtdb_keys if "spot" in x]
keys = rtdb_keys.copy()


def keys_minutely():
	"""
	Maintain the minutely key files.
	"""
	logger.info("key_minutely.started.")
	for key in keys:
		df = pd.read_parquet(f"/data/tsdb/minutely/{key}.parq")
		df.to_csv(f"/data/adbcsv/{key}_minutely.csv", index=False)
	logger.info("spot_minutely.finished.")


def spots_minutely():
	"""
	Maintain minutely spot aggregates.
	"""
	logger.info("spots_minutely.started.")
	spot_keys = spot_keys.copy()
	spot_keys.remove("bisq")
	df = pd.read_parquet(f"/data/tsdb/minutely/{spot_keys[0]}.parq")
	df["source"] = spot_keys[0]
	for spot_key in spot_keys[1:]:
		df = pd.concat([df, pd.read_parquet(f"/data/tsdb/minutely/{spot_key}.parq")], ignore_index=True)
		df.source = df.source.fillna(source)
	cutoff = datetime.datetime.utcnow().replace(second=0, microsecond=0)
	cutoff = cutoff - datetime.timedelta(hours=3*24)
	cutoff = datetime.datetime(*cutoff.timetuple()[:6])
	df = df[df.date >= cutoff]
	df.to_csv("/data/adbcsv/spots_minutely.csv", index=False)
	df = df.drop_duplicates(subset=["source"], keep="last")
	df = df[df.source != "bisq"].sort_values("value", ascending=True, axis=0)
	df.to_csv("/data/adbcsv/spots_minutely_tail.csv", index=False)
	logger.info("spots_minutely.finished.")


def stats_minutely():
	"""
	Maintain stats_minutely.csv.
	"""
	df = pd.read_parquet("/data/tsdb/blockchain_stats_minutely.parq")
	keep_stats = [
		"date",
		"timestamp",
		"market_price_usd",
		"trade_volume_btc",
		"blocks_size",
		"hash_rate",
		"difficulty",
		"miners_revenue_btc",
		"n_blocks_total",
		"minutes_between_blocks"
	]
	df = df[keep_stats]
	df["log_hash_rate"] = df.hash_rate.apply(math.log10)
	df.to_csv("/data/arrows/stats_minutely.csv", index=False)
	logger.info("stats minutely finished.")


def minute_arrow():
	stats_minutely()
	keys_minutely()
	spots_minutely()


def day_arrow():
	for key in keys:
		df = pd.read_parquet(f"/data/tsdb/daily/{key}.parq")
		df.to_csv(f"/data/adbcsv/{key}_daily.csv", index=False)



