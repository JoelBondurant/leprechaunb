#!/usr/bin/env python3
"""
Test util.sqlite
"""
import os
import time

from util import sqlite


class TestSqlite:

	@classmethod
	def isetup_class(self):
		try:
			os.remove("/data/sqlite/test.db")
		except:
			pass

	def test_hammer(self):
		N = 30
		try:
			started = time.time()
			for idx in range(N):
				sqlite.KV("test").put(f"key{idx}", idx)
			test_result = True
			for idx in range(N):
				val = sqlite.KV("test").get(f"key{idx}")
				test_result = test_result and (val == idx)
				if not test_result:
					print(idx, val)
			elapsed = time.time() - started
			if elapsed >= 8:
				print("8 second timeout on test sqlite. ;?")
				assert False
		except Exception as ex:
			print(ex)
			raise ex

