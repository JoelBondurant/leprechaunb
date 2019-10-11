"""
Racoon, the magic trash panda is a wrapper to 
the amazing/terrible Pandas.
"""

import datetime
import os

import pandas as pd


def test_df(n=10):
	"""
	Generate a test dataframe.
	"""
	X = range(1, n+1)
	now = datetime.datetime.now().date()
	dat = {
		"x": X,
		"y": [3.14*x for x in X],
		"z": [now + datetime.timedelta(days=-x) for x in reversed(X)]
	}
	df = pd.DataFrame(dat)
	return df


def to_csv(df, file_path):
	"""
	Atomic write a csv.
	(getting data flicker with partial writes is fun)
	"""
	fn = os.path.basename(file_path)
	rn = os.urandom(8).hex()
	invisible_file_path = file_path.replace(fn, "." + rn + "_" + fn)
	df.to_csv(invisible_file_path, index=False)
	os.rename(invisible_file_path, file_path) # Atomic swap


def to_parquet(df, file_path):
	"""
	Atomic write a parquet file.
	(finally got some data corruption running multiple instances in prod)
	"""
	fn = os.path.basename(file_path)
	rn = os.urandom(8).hex()
	invisible_file_path = file_path.replace(fn, "." + rn + "_" + fn)
	df.to_parquet(invisible_file_path)
	os.rename(invisible_file_path, file_path) # Atomic swap

