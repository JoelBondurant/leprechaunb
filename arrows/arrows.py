#!/usr/bin/env python3
"""
Currency crisis center.
"""
import time
import concurrent.futures

from util import logger
from util import rock

import spot_history



def rt_arrow():
	logger.info("<rt_arrow>")
	try:
		rtdb_data = rock.rocks("tsdbrocks").get("rtdb_data")
		rtdb_data["adb_timestamp"] = int(time.time())
		rock.rocks("adbrocks").put("rtdb_data", rtdb_data)
	except Exception as ex:
		logger.exception(ex, "Root rt_arrow exception handler:")
		time.sleep(2)
	logger.info("</rt_arrow>")


def minute_arrow():
	logger.info("<minute_arrow>")
	try:
		spot_history.minute_arrow()
	except Exception as ex:
		logger.exception(ex, "Root minute_arrow exception handler:")
		time.sleep(4)
	logger.info("</minute_arrow>")


def day_arrow():
	logger.info("<day_arrow>")
	try:
		spot_history.day_arrow()
	except Exception as ex:
		logger.exception(ex, "Root day_arrow exception handler:")
		time.sleep(8)
	logger.info("</day_arrow>")



def main():
	"""
	Main entry to arrows.
	"""
	logger.info("arrows started.")
	time.sleep(1)
	rt_arrow()
	minute_arrow()
	day_arrow()
	import schedule
	schedule.every(10).seconds.do(rt_arrow)
	schedule.every(20).seconds.do(minute_arrow)
	schedule.every(120).seconds.do(day_arrow)
	t0 = time.time()
	while True:
		schedule.run_pending()
		time.sleep(1)


if __name__ == "__main__":
	main()

