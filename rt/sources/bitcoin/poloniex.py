"""
Poloniex Data Ingress
"""

from util import web


# Poloniex API Endpoints:
base_uri = "https://poloniex.com/public"


def spot(symbol="USDT_BTC"):
	"""
	Poloniex realtime prices.
		symbol - [USDT_BTC]
	"""
	resp = web.get(base_uri + "?command=returnTicker")
	return float(resp[symbol]["last"])

