"""
Bittrex Data Ingress
"""

import cachetools.func

from util import web


# Bittrex API Endpoints:
base_uri = "https://api.bittrex.com/api/v1.1/public/"


@cachetools.func.ttl_cache(ttl=10)
def spot(market="USD-BTC"):
	"""
	Bittrex realtime prices.
		market - [USD-BTC]
	"""
	resp = web.get(base_uri + f"getticker?market={market}")
	return float(resp["result"]["Last"])

