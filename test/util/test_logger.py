#!/usr/bin/env python3
"""
Test util.logger
"""

import importlib
import os
import time
import shutil

from util import logger


class TestLogger:

	logger_name = "tests"
	logger_root = "/data/log/"

	@classmethod
	def setup_class(self):
		print("TestLogger.setup_class" + TestLogger.logger_name)
		importlib.reload(logger)
		shutil.rmtree(TestLogger.logger_root + TestLogger.logger_name, ignore_errors=True)

	@classmethod
	def teardown_class(self):
		print("TestLogger.teardown_class" + TestLogger.logger_name)
		shutil.rmtree(TestLogger.logger_root + TestLogger.logger_name, ignore_errors=True)
		importlib.reload(logger)

	def test_logger(self):
		try:
			for idx in range(30):
				logger.info(f"testing, testing, 1, 2, 3.  {idx}")
		except Exception as ex:
			print(ex)
			raise ex


