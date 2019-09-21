# KITCO Data Ingress

from . import lhtml
from util import logger
from util import rock


# KITCO API Endpoints:
base_uri = "https://www.kitco.com/"


def spot():
	"""
	KITCO realtime prices.
	"""
	htm = lhtml.parse_url(base_uri + "charts/livegold.html")
	bid_usd_per_toz = float(htm.xpath("""//*[@id="sp-bid"]""")[0].text.replace(",",""))
	ask_usd_per_toz = float(htm.xpath("""//*[@id="sp-ask"]""")[0].text.replace(",",""))
	usd_per_toz = (bid_usd_per_toz + ask_usd_per_toz)/2.0
	usd_per_gram = (usd_per_toz / rock.grams_per_toz)
	return usd_per_gram

