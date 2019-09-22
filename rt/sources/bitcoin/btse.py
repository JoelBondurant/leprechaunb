# BTSE Data Ingress

from util import web

# BTSE API Endpoints:
base_uri = "https://api.btse.com/"


def spot(symbol="BTC-USD"):
	"""
	BTSE realtime prices.
		symbol - [BTC-USD]
	"""
	resp = web.get(base_uri + f"spot/v2/ticker/{symbol}")
	return float(resp["price"])

