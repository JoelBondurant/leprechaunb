# Bitfinex Data Ingress
import requests

from util import logger

# Bitfinex API Endpoints:
base_uri = "https://api-pub.bitfinex.com/v2/"


"""
Bitfinex realtime prices.
	ticker - [tBTCUSD]
"""
def spot(ticker="tBTCUSD"):
	resp = requests.get(base_uri + f"ticker/{ticker}").json()
	return float(resp[-4])

