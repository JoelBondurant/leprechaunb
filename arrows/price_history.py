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
	"coinbase_spot",
	"gold_spot",
	"kraken_spot",
	"spot",
	"spot_usd"
]


def spot_minutely():
	for source in sources:
		df = pd.read_parquet(f"/data/tsdb/{source}_minutely.parq")
		df.to_csv(f"/data/arrows/{source}_minutely.csv", index=False)


def spots_minutely():
	df = pd.read_parquet(f"/data/tsdb/binance_spot_minutely.parq")
	df["source"] = "binance"
	df = pd.concat([df, pd.read_parquet(f"/data/tsdb/coinbase_spot_minutely.parq")])
	df.source = df.source.fillna("coinbase")
	df = pd.concat([df, pd.read_parquet(f"/data/tsdb/kraken_spot_minutely.parq")])
	df.source = df.source.fillna("kraken")
	df.to_csv("/data/arrows/spots_minutely.csv", index=False)


def minute_arrow():
	spot_minutely()
	spots_minutely()


def day_arrow():
	for source in sources:
		df = pd.read_parquet(f"/data/tsdb/{source}_daily.parq")
		df.to_csv(f"/data/arrows/{source}_daily.csv", index=False)



