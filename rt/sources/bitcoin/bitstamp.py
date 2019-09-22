# Bitstamp Data Ingress
import requests

from util import logger

# Bitstamp API Endpoints:
base_uri = "https://www.bitstamp.com/api/v2/"


def spot(ticker="btcusd"):
	"""
	Bitstamp realtime prices.
		ticker - [btcusd]
	"""
	resp = requests.get(base_uri + f"ticker/{ticker}").json()
	return float(resp["last"])

