"""
Key-Value Wrapper to sqlite3.
"""

import os
import sqlite3


class KV:

	def __init__(self, name):
		self.name = name
		base = "file:/data/sqlite"
		os.makedirs(base, mode=0o770, exist_ok=True)
		self.path = f"{base}/{name}.db"
		try:
			print("KV.create")
			sql_text = "create table if not exists kv (kk text primary key, vv text)"
			self.execute(sql_text)
		except sqlite3.OperationalError as ex:
			print("KV.create.err")
			print(ex)


	def execute(self, sql_txt, kv=None, fetch=None, read_only=False):
		print(f"execute(sql_txt={sql_txt}, kv={kv}, fetch={fetch}, ro={read_only})")
		uri = self.path
		if read_only:
			uri += "?mode=ro"
		curs = sqlite3.connect(uri, uri=True)
		if fetch is None:
			print(sql_txt, kv, fetch, read_only)
			if kv is None:
				curs.execute(sql_txt)
			else:
				curs.execute(sql_txt, kv)
			curs.commit()
			curs.close()
			return None
		elif fetch == "one":
			return curs.execute(sql_txt, kv).fetchone()
		elif fetch == "many":
			return curs.execute(sql_txt, kv).fetchmany()


	def put(self, akey, aval):
		print(f"put({akey}, {aval})")
		sql_txt = "insert into kv values (:akey, :aval)"
		kv = {
			"akey": akey,
			"aval": aval,
		}
		self.execute(sql_txt, kv)


	def get(self, akey):
		print(f"get({akey})")
		sql_txt = "select vv from kv where kk = :akey"
		kv = {
			"akey": akey,
		}
		rs = self.execute(sql_txt, kv, fetch="one", read_only=True)
		if rs is None:
			return None
		return rs[0]



