# Gemini Data Ingress
import requests

from util import logger

# Gemini API Endpoints:
base_uri = "https://api.gemini.com/v1/"


def spot(symbol="btcusd"):
	"""
	Gemini realtime prices.
		symbol - [btcusd]
	"""
	resp = requests.get(base_uri + f"pubticker/{symbol}").json()
	return float(resp["last"])

