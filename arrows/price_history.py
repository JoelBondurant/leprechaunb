"""
Bitcoin price history.
"""
import datetime
import os
import time

import pandas as pd

from util import logger


spot_sources = [
	# Bitcoin spots:
	"binance_spot",
	"bisq_spot",
	"bitfinex_spot",
	"bitstamp_spot",
	"bittrex_spot",
	"btse_spot",
	"cex_spot",
	"coinbase_spot",
	"gemini_spot",
	"huobi_spot",
	"itbit_spot",
	"kraken_spot",
	"poloniex_spot",
]

sources = spot_sources.copy()
sources += [
	# Gold spots:
	"apmex_spot",
	"gold_spot",
	# Bitcoin:
	"spot",
	"spot_usd"
]


def spot_minutely():
	"""
	Maintain the minutely spot files.
	"""
	logger.info("spot_minutely.started.")
	for source in sources:
		df = pd.read_parquet(f"/data/tsdb/{source}_minutely.parq")
		df.to_csv(f"/data/arrows/{source}_minutely.csv", index=False)
	logger.info("spot_minutely.finished.")


def spots_minutely():
	"""
	Maintain minutely spot aggregates.
	"""
	logger.info("spots_minutely.started.")
	sources = [s.replace("_spot", "") for s in spot_sources]
	sources.remove("bisq")
	df = pd.read_parquet(f"/data/tsdb/{sources[0]}_spot_minutely.parq")
	df["source"] = sources[0]
	for source in sources[1:]:
		df = pd.concat([df, pd.read_parquet(f"/data/tsdb/{source}_spot_minutely.parq")], ignore_index=True)
		df.source = df.source.fillna(source)
	cutoff = datetime.datetime.utcnow().replace(second=0, microsecond=0)
	cutoff = cutoff - datetime.timedelta(hours=3*24)
	cutoff = datetime.datetime(*cutoff.timetuple()[:6])
	df = df[df.date >= cutoff]
	df.to_csv("/data/arrows/spots_minutely.csv", index=False)
	df = df.drop_duplicates(subset=["source"], keep="last")
	df = df[df.source != "bisq"].sort_values("value", ascending=True, axis=0)
	df.to_csv("/data/arrows/spots_minutely_tail.csv", index=False)
	logger.info("spots_minutely.finished.")


def stats_minutely():
	"""
	Maintain stats_minutely.csv.
	"""
	df = pd.read_parquet("/data/tsdb/blockchain_stats_minutely.parq")
	keep_stats = ["timestamp", "market_price_usd", "trade_volume_btc", "blocks_size", "hash_rate", "difficulty", "miners_revenue_btc", "n_blocks_total", "minutes_between_blocks"]
	df = df[keep_stats]
	df.to_csv("/data/arrows/stats_minutely.csv", index=False)
	logger.info("stats minutely finished.")


def minute_arrow():
	stats_minutely()
	spot_minutely()
	spots_minutely()


def day_arrow():
	for source in sources:
		df = pd.read_parquet(f"/data/tsdb/{source}_daily.parq")
		df.to_csv(f"/data/arrows/{source}_daily.csv", index=False)



