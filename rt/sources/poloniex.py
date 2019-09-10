# Poloniex Data Ingress
import requests

from util import logger

# Poloniex API Endpoints:
base_uri = "https://poloniex.com/public"


"""
Poloniex realtime prices.
	symbol - [USDT_BTC]
"""
def spot(symbol="USDT_BTC"):
	resp = requests.get(base_uri + "?command=returnTicker").json()
	return float(resp[symbol]["last"])

