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


gold_spot_keys = [x for x in rtdb_keys if "_spot_btcxau" in x]
bitcoin_spot_keys = [x for x in rtdb_keys if "_spot_xaubtc" in x]
#logger.info("gold_spot_keys: " + str(gold_spot_keys))
#logger.info("bitcoin_spot_keys: " + str(bitcoin_spot_keys))
keys = rtdb_keys.copy()


def keys_minutely():
	"""
	Maintain the minutely key files.
	"""
	logger.info("<keys_minutely>")
	for key in keys:
		df = pd.read_parquet(f"/data/tsdb/minutely/{key}.parq")
		df.to_csv(f"/data/adbcsv/{key}_minutely.csv", index=False)
	logger.info("</keys_minutely>")


def spots_minutely():
	"""
	Maintain minutely spot aggregates.
	"""
	global gold_spot_keys
	global bitcoin_spot_keys
	logger.info("<spots_minutely>")
	##############
	# Gold:
	##############
	gold_spot_keys = gold_spot_keys.copy()
	df = pd.read_parquet(f"/data/tsdb/minutely/{gold_spot_keys[0]}.parq")
	df["source"] = gold_spot_keys[0].split("_")[0]
	for spot_key in gold_spot_keys[1:]:
		df = pd.concat([df, pd.read_parquet(f"/data/tsdb/minutely/{spot_key}.parq")], ignore_index=True, sort=True)
		source = spot_key.split("_")[0]
		df.source = df.source.fillna(source)
	cutoff = datetime.datetime.utcnow().replace(second=0, microsecond=0)
	cutoff = cutoff - datetime.timedelta(hours=3*24)
	cutoff = datetime.datetime(*cutoff.timetuple()[:6])
	df = df[df.date >= cutoff]
	df.to_csv("/data/adbcsv/spots_btcxau_minutely.csv", index=False)
	df = df.drop_duplicates(subset=["source"], keep="last")
	df = df[df.source != "bisq"].sort_values("value", ascending=True, axis=0)
	df.to_csv("/data/adbcsv/spots_btcxau_minutely_tail.csv", index=False)
	##############
	# Bitcoin:
	##############
	bitcoin_spot_keys = bitcoin_spot_keys.copy()
	bitcoin_spot_keys = [x for x in bitcoin_spot_keys if "bisq" not in x]
	df = pd.read_parquet(f"/data/tsdb/minutely/{bitcoin_spot_keys[0]}.parq")
	df["source"] = bitcoin_spot_keys[0].split("_")[0]
	for spot_key in bitcoin_spot_keys[1:]:
		df = pd.concat([df, pd.read_parquet(f"/data/tsdb/minutely/{spot_key}.parq")], ignore_index=True, sort=True)
		source = spot_key.split("_")[0]
		df.source = df.source.fillna(source)
	cutoff = datetime.datetime.utcnow().replace(second=0, microsecond=0)
	cutoff = cutoff - datetime.timedelta(hours=3*24)
	cutoff = datetime.datetime(*cutoff.timetuple()[:6])
	df = df[df.date >= cutoff]
	df.to_csv("/data/adbcsv/spots_xaubtc_minutely.csv", index=False)
	df = df.drop_duplicates(subset=["source"], keep="last")
	df = df[df.source != "bisq"].sort_values("value", ascending=True, axis=0)
	df.to_csv("/data/adbcsv/spots_xaubtc_minutely_tail.csv", index=False)
	logger.info("</spots_minutely>")


def stats_minutely():
	"""
	Maintain stats_minutely.csv.
	"""
	logger.info("<stats_minutely>")
	df = pd.read_parquet("/data/tsdb/minutely/blockchain_stats.parq")
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
	df.to_csv("/data/adbcsv/stats_minutely.csv", index=False)
	logger.info("</stats_minutely>")


def minute_arrow():
	stats_minutely()
	keys_minutely()
	spots_minutely()


def day_arrow():
	logger.info("<day_arrow>")
	for key in keys:
		df = pd.read_parquet(f"/data/tsdb/daily/{key}.parq")
		df.to_csv(f"/data/adbcsv/{key}_daily.csv", index=False)
	logger.info("</day_arrow>")


