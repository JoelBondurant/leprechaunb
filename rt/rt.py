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
from util import stats

# Data sources:
from sources import gold
from sources import bitcoin


# The period of the rt phase, collection must complete within the rt PERIOD:
PERIOD = 10

# Break the Period into this many sub intervals:
SUBPERIODS = 2

# A subperiod/timeout for retry loops:
SUBPERIOD = max(1, PERIOD // SUBPERIODS)


def peek():
	"""
	Interactive debugging in prod...
	"""
	return rock.rocks("rtdb").get("spot_xaubtc")


def get_spots(spot_type, timeout=SUBPERIOD, max_tries=SUBPERIODS):
	"""
	Returns a list of the spot prices (calls .spot() on modules)
	"""
	if spot_type == "gold":
		spot_source_modules = gold.spot_source_modules
	elif spot_type == "bitcoin":
		spot_source_modules = bitcoin.spot_source_modules
	else:
		raise NotImplementedError("spot_type="+str(spot_type)+"not implemented")
	tries = 0
	while True:
		tries += 1
		if tries > max_tries:
			break
		try:
			mw = len(spot_source_modules)
			with concurrent.futures.ThreadPoolExecutor(max_workers=mw) as executor:
				res = executor.map(lambda x: x.spot(), spot_source_modules, timeout=timeout)
			return list(res)
		except Exception as ex:
			logger.exception(ex)
			time.sleep(1)


def write_rt():
	"""
	Write real-time data.
	"""
	try:
		# Gold Spots:
		spots_usdxau = get_spots("gold")
		#logger.info("spots_usdxau" + str(spots_usdxau))
		spot_usdxau = stats.robust_mean(spots_usdxau)

		# Bitcoin Spots:
		spots_usdbtc = get_spots("bitcoin")
		#logger.info("spots_usdbtc" + str(spots_usdbtc))
		spot_usdbtc = stats.robust_mean(spots_usdbtc)

		# Average Spot:
		spot_xaubtc = spot_usdbtc / spot_usdxau
		spot_btcxau = 1.0 / spot_xaubtc

		# Purge terrorism units:
		spots_xaubtc = [x/spot_usdxau for x in spots_usdbtc]
		spots_btcxau = [1.0/x for x in spots_xaubtc]

		# Network Stats:
		blockchain_stats = bitcoin.blockchain.stats()

		# Storage:
		dats = []
		keys = []

		for source, source_spot in zip(gold.spot_source_names, spots_btcxau):
			key = f"{source}_spot_btcxau"
			keys += [key]
			dats += [(key, source_spot)]

		for source, source_spot in zip(bitcoin.spot_source_names, spots_xaubtc):
			key = f"{source}_spot_xaubtc"
			keys += [key]
			dats += [(key, source_spot)]

		extra_dats = [
			("spot_usdxau", spot_usdxau),
			("spot_usdbtc",spot_usdbtc),
			("spot_btcxau", spot_btcxau),
			("spot_xaubtc", spot_xaubtc),
			("blockchain_stats", blockchain_stats),
			("rtdb_timestamp", int(time.time())),
		]

		dats += extra_dats
		keys += [x[0] for x in extra_dats]
		dats += [
			("keys", keys),
		]

		for dat in dats:
			#logger.info("rtdb.put: " + dat[0])
			rock.rocks("rtdb").put(dat[0], dat[1])

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

