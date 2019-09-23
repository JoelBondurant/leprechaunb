#!/usr/bin/env python3
"""
Realtime/microbatch (<=10 second latency) data collection.

Historical patching of data will be done in ts (time series constructor service),
rt will be ephemeral, no worries about past data here.
"""
import concurrent.futures
import time

from util import logger
from util import rock

# Data sources:
from sources import gold
from sources import bitcoin


def rtdb():
	return rock.Rock("rtdb") 


# The period of the rt phase, collection must complete within the rt PERIOD:
PERIOD = 10

# Break the Period into this many sub intervals:
SUBPERIODS = 2

# A subperiod/timeout for retry loops:
SUBPERIOD = max(1, PERIOD // SUBPERIODS)


def get_spots(spot_source_modules, timeout=SUBPERIOD, max_tries=SUBPERIODS):
	"""
	Returns a list of the spot prices (calls .spot() on modules)
	"""
	tries = 0
	while True:
		tries += 1
		if tries > max_tries:
			break
		try:
			mw = len(spot_source_modules)
			with concurrent.futures.ThreadPoolExecutor(max_workers=mw) as executor:
				res = executor.map(lambda x: x.spot(), spot_source_modules, timeout=timeout)
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
		spots_usdxau = get_spots(gold.spot_source_modules)

		# Bitcoin Spots:
		spots_usdbtc = get_spots(bitcoin.spot_source_modules)

		# Network Stats:
		blockchain_stats = bitcoin.blockchain.stats()

		# Storage:
		dats = []
		keys = []

		for source, source_spot in zip(gold.spot_source_names, spots_usdxau):
			key = f"{source}_spot_usdxau"
			keys += [key]
			dats += [(key, source_spot)]

		for source, source_spot in zip(bitcoin.spot_source_names, spots_usdbtc):
			key = f"{source}_spot_usdbtc"
			keys += [key]
			dats += [(key, source_spot)]

		keys += ["blockchain_stats", "rtdb_timestamp"]
		dats += [
			("blockchain_stats", blockchain_stats),
			("rtdb_timestamp", int(time.time())),
			("keys", keys),
		]

		db = rtdb()
		for dat in dats:
			db.put(dat[0], dat[1])

	except Exception as ex:
		time.sleep(4)
		logger.exception(ex)


def main():
	"""
	Main rt entry point.
	"""
	logger.info("rt started")
	started = int(time.time())
	while True:
		try:
			elapsed = int(time.time())
			time.sleep(1)
			if int(time.time()) - started > 600:
				logger.info("heartbeat")
				started = int(time.time())
			logger.info("<write_rt>")
			write_rt()
			logger.info("</write_rt>")
			elapsed = int(time.time()) - elapsed
			time.sleep(max(0, PERIOD - elapsed))
		except Exception as ex:
			logger.exception(ex)


if __name__ == "__main__":
	main()

