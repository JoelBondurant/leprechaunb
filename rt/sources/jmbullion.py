# JM Bullion Data Ingress
import requests

from util import logger
from util import rock


# JM Bullion API Endpoints:
base_uri = "https://www.jmbullion.com/utilities/calculators/forex.json"


def spot(symbol="USDXAU"):
	"""
	JM Bullion realtime prices.
	"""
	resp = requests.get(base_uri).json()
	usd_per_toz = 1.0/float(resp["quotes"][symbol])
	usd_per_gram = (usd_per_toz / rock.grams_per_toz)
	return usd_per_gram

