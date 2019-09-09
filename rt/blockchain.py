# Blockchain.com Data Ingress
import requests

from util import logger

# Blockchain.com API Endpoints:
base_uri = "https://api.blockchain.info/"


def stats():
	"""
	Blockchain.com stats.
	"""
	resp = requests.get(base_uri + "stats").json()
	return resp


