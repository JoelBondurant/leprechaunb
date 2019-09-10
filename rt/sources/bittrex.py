# Bittrex Data Ingress
import requests

from util import logger

# Bittrex API Endpoints:
base_uri = "https://api.bittrex.com/api/v1.1/public/"


"""
Bittrex realtime prices.
	market - [USD-BTC]
"""
def spot(market="USD-BTC"):
	resp = requests.get(base_uri + f"getticker?market={market}").json()
	return float(resp["result"]["Last"])

