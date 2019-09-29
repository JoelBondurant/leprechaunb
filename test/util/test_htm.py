#!/usr/bin/env python3
"""
Test util.htm
"""

from util import htm


class TestHTM:


	def test_to_table(self):
		"""
		Test to_to_table.
		"""
		test_cases = [
			[1,2,3],
		]
		for test_case in test_cases:
			tbl = htm.to_table(test_case)
			td_rows = len(tbl.split("</td>")) - 1
			test_rows = len(test_case)
			test_result = td_rows == test_rows
			if not test_result:
				print(test_case, td_rows, test_rows, "\n", tbl)
			assert test_result

