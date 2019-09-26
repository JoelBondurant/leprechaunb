"""
Test arrows.spot_history
"""
import os

from arrows import spot_history

class TestSpotHist:

	adbcsv = "/data/adbcsv/"

	@classmethod
	def setup_class(self):
		print("TestSpotHist.setup_class: " + TestSpotHist.adbcsv)
		# dev == prod...
		# shutil.rmtree(TestSpotHist.adbcsv, ignore_errors=True)

	@classmethod
	def teardown_class(self):
		print("TestSpotHist.teardown_class: " + TestSpotHist.adbcsv)
		# dev == prod...
		# shutil.rmtree(TestSpotHist.adbcsv, ignore_errors=True)

	def test_minute_arrow(self):
		spot_history.minute_arrow()
		test_result = len(os.listdir(TestSpotHist.adbcsv)) >= len(spot_history.keys)
		assert test_result

	def test_day_arrow(self):
		spot_history.day_arrow()
		test_result = len(os.listdir(TestSpotHist.adbcsv)) >= len(spot_history.keys)
		assert test_result

