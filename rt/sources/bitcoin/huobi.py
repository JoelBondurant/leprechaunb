"""
Huobi Data Ingress
"""

import cachetools.func

from util import web


# Huobi API Endpoints:
base_uri = "https://api.huobi.pro/"


@cachetools.func.ttl_cache(ttl=10)
def spot(symbol="btcusdt"):
	"""
	Huobi realtime prices.
		symbol - [btcusdt]
	"""
	resp = web.get(base_uri + f"market/detail/merged?symbol={symbol}")
	resp = resp["tick"]
	ask = resp["ask"][0]
	bid = resp["bid"][0]
	return (ask + bid)/2.0

