#!/usr/bin/env python3
"""
Currency crisis center.
"""
import time
import schedule
import concurrent.futures

from util import logger
import price_history


def minute_arrow():
	try:
		with concurrent.futures.ProcessPoolExecutor() as executor:
			executor.submit(price_history.minute_arrow)
	except Exception as ex:
		logger.exception(ex, "Root minute_arrow exception handler:")
		time.sleep(4)

def day_arrow():
	try:
		with concurrent.futures.ProcessPoolExecutor() as executor:
			executor.submit(price_history.day_arrow)
	except Exception as ex:
		logger.exception(ex, "Root day_arrow exception handler:")
		time.sleep(4)


schedule.every(20).seconds.do(minute_arrow)
schedule.every(60).seconds.do(day_arrow)


def main():
	"""
	Main entry to arrows.
	"""
	t0 = time.time()
	while True:
		schedule.run_pending()
		time.sleep(1)
		if time.time() - t0 > 120:
			t0 = time.time()
			logger.info("heartbeat")


if __name__ == "__main__":
	main()
