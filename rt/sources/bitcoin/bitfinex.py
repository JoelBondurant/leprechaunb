# Bitfinex Data Ingress

import cachetools.func

from util import web


# Bitfinex API Endpoints:
base_uri = "https://api-pub.bitfinex.com/v2/"


@cachetools.func.ttl_cache(ttl=10)
def spot(ticker="tBTCUSD"):
	"""
	Bitfinex realtime prices.
		ticker - [tBTCUSD]
	"""
	resp = web.get(base_uri + f"ticker/{ticker}")
	return float(resp[-4])

