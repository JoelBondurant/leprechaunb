"""
Generic key-value wrapper, implemented on RocksDB.
"""
import datetime
import os
import json
import time


import rocksdb

grams_per_toz = 31.1034768


def secondstamp():
	"""
	UTC Second Stamp
	"""
	return datetime.datetime.now().isoformat()[:19]

def minutestamp():
	"""
	UTC Minute Stamp
	"""
	return secondstamp()[:-3]

def hourstamp():
	"""
	UTC Hour Stamp
	"""
	return minutestamp()[:-3]


def daystamp():
	"""
	UTC Day Stamp
	"""
	return secondstamp()[:10]


class Rock:

	def __init__(self, db_name, read_only=False):
		"""
		Initalize a key-value store.
		"""
		self.db_name = db_name
		self.db_path = os.path.join("/data", db_name)
		self.read_only = read_only
		self.conn = None


	def connection(self):
		"""
		Store connection semi-ephemerally to avoid locks.
		"""
		if self.conn is None:
			conn_opts = rocksdb.Options(create_if_missing=True)
			conn = rocksdb.DB(self.db_path, conn_opts, read_only=self.read_only)
			self.conn = conn
		return self.conn


	def listkeys(self, decode=True):
		"""
		List all the keys in a RocksDB database.
		"""
		q = self.connection().iterkeys()
		q.seek_to_first()
		if decode:
			return [x.decode() for x in q]
		return list(q)


	def listitems(self, key_decode=True, value_decode=True, value_dejson=True):
		"""
		List all the key-value pairs in a RocksDB database.
		"""
		q = self.connection().iteritems()
		q.seek_to_first()
		ret = []
		for (k, v) in q:
			kr, vr = k, v
			if key_decode:
				kr = k.decode()
			if value_decode:
				vr = v.decode()
			if value_dejson:
				vr = json.loads(v)
			ret += (kr, vr)
		return ret


	def put(self, akey, aval, key_encode=True, value_encode=True):
		"""
		Write a key-value pair.
		"""
		if key_encode:
			bkey = akey.encode()
		else:
			bkey = akey
		if value_encode:
			bval = json.dumps(aval).encode()
		else:
			bval = aval
		self.connection().put(bkey, bval)


	def get(self, akey, key_encode=True, value_decode=True):
		tries = 0
		max_tries = 40
		while tries < max_tries:
			try:
				tries += 1
				return self._get(akey, key_encode=key_encode, value_decode=value_decode)
			except:
				time.sleep(0.1)
				if tries > max_tries - 1:
					raise


	def _get(self, akey, key_encode=True, value_decode=True):
		"""
		Read a key-value pair.
		"""
		if key_encode:
			bkey = akey.encode()
		else:
			bkey = akey
		bval = self.connection().get(bkey)
		if bval is None:
			return None
		if value_decode:
			try:
				aval = bval.decode()
				aval = json.loads(aval)
			except Exception as ex:
				msg = ex.args[0] + "\n"
				msg += "val.decode failure:\n"
				msg += f"akey={akey}\n"
				msg += f"bval={bval}\n"
				msg += f"db_name={self.db_name}\n"
				msg += f"read_only={self.read_only}\n"
				raise Exception(msg) from ex
		else:
			aval = bval
		return aval


	def multi_get(self, akeys, key_encode=True, cast_func=None):
		tries = 0
		max_tries = 30
		while tries < max_tries:
			try:
				tries += 1
				return self._multi_get(akeys, key_encode=key_encode, cast_func=cast_func)
			except:
				time.sleep(0.1)
				if tries > max_tries - 1:
					raise


	def _multi_get(self, akeys, key_encode=True, cast_func=None):
		"""
		Read a key-value list pair.
		"""
		if key_encode:
			bkeys = [akey.encode() for akey in akeys]
		else:
			bkeys = akeys
		bvals = self.connection().multi_get(bkeys)
		if cast_func:
			avals = {k.decode():cast_func(v.decode()) for k,v in bvals.items()}
		else:
			avals = bvals
		return avals

def rocks(rocks_db_name, read_only=False):
	"""
	Get a connection to RocksDB.
	"""
	return Rock(rocks_db_name, read_only=read_only)

