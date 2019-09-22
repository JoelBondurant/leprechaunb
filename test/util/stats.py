#!/usr/bin/env python3
"""
Test util.stats
"""
import unittest

from util import stats


class TestStats(unittest.TestCase):

	def test_filter_outliers(self):
		test_cases = [
			[[1000, 1001, 1002], [1000, 1001, 1002]],
			[[1002, 1001, 1000, 0], [1002, 1001, 1000]],
			[[1002, 1001, 1000, 0], [1002, 1001, 1000]],
			[[1002, 1001, 1000, 1], [1002, 1001, 1000]],
			[[1002, 1001, 1000, 1], [1002, 1001, 1000]],
			[[1002, 1001, 1000, 100], [1002, 1001, 1000]],
			[[1002, 1001, 1000, 100], [1002, 1001, 1000]],
			[[10000, 10001, 10002], [10000, 10001, 10002]],
			[[10002, 10001, 10000, 0], [10002, 10001, 10000]],
			[[10002, 10001, 10000, 0], [10002, 10001, 10000]],
			[[10002, 10001, 10000, 1], [10002, 10001, 10000]],
			[[10002, 10001, 10000, 1], [10002, 10001, 10000]],
			[[10002, 10001, 10000, 100], [10002, 10001, 10000]],
			[[10002, 10001, 10000, 100], [10002, 10001, 10000]],
		]
		for test_case in test_cases:
			actual = stats.filter_outliers(test_case[0])
			test_result = actual == test_case[1]
			if not test_result:
				print(test_case, actual)
			self.assertTrue(test_result)


if __name__ == "__main__":
	unittest.main()
