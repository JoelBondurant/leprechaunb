# Bisq Data Ingress
import requests

from util import logger

# Bisq API Endpoints:
base_uri = "https://markets.bisq.network/api/"


def spot(market="btc_usd"):
	"""
	Bisq realtime prices.
		market - [btc_usd]
	"""
	resp = requests.get(base_uri + f"ticker?market={market}").json()
	return float(resp[0]["last"])

