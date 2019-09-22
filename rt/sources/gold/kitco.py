"""
KITCO Data Ingress
"""

import cachetools.func

from util import rock
from util import web


# KITCO API Endpoints:
base_uri = "https://www.kitco.com/"


@cachetools.func.ttl_cache(ttl=600)
def spot():
	"""
	KITCO USD/XAU spot.
	"""
	htm = web.parse_url(base_uri + "charts/livegold.html")
	bid_usd_per_toz = float(htm.xpath("""//*[@id="sp-bid"]""")[0].text.replace(",",""))
	ask_usd_per_toz = float(htm.xpath("""//*[@id="sp-ask"]""")[0].text.replace(",",""))
	usd_per_toz = (bid_usd_per_toz + ask_usd_per_toz)/2.0
	usd_per_gram = (usd_per_toz / rock.grams_per_toz)
	return usd_per_gram

