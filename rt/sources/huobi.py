# Huobi Data Ingress
import requests

from util import logger

# Huobi API Endpoints:
base_uri = "https://api.huobi.pro/"


"""
Huobi realtime prices.
	symbol - [btcusdt]
"""
def spot(symbol="btcusdt"):
	resp = requests.get(base_uri + f"market/detail/merged?symbol={symbol}").json()
	resp = resp["tick"]
	ask = resp["ask"][0]
	bid = resp["bid"][0]
	return (ask + bid)/2.0

