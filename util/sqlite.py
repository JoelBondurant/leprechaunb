"""
Key-Value Wrapper to sqlite3.
"""

import os
import sqlite3


class KV:

	def __init__(self, name):
		self.name = name
		base = "/data/sqlite"
		os.makedirs(base, mode=0o770, exist_ok=True)
		self.path = f"{base}/{name}.db"
		self.uri = f"file:{self.path}"
		try:
			sql_text = """
				create table if not exists kv
				(
					kk text primary key,
					vv text
				);
			"""
			self._execute(sql_text)
		except sqlite3.OperationalError as ex:
			print(ex)


	def reset(self):
		return os.remove(self.path)


	def dump(self):
		return self._execute("select kk, vv from kv;", fetch="many")


	def _execute(self, sql_txt, kv=None, fetch=None, read_only=False):
		uri = self.uri
		if read_only:
			uri += "?mode=ro"
		conn = sqlite3.connect(uri, uri=True)
		curs = conn.cursor()
		if fetch is None:
			if kv is None:
				curs.execute(sql_txt)
			else:
				curs.execute(sql_txt, kv)
			conn.commit()
			rs = None
		elif fetch == "one":
			if kv is None:
				curs.execute(sql_txt)
			else:
				curs.execute(sql_txt, kv)
			rs = curs.fetchone()
		elif fetch == "many":
			if kv is None:
				curs.execute(sql_txt)
			else:
				curs.execute(sql_txt, kv)
			rs = curs.fetchmany(100)
		curs.close()
		conn.close()
		return rs


	def put(self, akey, aval):
		print(f"put({akey}, {aval})")
		sql_txt = """
			insert into kv (kk, vv) values (:akey, :aval)
			on conflict(kk) do update set vv = :aval;
		"""
		kv = {
			"akey": akey,
			"aval": aval,
		}
		self._execute(sql_txt, kv)


	def get(self, akey):
		print(f"get({akey})")
		sql_txt = """
			select vv from kv where kk = :akey;
		"""
		kv = {
			"akey": akey,
		}
		rs = self._execute(sql_txt, kv, fetch="one", read_only=True)
		if rs is None:
			return None
		return rs[0]



