"""
Blockchain.com Data Ingress
"""

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
	return resp


