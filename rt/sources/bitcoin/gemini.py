"""
Gemini Data Ingress
"""

from util import web


# Gemini API Endpoints:
base_uri = "https://api.gemini.com/v1/"


def spot(symbol="btcusd"):
	"""
	Gemini realtime prices.
		symbol - [btcusd]
	"""
	resp = web.get(base_uri + f"pubticker/{symbol}")
	return float(resp["last"])

