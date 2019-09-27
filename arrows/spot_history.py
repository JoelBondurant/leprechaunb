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
from util import rock



rtdb_keys = list(rock.rocks("tsdbrocks").get("rtdb_data").keys())

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
		if key.endswith("_timestamp"):
			continue
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
	df["log_difficulty"] = df.difficulty.apply(math.log10)
	df["log_hash_rate"] = df.hash_rate.apply(math.log10)
	df["arrival_rate"] = (df.minutes_between_blocks * 60).astype(int)
	df.to_csv("/data/adbcsv/stats_minutely.csv", index=False)
	logger.info("</stats_minutely>")



def minute_arrow():
	"""
	External minute level wrapper.
	"""
	stats_minutely()
	keys_minutely()
	spots_minutely()


def day_spot_model():
	"""
	Daily spot model.
	"""
	logger.info("<day_spot_model>")

	fn = "/data/tsdb/daily/spot_xaubtc.parq"
	df = pd.read_parquet(fn)
	df.columns = ["date", "spot"]

	df["time"] = range(len(df))
	df["log1p_spot"] = df.spot.apply(np.log1p)

	aa, bb, cc, dd, ee = np.polyfit(df.time, df.log1p_spot, 4)

	labels = [f"_{x}" for x in range(6)]
	log_pads = [-0.80, -0.40, 0.0, 0.5, 1.0, 1.1]
	exp_pads = [0.66, 0.50, 0.25, -0.2, -1.0, -1.1]
	for label, lpad, epad in zip(labels, log_pads, exp_pads):
		log1p_spot_model = aa*df.time**4 + bb*df.time**3 + cc*df.time**2 + dd*df.time + ee
		log1p_spot_model += lpad
		spot_model = np.exp(log1p_spot_model) - 1
		spot_model += epad
		df[f"spot_model{label}"] = spot_model

	df.to_csv("/data/adbcsv/spot_model_xaubtc_daily.csv", index=False)
	logger.info("</day_spot_model>")


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
			df.to_csv(f"/data/adbcsv/{key}_daily.csv", index=False)
		else:
			logger.warn(f"/data/tsdb/daily/{key}.parq files are missing.")
	day_spot_model()
	logger.info("</day_arrow>")


