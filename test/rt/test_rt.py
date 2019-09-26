#!/usr/bin/env python3
"""
Test rt.rt
"""

from rt.sources import bitcoin
from rt.sources import gold


class TestRT:

	def test_bitcoin_spots(self):
		for name, src in bitcoin.spot_sources.items():
			print(f"test_bitcoin_spots:{name}")
			src.spot()

	def test_gold_spots(self):
		for name, src in gold.spot_sources.items():
			print(f"test_gold_spots:{name}")
			src.spot()

