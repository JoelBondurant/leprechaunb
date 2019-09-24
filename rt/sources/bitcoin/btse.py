"""
BTSE Data Ingress
"""

import cachetools.func

from util import web


# BTSE API Endpoints:
base_uri = "https://api.btse.com/"


@cachetools.func.ttl_cache(ttl=20)
def spot(symbol="BTC-USD"):
	"""
	BTSE realtime prices.
		symbol - [BTC-USD]
	"""
	resp = web.get(base_uri + f"spot/v2/ticker/{symbol}")
	return float(resp["price"])

