"""
itBit Data Ingress
"""

from util import web


# itBit API Endpoints:
base_uri = "https://api.itbit.com/v1/"


def spot(symbol="XBTUSD"):
	"""
	itBit realtime prices.
		symbol - [XBTUSD]
	"""
	resp = web.get(base_uri + f"markets/{symbol}/ticker")
	return float(resp["lastPrice"])

