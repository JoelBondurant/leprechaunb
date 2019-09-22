# Bittrex Data Ingress

from util import web

# Bittrex API Endpoints:
base_uri = "https://api.bittrex.com/api/v1.1/public/"


def spot(market="USD-BTC"):
	"""
	Bittrex realtime prices.
		market - [USD-BTC]
	"""
	resp = web.get(base_uri + f"getticker?market={market}")
	return float(resp["result"]["Last"])

