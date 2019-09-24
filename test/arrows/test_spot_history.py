"""
Test arrows.spot_history
"""
import os

from arrows import spot_history


def test_minute_arrow():
	spot_history.minute_arrow()
	test_result = len(os.listdir("/data/adbcsv")) >= len(spot_history.keys)
	assert test_result

def test_day_arrow():
	spot_history.day_arrow()
	test_result = len(os.listdir("/data/adbcsv")) >= len(spot_history.keys)
	assert test_result

