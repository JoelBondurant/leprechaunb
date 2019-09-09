"""
Bitcoin price history.
"""
import datetime
import os

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


def minute_arrow():
	for source in sources:
		df = pd.read_parquet(f"/data/tsdb/{source}_minutely.parq")
		df.to_csv(f"/data/arrows/{source}_minutely.csv", index=False)


def day_arrow():
	for source in sources:
		df = pd.read_parquet(f"/data/tsdb/{source}_daily.parq")
		df.to_csv(f"/data/arrows/{source}_daily.csv", index=False)




