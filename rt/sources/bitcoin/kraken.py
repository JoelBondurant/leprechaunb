"""
Kraken Data Ingress
"""

from util import web


# Kraken API Endpoints:
base_uri = "https://api.kraken.com/0/public/"


def spot(pair="XBTUSD", full_pair="XXBTZUSD"):
	"""
	Kraken realtime prices.
		pair - [XBTUSD]
	"""
	resp = web.get(base_uri + f"Ticker?pair={pair}")
	return float(resp["result"][full_pair]["c"][0])

