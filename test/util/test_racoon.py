#!/usr/bin/env python3
"""
Test util.racoon
"""
import os
import time
import shutil

import pandas as pd

from util import racoon


class TestRacoon:


	def test_to_csv(self):
		"""
		Test to_csv.
		"""
		fn = "/tmp/test_racoon.csv"
		df = racoon.test_df()
		racoon.to_csv(df, fn)
		dg = pd.read_csv(fn)
		assert df.shape == dg.shape

