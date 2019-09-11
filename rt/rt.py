#!/usr/bin/env python3
"""
Realtime/microbatch (<=10 second latency) data collection.

Historical patching of data will be done in ts (time series constructor service),
rt will be ephemeral, no worries about past data here.
"""
import concurrent.futures
import statistics
import time

from util import logger
from util import rock
from util import stats

# Realtime data sources:
# Gold Spots:
from sources import apmex
# Bitcoin Spots:
from sources import binance
from sources import bisq
from sources import bitfinex
from sources import bitstamp
from sources import bittrex
from sources import btse
from sources import cex
from sources import coinbase
from sources import gemini
from sources import huobi
from sources import itbit
from sources import kraken
from sources import poloniex
# Bitcoin Network:
from sources import blockchain


# The period of the rt phase, collection must complete within the rt PERIOD:
# Light can circle the planet almost twice, but not quite in this time:
PERIOD = 14

# Break the Period into this many sub intervals:
SUBPERIODS = 2

# A subperiod/timeout for retry loops:
SUBPERIOD = max(1, PERIOD // SUBPERIODS)

# How bandy is the cloudness:
NETHREADS = 16


_spot_sources = {
	"binance": binance,
	"bisq": bisq,
	"bitfinex": bitfinex,
	"bitstamp": bitstamp,
	"bittrex": bittrex,
	"btse": btse,
	"cex": cex,
	"coinbase": coinbase,
	"gemini": gemini,
	"huobi": huobi,
	"itbit": itbit,
	"kraken": kraken,
	"poloniex": poloniex,
}


def get_spot_source_names():
	"""
	List of names for Bitcoin spot price source data.
	"""
	return list(_spot_sources.keys())


def get_spots(timeout=SUBPERIOD, max_tries=SUBPERIODS):
	"""
	Returns a list of the spot prices
	"""
	tries = 0
	while True:
		tries += 1
		if tries > max_tries:
			break
		try:
			with concurrent.futures.ThreadPoolExecutor(max_workers=NETHREADS) as executor:
				res = executor.map(lambda x: x.spot(), _spot_sources.values(), timeout=timeout)
			return res
		except Exception as ex:
			logger.exception(ex)
			time.sleep(1)
		


def write_rt():
	"""
	Write real-time data.
	"""
	try:
		# Gold Spots:
		# Struggling to snatch up realtime gold data.
		apmex_spot = apmex.spot()
		gold_spot = apmex_spot

		# Bitcoin Spots:
		spot_source_names = get_spot_source_names()
		spots_usd = get_spots()
		spots = [s / gold_spot for s in spots_usd]
		spot = statistics.mean(stats.filter_outliers(spots))
		spot_usd = spot * gold_spot

		# Network Stats:
		blockchain_stats = blockchain.stats()

		# Storage:
		dats = []
		for source, source_spot in zip(spot_source_names, spots):
			dats += [(f"{source}_spot", source_spot)]

		dats += [
			# Gold:
			("apmex_spot", apmex_spot),
			("gold_spot", gold_spot),

			# Bitcoin:
			("spot", spot),
			("spot_usd", spot_usd),
			("blockchain_stats", blockchain_stats)
		]

		rtdb = rock.Rock("rtdb")
		for dat in dats:
			rtdb.put(dat[0], dat[1])
	except Exception as ex:
		time.sleep(4)
		logger.exception(ex)


def main():
	"""
	Main rt entry point.
	"""
	tcounter = 0
	while True:
		time.sleep(PERIOD)
		tcounter += PERIOD
		if tcounter > 600:
			tcounter = 0
			logger.info("heartbeat")
		write_rt()


if __name__ == "__main__":
	main()

