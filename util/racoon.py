"""
Racoon, the magic trash panda is a wrapper to 
the amazing/terrible Pandas.
"""

import os


def to_csv(df, file_path):
	"""
	Atomic write a csv.
	(getting data flicker with partial writes is fun)
	"""
	fn = os.path.basename(file_path)
	invisible_file_path = file_path.replace(fn, "." + fn)
	df.to_csv(invisible_file_path, index=False)
	os.rename(invisivle_file_path, file_path) # Atomic swap

