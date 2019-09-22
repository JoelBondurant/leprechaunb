# Bitfinex Data Ingress

from util import web


# Bitfinex API Endpoints:
base_uri = "https://api-pub.bitfinex.com/v2/"


def spot(ticker="tBTCUSD"):
	"""
	Bitfinex realtime prices.
		ticker - [tBTCUSD]
	"""
	resp = web.get(base_uri + f"ticker/{ticker}")
	return float(resp[-4])

