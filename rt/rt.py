#!/usr/bin/env python3
"""
Realtime/microbatch (~10 second latency) data collection.
"""
import statistics
import time

from util import logger
from util import rock

# Realtime data sources:
import apmex
import binance
import coinbase
import kraken


def write_rt():
	"""
	Write real-time data.
	"""
	try:
		# Gold Spots:
		apmex_spot = apmex.spot()
		gold_spot = apmex_spot

		# Bitcoin Spots:
		binance_spot = binance.spot() / gold_spot
		coinbase_spot = coinbase.spot() / gold_spot
		kraken_spot = kraken.spot() / gold_spot

		# Summary Stats:
		bitcoin_spots = [binance_spot, coinbase_spot, kraken_spot]
		bitcoin_spot = statistics.mean(bitcoin_spots)
		bitcoin_spot_usd = bitcoin_spot * gold_spot

		# Storage:
		dats = (
			("binance.spot", binance_spot),
			("coinbase.spot", coinbase_spot),
			("kraken.spot", kraken_spot),
			("apmex.spot", apmex_spot),
			("gold.spot", gold_spot),
			("spot", bitcoin_spot),
			("spot.usd", bitcoin_spot_usd)
		)
		rtdb = rock.Rock("rtdb")
		for dat in dats:
			rtdb.put(dat[0], dat[1])
	except Exception as ex:
		time.sleep(4)
		logger.exception(ex)


tcounter = 0
while True:
	time.sleep(10)
	tcounter += 10
	if tcounter > 120:
		tcounter = 0
		logger.info("heartbeat")
	write_rt()


