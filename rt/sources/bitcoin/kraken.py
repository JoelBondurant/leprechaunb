"""
Kraken Data Ingress
"""

import cachetools.func

from util import web


# Kraken API Endpoints:
base_uri = "https://api.kraken.com/0/public/"


@cachetools.func.ttl_cache(ttl=10)
def spot(pair="XBTUSD", full_pair="XXBTZUSD"):
	"""
	Kraken realtime prices.
		pair - [XBTUSD]
	"""
	resp = web.get(base_uri + f"Ticker?pair={pair}")
	return float(resp["result"][full_pair]["c"][0])

