# BTSE Data Ingress
import requests

from util import logger

# BTSE API Endpoints:
base_uri = "https://api.btse.com/"


"""
BTSE realtime prices.
	symbol - [BTC-USD]
"""
def spot(symbol="BTC-USD"):
	resp = requests.get(base_uri + f"spot/v2/ticker/{symbol}").json()
	return float(resp["price"])

