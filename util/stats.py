"""
Stack stats for apps.
"""

import math
import statistics


def filter_outliers(alist, m=1.5):
	"""
	Don't include crazy screw-ups in price averaging, etc.
	"""
	alist = [x for x in alist if not math.isnan(x)]
	med = statistics.median(alist)
	mean = statistics.mean(alist)
	avg = (mean + med)/2.0
	std = statistics.stdev(alist)
	result = [x for x in alist if x > avg - m*std]
	result = [x for x in result if x < avg + m*std]
	return result


def robust_mean(alist):
	"""
	A robust mean.
	"""
	return statistics.mean(filter_outliers(alist))


def closest(alist, aval):
	"""
	Find the closest item in a list.
	"""
	return min(alist, key=lambda x: abs(x - aval))
