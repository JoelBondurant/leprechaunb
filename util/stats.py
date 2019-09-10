"""
Stack stats for apps.
"""
import statistics


def filter_outliers(alist, m=2):
	"""
	Don't include crazy screw-ups in price averaging, etc.
	"""
	med = statistics.median(alist)
	mean = statistics.mean(alist)
	avg = (mean + med)/2.0
	std = statistics.stdev(alist)
	return [x for x in alist if (x - avg) < m * std]
