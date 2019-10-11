"""
Test arrows.spot_history
"""
import os
import shutil

from arrows.quiver import spot_history

class TestSpotHist:

	adbcsv = "/data/adbcsvtest/"

	@classmethod
	def setup_class(self):
		print("TestSpotHist.setup_class: " + TestSpotHist.adbcsv)
		shutil.rmtree(TestSpotHist.adbcsv, ignore_errors=True)
		os.makedirs(TestSpotHist.adbcsv, mode=0o770, exist_ok=True)

	@classmethod
	def teardown_class(self):
		print("TestSpotHist.teardown_class: " + TestSpotHist.adbcsv)
		shutil.rmtree(TestSpotHist.adbcsv, ignore_errors=True)

	def test_minute_arrow(self):
		spot_history.minute_arrow()
		files_made = len(os.listdir(TestSpotHist.adbcsv))
		test_result = (files_made == 0)
		if not test_result:
			print(f"test_minute_arrow:files_made={files_made}")
		assert test_result

	def test_day_arrow(self):
		spot_history.day_arrow()
		files_made = len(os.listdir(TestSpotHist.adbcsv))
		test_result = (files_made == 0)
		if not test_result:
			print(f"test_day_arrow:files_made={files_made}")
		assert test_result

