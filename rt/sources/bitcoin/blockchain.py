"""
Blockchain.com Data Ingress
"""
import math

import cachetools.func

from util import logger
from util import web


# Blockchain.com API Endpoints:
base_uri = "https://api.blockchain.info/"


@cachetools.func.ttl_cache(ttl=60)
def stats():
	"""
	Blockchain.com stats.
	"""
	resp = web.get(base_uri + "stats")
	resp['hash_rate'] = int(resp['hash_rate'])
	resp['difficulty'] = int(resp['difficulty'])
	return resp


