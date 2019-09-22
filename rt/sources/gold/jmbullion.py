"""
JM Bullion Data Ingress
"""

from util import rock
from util import web


# JM Bullion API Endpoints:
base_uri = "https://www.jmbullion.com/utilities/calculators/forex.json"


def spot(symbol="USDXAU"):
	"""
	JM Bullion USD/XAU spot.
	"""
	resp = web.get(base_uri)
	usd_per_toz = 1.0/float(resp["quotes"][symbol])
	usd_per_gram = (usd_per_toz / rock.grams_per_toz)
	return usd_per_gram

