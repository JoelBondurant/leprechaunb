# Gemini Data Ingress
import requests

from util import logger

# Gemini API Endpoints:
base_uri = "https://api.gemini.com/v1/"


"""
Gemini realtime prices.
	symbol - [btcusd]
"""
def spot(symbol="btcusd"):
	resp = requests.get(base_uri + f"pubticker/{symbol}").json()
	return float(resp["last"])

