#!/usr/bin/env python3
"""
Currency crisis center.
"""
import time
import concurrent.futures

from util import logger

import spot_history


def minute_arrow():
	logger.info("<minute_arrow>")
	try:
		with concurrent.futures.ProcessPoolExecutor() as executor:
			executor.submit(spot_history.minute_arrow)
	except Exception as ex:
		logger.exception(ex, "Root minute_arrow exception handler:")
		time.sleep(4)
	logger.info("</minute_arrow>")


def day_arrow():
	logger.info("<day_arrow>")
	try:
		with concurrent.futures.ProcessPoolExecutor() as executor:
			executor.submit(spot_history.day_arrow)
	except Exception as ex:
		logger.exception(ex, "Root day_arrow exception handler:")
		time.sleep(4)
	logger.info("</day_arrow>")



def main():
	"""
	Main entry to arrows.
	"""
	logger.info("arrows started.")
	import schedule
	schedule.every(20).seconds.do(minute_arrow)
	schedule.every(120).seconds.do(day_arrow)
	t0 = time.time()
	while True:
		schedule.run_pending()
		time.sleep(1)
		if time.time() - t0 > 120:
			t0 = time.time()
			logger.info("heartbeat")


if __name__ == "__main__":
	main()

