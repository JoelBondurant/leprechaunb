"""
APMEX Data Ingress
"""

import cachetools.func

from util import rock
from util import web


# APMEX API Endpoints:
base_uri = "https://widgets.apmex.com/widget/spotprice/"


@cachetools.func.ttl_cache(ttl=60)
def spot():
	"""
	APMEX USD/XAU spot.
	"""
	htm = web.parse_url(base_uri)
	spot_dom = htm.xpath("/html/body/div/div/table/tbody/tr[1]/td[2]")[0]
	spot_txt = spot_dom.text.strip().strip("$").replace(",", "")
	usd_per_toz = float(spot_txt)
	usd_per_gram = (usd_per_toz / rock.grams_per_toz)
	return usd_per_gram

