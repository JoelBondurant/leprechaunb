"""
Bitcoin Data Ingress
"""
import json
import subprocess as sp

import cachetools.func

from util import logger


def cli(arg):
	"""
	bitcoin cli.
	"""
	return json.loads(sp.check_output(['bitcoin-cli', arg]))


@cachetools.func.ttl_cache(ttl=30)
def blockchaininfo():
	"""
	bitcoin getblockchaininfo.
	"""
	return cli('getblockchaininfo')


@cachetools.func.ttl_cache(ttl=30)
def info():
	"""
	bitcoin -getinfo.
	"""
	return cli('-getinfo')
