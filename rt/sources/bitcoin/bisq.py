# Bisq Data Ingress

from util import web

# Bisq API Endpoints:
base_uri = "https://markets.bisq.network/api/"


def spot(market="btc_usd"):
	"""
	Bisq realtime prices.
		market - [btc_usd]
	"""
	resp = web.get(base_uri + f"ticker?market={market}", timeout=4)
	return float(resp[0]["last"])

