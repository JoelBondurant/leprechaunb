# Cex Data Ingress

import cachetools.func

from util import web


# Cex API Endpoints:
base_uri = "https://cex.io/api/"


@cachetools.func.ttl_cache(ttl=10)
def spot(symbol1="BTC", symbol2="USD"):
	"""
	Cex realtime prices.
		symbol1 - [BTC]
		symbol2 - [USD]
	"""
	resp = web.get(base_uri + f"ticker/{symbol1}/{symbol2}")
	return float(resp["last"])

