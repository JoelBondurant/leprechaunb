# Bisq Data Ingress

import cachetools.func

from util import web

# Bisq API Endpoints:
base_uri = "https://markets.bisq.network/api/"


@cachetools.func.ttl_cache(ttl=300)
def spot(market="btc_usd"):
	"""
	Bisq realtime prices.
		market - [btc_usd]
	"""
	resp = web.get(base_uri + f"ticker?market={market}", timeout=8)
	return float(resp[0]["last"])

