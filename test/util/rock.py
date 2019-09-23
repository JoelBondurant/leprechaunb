#!/usr/bin/env python3
"""
Test util.rock
"""
import unittest

from util import rock


class TestRock(unittest.TestCase):

	def test_hammer(self):
		tr = rock.Rock("testrock")
		N = 1000
		for idx in range(N):
			tr.put(f"key{idx}", idx)
		test_result = True
		for idx in range(N):
			val = tr.get(f"key{idx}")
			test_result = test_result and (val == idx)
			if not test_result:
				print(idx, val)
			self.assertTrue(test_result)


if __name__ == "__main__":
	unittest.main()
