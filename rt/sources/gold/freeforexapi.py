"""
FreeForexAPI Data Ingress
"""

import cachetools.func

from util import rock
from util import web


# FreeForexAPI API Endpoints:
base_uri = "https://www.freeforexapi.com/api/"


@cachetools.func.ttl_cache(ttl=1200)
def spot(pairs="USDXAU"):
	"""
	Freeforexapi USD/XAU spot.
	"""
	resp = web.get(base_uri + f"live?pairs={pairs}", timeout=4)
	usd_per_toz = float(1.0/resp["rates"][pairs]["rate"])
	usd_per_gram = (usd_per_toz / rock.grams_per_toz)
	return usd_per_gram

