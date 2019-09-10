# Kraken Data Ingress
import requests

from util import logger

# Kraken API Endpoints:
base_uri = "https://api.kraken.com/0/public/"


"""
Kraken realtime prices.
	pair - [XBTUSD]
"""
def spot(pair="XBTUSD", full_pair="XXBTZUSD"):
	resp = requests.get(base_uri + f"Ticker?pair={pair}").json()
	return float(resp["result"][full_pair]["c"][0])

