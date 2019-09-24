"""
Bitstamp Data Ingress
"""

import cachetools.func

from util import logger
from util import web


# Bitstamp API Endpoints:
base_uri = "https://www.bitstamp.com/api/v2/"


@cachetools.func.ttl_cache(ttl=10)
def spot(ticker="btcusd"):
	"""
	Bitstamp realtime prices.
		ticker - [btcusd]
	"""
	resp = web.get(base_uri + f"ticker/{ticker}")
	return float(resp["last"])

