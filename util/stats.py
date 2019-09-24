"""
Stack stats for apps.
"""
import statistics


def filter_outliers(alist, m=1.5):
	"""
	Don't include crazy screw-ups in price averaging, etc.
	"""
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

