# Binance Data Ingress
import datetime
import requests


# Binance API Endpoints:
base_uri = "https://api.binance.com/api/v1/"


def spot(symbol="BTCUSDT"):
	"""
	Binance realtime prices.
		symbol- [BTCUSDT]
	"""
	resp = requests.get(base_uri + f"ticker/price?symbol={symbol}").json()
	return float(resp["price"])

