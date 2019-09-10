# APMEX Data Ingress
import requests

from util import logger
from util import rock

# APMEX API Endpoints:
base_uri = "https://widgets.apmex.com/widget/spotprice/"


"""
APMEX realtime prices.
"""
def spot():
	resp = requests.get(base_uri).text
	trim = resp[resp.lower().find("gold"):][:200]
	trim = trim[trim.find("$"):]
	usd_per_toz = float(trim.split()[0][1:].replace(",",""))
	usd_per_gram = (usd_per_toz / rock.grams_per_toz)
	return usd_per_gram

