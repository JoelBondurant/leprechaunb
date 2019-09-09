"""
Bitcoin price history.
"""
import datetime
import os
import time

import pandas as pd

from util import logger


sources = [
	"apmex_spot",
	"binance_spot",
	"bitfinex_spot",
	"bitstamp_spot",
	"coinbase_spot",
	"gemini_spot",
	"kraken_spot",
	"gold_spot",
	"spot",
	"spot_usd"
]


def spot_minutely():
	for source in sources:
		df = pd.read_parquet(f"/data/tsdb/{source}_minutely.parq")
		df.to_csv(f"/data/arrows/{source}_minutely.csv", index=False)


def spots_minutely():
	sources = ("binance", "bitfinex", "bitstamp", "coinbase", "gemini", "kraken")
	df = pd.read_parquet(f"/data/tsdb/{sources[0]}_spot_minutely.parq")
	df["source"] = sources[0]
	for source in sources[1:]:
		df = pd.concat([df, pd.read_parquet(f"/data/tsdb/{source}_spot_minutely.parq")])
		df.source = df.source.fillna(source)
	df.to_csv("/data/arrows/spots_minutely.csv", index=False)


def minute_arrow():
	spot_minutely()
	spots_minutely()


def day_arrow():
	for source in sources:
		df = pd.read_parquet(f"/data/tsdb/{source}_daily.parq")
		df.to_csv(f"/data/arrows/{source}_daily.csv", index=False)



