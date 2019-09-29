#!/usr/bin/env python3
"""
Test util.stats
"""

from util import stats


class TestStats:

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
			assert test_result

	def test_closest(self):
		test_cases = [
			[[1,2,3], 0.1, 1],
			[[1,2,3], 1.1, 1],
			[[1,2,3], 1.9, 2],
			[[1,2,3], 2.9, 3],
			[[1,2,3], 3.9, 3],
		]
		for test_case in test_cases:
			test_result = stats.closest(test_case[0], test_case[1]) == test_case[2]
			if not test_result:
				print(test_case, test_result)
			assert test_result


