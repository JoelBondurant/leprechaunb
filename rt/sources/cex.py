# Cex Data Ingress
import requests

from util import logger

# Cex API Endpoints:
base_uri = "https://cex.io/api/"


"""
Cex realtime prices.
	symbol1 - [BTC]
	symbol2 - [USD]
"""
def spot(symbol1="BTC", symbol2="USD"):
	resp = requests.get(base_uri + f"ticker/{symbol1}/{symbol2}").json()
	return float(resp["last"])

