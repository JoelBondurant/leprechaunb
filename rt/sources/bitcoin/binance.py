# Binance Data Ingress

import cachetools.func

from util import web

# Binance API Endpoints:
base_uri = "https://api.binance.com/api/v1/"


@cachetools.func.ttl_cache(ttl=10)
def spot(symbol="BTCUSDT"):
	"""
	Binance realtime prices.
		symbol- [BTCUSDT]
	"""
	resp = web.get(base_uri + f"ticker/price?symbol={symbol}")
	return float(resp["price"])

