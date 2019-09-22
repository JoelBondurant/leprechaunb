"""
Coinbase Data Ingress
"""

from util import web


# Coinbase API Endpoints:
base_uri = "https://api.coinbase.com/v2/"


def spot(endpoint="spot", currency="USD"):
	"""
	Coinbase realtime prices.
		endpoint - [spot|buy|sell]
		currency - [USD]
	"""
	resp = web.get(base_uri + f"prices/{endpoint}?" + f"currency={currency}")
	return float(resp["data"]["amount"])

