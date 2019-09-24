"""
Gemini Data Ingress
"""

import cachetools.func

from util import web


# Gemini API Endpoints:
base_uri = "https://api.gemini.com/v1/"


@cachetools.func.ttl_cache(ttl=10)
def spot(symbol="btcusd"):
	"""
	Gemini realtime prices.
		symbol - [btcusd]
	"""
	resp = web.get(base_uri + f"pubticker/{symbol}")
	return float(resp["last"])

