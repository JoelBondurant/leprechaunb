# APMEX Data Ingress

from . import lhtml
from util import logger
from util import rock


# APMEX API Endpoints:
base_uri = "https://widgets.apmex.com/widget/spotprice/"


def spot():
	"""
	APMEX realtime prices.
	"""
	htm = lhtml.parse_url(base_uri)
	spot_dom = htm.xpath("/html/body/div/div/table/tbody/tr[1]/td[2]")[0]
	spot_txt = spot_dom.text.strip().strip("$").replace(",", "")
	usd_per_toz = float(spot_txt)
	usd_per_gram = (usd_per_toz / rock.grams_per_toz)
	return usd_per_gram

