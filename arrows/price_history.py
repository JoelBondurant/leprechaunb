"""
Bitcoin price history.
"""
import datetime
import os

import schedule
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


def minutely_arrow():
	for source in sources:
		df = pd.read_parquet(f"/data/tsdb/{source}.parq")
		df.to_csv(f"/data/arrows/{source}_minutely.csv", index=False)


def daily_arrow():
	## Yahoo Finance BTC-USD data since 2010-07-17.
	daily_source = "/data/bootstrap/BTC-USD.csv"
	if not os.path.exists(daily_parq):
		logger.info("bootstrap daily price history")
		# Massage raw price history from Yahoo:
		df = pd.read_csv(source)
		df.columns = df.columns.str.lower()
		df = df[["date","close"]]
		df.date = pd.to_datetime(df.date)
		# Back convert data to gold basis:
		gold = quandl.get("WGC/GOLD_DAILY_USD", start_date="2010-07-17").reset_index()
		gold.columns = ["date", "gold"]
		df = df.merge(gold, on="date", how="left")
		df = df.ffill().bfill()
		df.close = (df.close / df.gold) * rock.grams_per_toz
		df = df[["date","close"]]
		df.to_parquet(daily_parq)
		df.to_csv(daily_csv, index=False)
	else:
		df = pd.read_parquet(daily_parq)
		last_date = df.date.iloc[-1]
		nowish = pd.Timestamp.now().date()
		if nowish > last_date:
			logger.info("update daily price history")
			tsdb = rock.Rock("ts")
			spot = tsdb.get("spot."+rock.daystamp())
			dt = datetime.datetime.utcnow().date()
			nowpie = {"date":dt, "close":spot}
			df = df.append(nowpie, ignore_index=True)
			df.date = pd.to_datetime(df.date).dt.round("ms")
			df.to_parquet(daily_parq)
			df.to_csv(daily_csv, index=False)


def arrow():
	"""
	Arrow stuff.
	"""
	minutely_arrow()


schedule.every(60).seconds.do(arrow)

if __name__ == "__main__":
	logger.info("arrows started.")
	while True:
		schedule.run_pending()
		time.sleep(1)


