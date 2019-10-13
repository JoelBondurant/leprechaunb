"""
Bitcoin wrapper.
"""

import cachetools.func

import bitcoinlib
from bitcoinlib.services.services import Service



@cachetools.func.ttl_cache(ttl=120)
def service():
	serv = Service()
	return serv


def get_balance(addresses):
	"""
	Get the balance of a Bitcoin address.
	address - A bitcoin address.
	"""
	if type(addresses) == str:
		addresses = [addresses]
	return service().getbalance(addresses)


