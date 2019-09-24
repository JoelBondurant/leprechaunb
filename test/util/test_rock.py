#!/usr/bin/env python3
"""
Test util.rock
"""
import os
import time
import shutil

from util import rock


class TestRock:

	DBNAME = "testrocks"

	@classmethod
	def setup_class(self):
		print("TestRock.rmtree:/data/" + TestRock.DBNAME)
		shutil.rmtree("/data" + TestRock.DBNAME, ignore_errors=True)

	def test_hammer(self):
		N = 30
		try:
			started = time.time()
			os.makedirs("/data/" + TestRock.DBNAME, exist_ok=True)
			for idx in range(N):
				rock.rocks(TestRock.DBNAME).put(f"key{idx}", idx)
			test_result = True
			for idx in range(N):
				val = rock.rocks(TestRock.DBNAME).get(f"key{idx}")
				test_result = test_result and (val == idx)
				if not test_result:
					print(idx, val)
			elapsed = time.time() - started
			if elapsed >= 8:
				print("8 second timeout on testrocks. ;?")
				assert False
		except Exception as ex:
			print(ex)
			raise ex


if __name__ == "__main__":
	unittest.main()
