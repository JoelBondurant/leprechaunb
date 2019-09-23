#!/usr/bin/env python3
"""
Test arrows.spot_history
"""
import os
import unittest

from arrows import spot_history


class TestSpotHistory(unittest.TestCase):

	def test_spots_minutely(self):
		spot_history.spots_minutely()
		test_result = len(os.listdir("/data/adbcsv")) >= len(spot_history.keys)
		self.assertTrue(test_result)


if __name__ == "__main__":
	unittest.main()
