# itBit Data Ingress
import requests

from util import logger

# itBit API Endpoints:
base_uri = "https://api.itbit.com/v1/"


def spot(symbol="XBTUSD"):
	"""
	itBit realtime prices.
		symbol - [XBTUSD]
	"""
	resp = requests.get(base_uri + f"markets/{symbol}/ticker").json()
	return float(resp["lastPrice"])

