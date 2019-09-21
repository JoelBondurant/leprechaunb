# FreeForexAPI Data Ingress
import requests

from util import logger


# FreeForexAPI API Endpoints:
base_uri = "https://www.freeforexapi.com/api/"


def spot(pairs="USDXAU"):
	"""
	Freeforexapi spot prices.
	"""
	resp = requests.get(base_uri + f"live?pairs={pairs}").json()
	return float(1.0/resp["rates"][pairs]["rate"])

