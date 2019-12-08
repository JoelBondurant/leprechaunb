"""
Bitcoin stats history.
"""
import math

import pandas as pd

from util import logger
from util import racoon


def minute_arrow():
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
	df["arrival_rate"] = (df.minutes_between_blocks * 60).astype(int)
	racoon.to_csv(df, "/data/adbcsv/stats_minutely.csv")
	logger.info("</stats_minutely>")

