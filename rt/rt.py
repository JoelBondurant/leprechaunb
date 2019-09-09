#!/usr/bin/env python3
"""
Realtime/microbatch (<=10 second latency) data collection.

Historical patching of data will be done in ts (time series constructor service),
rt will be ephemeral, no worries about past data here.
"""
import statistics
import time

from util import logger
from util import rock

# Realtime data sources:
import apmex
import blockchain
import binance
import bitfinex
import bitstamp
import coinbase
import gemini
import kraken


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
		binance_spot = binance.spot() / gold_spot
		bitfinex_spot = bitfinex.spot() / gold_spot
		bitstamp_spot = bitstamp.spot() / gold_spot
		coinbase_spot = coinbase.spot() / gold_spot
		gemini_spot = gemini.spot() / gold_spot
		kraken_spot = kraken.spot() / gold_spot

		# Summary Stats:
		bitcoin_spots = [
			binance_spot,
			bitfinex_spot,
			bitstamp_spot,
			coinbase_spot,
			gemini_spot,
			kraken_spot
		]
		bitcoin_spot = statistics.mean(bitcoin_spots)
		bitcoin_spot_usd = bitcoin_spot * gold_spot

		# Network Stats:
		blockchain_stats = blockchain.stats()

		# Storage:
		dats = (
			("binance_spot", binance_spot),
			("bitfinex_spot", bitfinex_spot),
			("bitstamp_spot", bitstamp_spot),
			("coinbase_spot", coinbase_spot),
			("gemini_spot", gemini_spot),
			("kraken_spot", kraken_spot),
			("apmex_spot", apmex_spot),
			("gold_spot", gold_spot),
			("spot", bitcoin_spot),
			("spot_usd", bitcoin_spot_usd),
			("blockchain_stats", blockchain_stats)
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


