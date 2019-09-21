# Coinbase Data Ingress
import requests

from util import logger

# Coinbase API Endpoints:
base_uri = "https://api.coinbase.com/v2/"


def spot(endpoint="spot", currency="USD"):
	"""
	Coinbase realtime prices.
		endpoint - [spot|buy|sell]
		currency - [USD]
	"""
	resp = requests.get(base_uri + f"prices/{endpoint}?" + f"currency={currency}").json()
	return float(resp["data"]["amount"])

